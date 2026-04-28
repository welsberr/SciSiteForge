#!/usr/bin/env python3
"""Optional offline multilingual translation for SciSiteForge sites."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from time import sleep

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scisiteforge.config import load_config
from scisiteforge.translations import GenieHiveTranslator, TranslationConfig


LANGUAGES = {
    "es": "Spanish",
    "fr": "French",
    "pt": "Portuguese",
    "de": "German",
    "it": "Italian",
    "ru": "Russian",
    "zh": "Chinese",
    "ja": "Japanese",
    "ar": "Arabic",
    "hi": "Hindi",
}


def _load_bs4():
    try:
        from bs4 import BeautifulSoup, NavigableString  # type: ignore
    except Exception as exc:  # pragma: no cover - import-time fallback
        raise RuntimeError("BeautifulSoup4 is required for HTML translation.") from exc
    return BeautifulSoup, NavigableString


def extract_translatable_text(soup):
    _, NavigableString = _load_bs4()
    for elem in soup.descendants:
        if isinstance(elem, NavigableString) and elem.parent.name not in ["script", "style"]:
            if elem.strip():
                yield elem


def translate_html_file(src_path: Path, dest_path: Path, target_lang_code: str, translator: GenieHiveTranslator, glossary: dict[str, str] | None = None) -> None:
    BeautifulSoup, _ = _load_bs4()
    print(f"Translating {src_path} -> {dest_path}")
    html = src_path.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    for node in extract_translatable_text(soup):
        translated = translator.translate(str(node), LANGUAGES[target_lang_code], glossary=glossary)
        node.replace_with(translated)
        sleep(0.05)
    dest_path.parent.mkdir(parents=True, exist_ok=True)
    dest_path.write_text(str(soup), encoding="utf-8")


def build_translator(config_path: str | Path | None, args: argparse.Namespace) -> GenieHiveTranslator:
    site_config = {}
    if config_path:
        site_config = load_config(config_path)
    translation_cfg = site_config.get("translation", {})
    provider = getattr(args, "provider", None) or translation_cfg.get("provider") or "geniehive"
    cfg = TranslationConfig(
        provider=provider,
        base_url=args.base_url or translation_cfg.get("base_url") or "http://127.0.0.1:8800",
        model=args.model or translation_cfg.get("model") or "general_assistant",
        api_key=args.api_key or translation_cfg.get("api_key") or "",
        timeout=args.timeout or int(translation_cfg.get("timeout") or 120),
        system_prompt=translation_cfg.get("system_prompt")
        or "You are a careful scientific translator. Preserve meaning, structure, and technical terms. Return only the translation.",
    )
    return GenieHiveTranslator(cfg)


def main() -> None:
    parser = argparse.ArgumentParser(description="Translate a SciSiteForge site with an optional provider backend.")
    parser.add_argument("--langs", required=True, help="Comma-separated language codes (e.g. es,fr)")
    parser.add_argument("--src", default="content/en", help="Source directory (English)")
    parser.add_argument("--dest", default="content", help="Base destination directory")
    parser.add_argument("--config", help="Optional site config to pull GenieHive settings from")
    parser.add_argument("--provider", help="Translation provider (currently: geniehive)")
    parser.add_argument("--base-url", help="Provider base URL (default for GenieHive: http://127.0.0.1:8800)")
    parser.add_argument("--model", help="Provider model or role alias")
    parser.add_argument("--api-key", help="Provider API key")
    parser.add_argument("--timeout", type=int, help="HTTP timeout in seconds")
    args = parser.parse_args()

    translator = build_translator(args.config, args)
    src_base = Path(args.src)
    dest_base = Path(args.dest)
    glossary_cache: dict[str, dict[str, str]] = {}

    for lang_code in args.langs.split(","):
        if lang_code not in LANGUAGES:
            print(f"Unsupported language: {lang_code}")
            continue
        print(f"\n=== Translating to {LANGUAGES[lang_code]} ({lang_code}) ===")
        glossary_path = Path(__file__).parent / f"glossary_{lang_code}.json"
        glossary = glossary_cache.setdefault(lang_code, json.loads(glossary_path.read_text(encoding="utf-8")) if glossary_path.exists() else {})
        for html_file in src_base.rglob("*.html"):
            rel_path = html_file.relative_to(src_base)
            translate_html_file(html_file, dest_base / lang_code / rel_path, lang_code, translator, glossary=glossary)
    print("\nTranslation complete.")


if __name__ == "__main__":
    main()
