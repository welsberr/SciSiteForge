from __future__ import annotations

from dataclasses import dataclass, field
import json
import re
from pathlib import Path
from typing import Any

from .render import html_escape


@dataclass(slots=True)
class ContentCard:
    title: str
    body: str
    href: str = ""
    meta: str = ""
    kind: str = "feature"
    source: str = ""


@dataclass(slots=True)
class SiteContent:
    feature_cards: list[ContentCard] = field(default_factory=list)
    section_cards: list[ContentCard] = field(default_factory=list)
    app_cards: list[ContentCard] = field(default_factory=list)
    bibliography_entries: list[ContentCard] = field(default_factory=list)
    notes: list[str] = field(default_factory=list)


def cards_from_config(items: list[dict[str, Any]], *, default_kind: str) -> list[ContentCard]:
    cards: list[ContentCard] = []
    for item in items:
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or item.get("name") or "Item")
        cards.append(
            ContentCard(
                title=title,
                body=str(item.get("body") or item.get("description") or item.get("summary") or ""),
                href=str(item.get("href") or item.get("url") or ""),
                meta=str(item.get("meta") or item.get("kind") or default_kind),
                kind=str(item.get("kind") or default_kind),
                source=str(item.get("source") or item.get("id") or title.lower().replace(" ", "-")),
            )
        )
    return cards


def _first_paragraph(text: str) -> str:
    paragraphs = [chunk.strip() for chunk in re.split(r"\n\s*\n", text) if chunk.strip()]
    return paragraphs[0] if paragraphs else text.strip()


def _read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def _read_yaml(path: Path) -> Any:
    text = path.read_text(encoding="utf-8")
    try:  # pragma: no cover - exercised only if PyYAML is installed
        import yaml  # type: ignore

        return yaml.safe_load(text) or {}
    except Exception:
        stripped = text.strip()
        if stripped.startswith("{") or stripped.startswith("["):
            return json.loads(stripped)
        return _parse_minimal_yaml(text)


def _parse_scalar(value: str) -> Any:
    value = value.strip()
    if value in {"", "null", "~"}:
        return None
    if value == "[]":
        return []
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [_parse_scalar(part) for part in inner.split(",")]
    if value.startswith('"') and value.endswith('"'):
        return value[1:-1]
    if value.startswith("'") and value.endswith("'"):
        return value[1:-1]
    if value.isdigit():
        return int(value)
    if value.lower() in {"true", "false"}:
        return value.lower() == "true"
    return value


def _parse_minimal_yaml(text: str) -> dict[str, Any]:
    lines = [line.rstrip() for line in text.splitlines() if line.strip() and not line.strip().startswith("#")]
    root: dict[str, Any] = {}
    current_key: str | None = None
    current_item: dict[str, Any] | None = None

    for index, raw in enumerate(lines):
        stripped = raw.lstrip(" ")
        indent = len(raw) - len(stripped)
        if indent == 0:
            current_item = None
            if ":" not in stripped:
                continue
            key, value = stripped.split(":", 1)
            key = key.strip()
            value = value.strip()
            if value:
                root[key] = _parse_scalar(value)
            else:
                next_line = lines[index + 1] if index + 1 < len(lines) else ""
                root[key] = [] if next_line.lstrip(" ").startswith("- ") else {}
            current_key = key
            continue

        if current_key is None:
            continue

        container = root.get(current_key)
        if isinstance(container, list) and stripped.startswith("- "):
            item_text = stripped[2:].strip()
            if not item_text:
                current_item = {}
                container.append(current_item)
            elif ":" in item_text:
                item_key, item_value = item_text.split(":", 1)
                current_item = {item_key.strip(): _parse_scalar(item_value)}
                container.append(current_item)
            else:
                current_item = None
                container.append(_parse_scalar(item_text))
            continue

        target = current_item if isinstance(current_item, dict) else container
        if isinstance(target, dict) and ":" in stripped:
            key, value = stripped.split(":", 1)
            target[key.strip()] = _parse_scalar(value)
        elif isinstance(target, list) and stripped.startswith("- "):
            target.append(_parse_scalar(stripped[2:]))

    return root


def load_doclift_cards(bundle_root: str | Path) -> list[ContentCard]:
    base = Path(bundle_root)
    manifest = _read_json(base / "manifest.json")
    cards: list[ContentCard] = []
    for item in manifest.get("documents", []):
        if not isinstance(item, dict):
            continue
        title = str(item.get("title") or item.get("document_id") or "Document")
        body = str(item.get("summary") or item.get("description") or item.get("document_kind") or "")
        markdown_path = item.get("markdown_path")
        source_href = str(item.get("canonical_url") or item.get("source_path") or "")
        if markdown_path:
            md_path = base / str(markdown_path)
            if md_path.exists():
                body = _first_paragraph(md_path.read_text(encoding="utf-8"))
        cards.append(
            ContentCard(
                title=title,
                body=body,
                href=source_href,
                meta=str(item.get("document_kind") or "document"),
                kind="notebook",
                source=str(item.get("document_id") or title.lower().replace(" ", "-")),
            )
        )
    return cards


def load_groundrecall_cards(bundle_root: str | Path) -> list[ContentCard]:
    base = Path(bundle_root)
    bundle_path = base / "groundrecall_query_bundle.json"
    if not bundle_path.exists():
        bundle_path = base / "exports" / "codex" / "codex_bundle.json"
    if not bundle_path.exists():
        return []
    payload = _read_json(bundle_path)
    concept = payload.get("concept") or {}
    title = str(concept.get("title") or payload.get("title") or "GroundRecall concept")
    body = str(payload.get("summary") or payload.get("explanation") or payload.get("body") or "")
    claims = payload.get("claims") or payload.get("related_claims") or []
    claim_count = len(claims) if isinstance(claims, list) else 0
    cards = [
        ContentCard(
            title=title,
            body=body or f"{claim_count} related claims and observations are bundled here.",
            href=str(payload.get("source_url") or ""),
            meta=f"GroundRecall bundle · {claim_count} claims",
            kind="section",
            source=str(concept.get("concept_id") or title.lower().replace(" ", "-")),
        )
    ]
    for claim in claims if isinstance(claims, list) else []:
        if not isinstance(claim, dict):
            continue
        cards.append(
            ContentCard(
                title=str(claim.get("claim_text") or claim.get("title") or "Claim"),
                body=str(claim.get("support") or claim.get("notes") or ""),
                href=str(claim.get("source_url") or ""),
                meta=str(claim.get("claim_kind") or "claim"),
                kind="section",
                source=str(claim.get("claim_id") or claim.get("id") or ""),
            )
        )
    return cards


def load_didactopus_cards(pack_root: str | Path) -> list[ContentCard]:
    base = Path(pack_root)
    pack_path = base / "pack.yaml"
    concepts_path = base / "concepts.yaml"
    if not pack_path.exists() or not concepts_path.exists():
        return []
    pack = _read_yaml(pack_path) or {}
    concepts = _read_yaml(concepts_path) or {}
    cards: list[ContentCard] = []
    for concept in concepts.get("concepts", []):
        if not isinstance(concept, dict):
            continue
        title = str(concept.get("title") or concept.get("id") or "Concept")
        description = str(concept.get("description") or "")
        prerequisites = concept.get("prerequisites") or []
        prereq_text = ", ".join(str(item) for item in prerequisites) if prerequisites else "None"
        body = description or f"Prerequisites: {prereq_text}."
        cards.append(
            ContentCard(
                title=title,
                body=body,
                href=str(pack.get("display_name") or pack.get("name") or ""),
                meta=f"Didactopus concept · {prereq_text}",
                kind="app",
                source=str(concept.get("id") or title.lower().replace(" ", "-")),
            )
        )
    return cards


def load_citegeist_cards(source_root: str | Path) -> list[ContentCard]:
    root = Path(source_root)
    bib_files = sorted(
        path
        for path in root.rglob("*.bib")
        if path.is_file() and not path.name.endswith("-bak.bib") and not path.name.startswith(".")
    )
    if not bib_files:
        return []
    cards: list[ContentCard] = []
    try:
        from citegeist.bibtex import parse_bibtex  # type: ignore
    except Exception:
        parse_bibtex = None
    for bib_path in bib_files:
        text = bib_path.read_text(encoding="utf-8")
        entries = parse_bibtex(text) if parse_bibtex is not None else _fallback_parse_bibtex(text)
        for entry in entries:
            data = entry if isinstance(entry, dict) else entry.__dict__
            title = str(data.get("title") or data.get("citation_key") or "Reference")
            author = str(data.get("author") or data.get("editor") or "")
            year = str(data.get("year") or "")
            body = " · ".join(part for part in [author, year] if part).strip()
            cards.append(
                ContentCard(
                    title=title,
                    body=body or bib_path.name,
                    href=str(bib_path.relative_to(root)),
                    meta="CiteGeist bibliography",
                    kind="bibliography",
                    source=str(data.get("citation_key") or title.lower().replace(" ", "-")),
                )
            )
    return cards


def _fallback_parse_bibtex(text: str) -> list[dict[str, str]]:
    entries: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if stripped.startswith("@") and "{" in stripped:
            if current:
                entries.append(current)
            kind, rest = stripped[1:].split("{", 1)
            key = rest.split(",", 1)[0].strip()
            current = {"entry_type": kind.strip(), "citation_key": key}
            continue
        if current and "=" in stripped:
            field, value = stripped.split("=", 1)
            current[field.strip().lower()] = value.strip().strip(",{}")
    if current:
        entries.append(current)
    return entries
