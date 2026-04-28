from __future__ import annotations

from dataclasses import dataclass
import json
from urllib import error, request


@dataclass(slots=True)
class TranslationConfig:
    provider: str = "geniehive"
    base_url: str = "http://127.0.0.1:8800"
    model: str = "general_assistant"
    api_key: str = ""
    timeout: int = 120
    system_prompt: str = (
        "You are a careful scientific translator. Preserve meaning, section structure, "
        "and technical terminology. Return only the translation."
    )


class GenieHiveTranslator:
    def __init__(self, config: TranslationConfig):
        if config.provider != "geniehive":
            raise ValueError(f"Unsupported translation provider: {config.provider}")
        self.config = config

    def translate(self, text: str, target_language: str, glossary: dict[str, str] | None = None) -> str:
        if not text.strip():
            return text
        prompt = self._build_prompt(text, target_language, glossary or {})
        payload = {
            "model": self.config.model,
            "messages": [
                {"role": "system", "content": self.config.system_prompt},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.1,
        }
        response = self._post_json("/v1/chat/completions", payload)
        try:
            return response["choices"][0]["message"]["content"].strip()
        except Exception as exc:
            raise RuntimeError("GenieHive response did not contain a translation.") from exc

    def _build_prompt(self, text: str, target_language: str, glossary: dict[str, str]) -> str:
        glossary_text = ""
        if glossary:
            glossary_text = "Use these translations when they fit the target language:\n" + "\n".join(
                f"- {source} => {target}" for source, target in glossary.items()
            )
            glossary_text += "\n\n"
        return (
            f"Translate the following English text into {target_language}.\n"
            "Keep the HTML/text structure intact. Do not add commentary.\n\n"
            f"{glossary_text}Text:\n{text}\n"
        )

    def _post_json(self, path: str, payload: dict) -> dict:
        url = self.config.base_url.rstrip("/") + path
        data = json.dumps(payload).encode("utf-8")
        headers = {"Content-Type": "application/json"}
        if self.config.api_key:
            headers["Authorization"] = f"Bearer {self.config.api_key}"
        req = request.Request(url, data=data, headers=headers, method="POST")
        try:
            with request.urlopen(req, timeout=self.config.timeout) as resp:
                return json.loads(resp.read().decode("utf-8"))
        except error.HTTPError as exc:  # pragma: no cover - network path
            raise RuntimeError(f"GenieHive request failed with HTTP {exc.code}") from exc
        except error.URLError as exc:  # pragma: no cover - network path
            raise RuntimeError(f"GenieHive request failed: {exc.reason}") from exc
