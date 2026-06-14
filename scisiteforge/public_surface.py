from __future__ import annotations

from dataclasses import dataclass
from html.parser import HTMLParser
import json
from pathlib import Path
from typing import Any


ACTIVE_ROUTE_PREFIXES = ("translation-status/", "workbench/", "review/", "scisiteforge-preview/")
PROCESS_ROUTE_PREFIXES = ("workbench/", "review/", "scisiteforge-preview/")


@dataclass
class HtmlMetadata:
    title: str = ""
    description: str = ""
    canonicals: list[str] | None = None
    json_ld_blocks: list[str] | None = None
    robots: str = ""

    def __post_init__(self) -> None:
        if self.canonicals is None:
            self.canonicals = []
        if self.json_ld_blocks is None:
            self.json_ld_blocks = []


class _MetadataParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.metadata = HtmlMetadata()
        self._in_title = False
        self._in_json_ld = False
        self._title_parts: list[str] = []
        self._json_ld_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {name.lower(): value or "" for name, value in attrs}
        tag = tag.lower()
        if tag == "title":
            self._in_title = True
        elif tag == "meta" and attr.get("name", "").lower() == "description":
            self.metadata.description = attr.get("content", "").strip()
        elif tag == "meta" and attr.get("name", "").lower() == "robots":
            self.metadata.robots = attr.get("content", "").strip()
        elif tag == "link" and attr.get("rel", "").lower() == "canonical":
            self.metadata.canonicals.append(attr.get("href", "").strip())
        elif tag == "script" and attr.get("type", "").lower() == "application/ld+json":
            self._in_json_ld = True
            self._json_ld_parts = []

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag == "title":
            self._in_title = False
            self.metadata.title = "".join(self._title_parts).strip()
        elif tag == "script" and self._in_json_ld:
            self._in_json_ld = False
            self.metadata.json_ld_blocks.append("".join(self._json_ld_parts).strip())

    def handle_data(self, data: str) -> None:
        if self._in_title:
            self._title_parts.append(data)
        elif self._in_json_ld:
            self._json_ld_parts.append(data)


def route_for_html(path: Path, root: Path) -> str:
    rel = path.relative_to(root).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    return "/" + rel


def _parse_html_metadata(path: Path) -> HtmlMetadata:
    parser = _MetadataParser()
    parser.feed(path.read_text(encoding="utf-8", errors="replace"))
    return parser.metadata


def _json_ld_nodes(blocks: list[str]) -> tuple[list[dict[str, Any]], list[str]]:
    nodes: list[dict[str, Any]] = []
    errors: list[str] = []
    for block in blocks:
        if not block:
            continue
        try:
            payload = json.loads(block)
        except json.JSONDecodeError as exc:
            errors.append(str(exc))
            continue
        if isinstance(payload, dict) and isinstance(payload.get("@graph"), list):
            nodes.extend(node for node in payload["@graph"] if isinstance(node, dict))
        elif isinstance(payload, dict):
            nodes.append(payload)
        elif isinstance(payload, list):
            nodes.extend(node for node in payload if isinstance(node, dict))
    return nodes, errors


def audit_public_surface(config: dict[str, Any], output_dir: str | Path) -> dict[str, Any]:
    root = Path(output_dir)
    base_url = str(config.get("base_url") or config.get("canonical_base_url") or "").rstrip("/")
    findings: list[dict[str, Any]] = []
    counts = {
        "html_pages": 0,
        "active_pages": 0,
        "search_manifests": 0,
        "search_records": 0,
    }

    def add(level: str, code: str, path: Path, message: str) -> None:
        findings.append(
            {
                "level": level,
                "code": code,
                "path": path.relative_to(root).as_posix(),
                "message": message,
            }
        )

    for path in sorted(root.rglob("*.html")):
        if "/build/" in f"/{path.relative_to(root).as_posix()}":
            continue
        counts["html_pages"] += 1
        route = route_for_html(path, root)
        rel = path.relative_to(root).as_posix()
        active = rel.startswith(ACTIVE_ROUTE_PREFIXES)
        process_surface = rel.startswith(PROCESS_ROUTE_PREFIXES)
        if active:
            counts["active_pages"] += 1
        metadata = _parse_html_metadata(path)
        if not metadata.title:
            add("error", "missing_title", path, "HTML page has no title.")
        if not metadata.description:
            add("warning", "missing_description", path, "HTML page has no meta description.")
        if len(metadata.canonicals) > 1:
            add("error", "duplicate_canonical", path, "HTML page has more than one canonical link.")
        elif not active and not metadata.canonicals:
            add("warning", "missing_canonical", path, "Public HTML page has no canonical link.")
        elif metadata.canonicals:
            canonical = metadata.canonicals[0]
            if base_url and not canonical.startswith(f"{base_url}/") and canonical != base_url:
                add("warning", "canonical_base_mismatch", path, f"Canonical URL is outside configured base URL: {canonical}")
            if not canonical.startswith("https://"):
                add("warning", "canonical_not_https", path, f"Canonical URL is not absolute HTTPS: {canonical}")
        nodes, json_errors = _json_ld_nodes(metadata.json_ld_blocks)
        for error in json_errors:
            add("error", "invalid_json_ld", path, f"JSON-LD block is not valid JSON: {error}")
        if not active and not nodes:
            add("warning", "missing_json_ld", path, "Public HTML page has no JSON-LD structured data.")
        canonical = metadata.canonicals[0] if metadata.canonicals else ""
        for node in nodes:
            node_url = str(node.get("url") or node.get("mainEntityOfPage") or "")
            if canonical and node_url and node_url != canonical:
                add("warning", "json_ld_url_mismatch", path, f"JSON-LD URL does not match canonical: {node_url}")
            node_type = node.get("@type")
            about = json.dumps(node.get("about", ""), sort_keys=True) if "about" in node else ""
            if active and (node_type == "Article" or "Archive Page" in about):
                add("warning", "active_surface_archive_json_ld", path, "Active surface JSON-LD looks like canonical archive content.")
        if process_surface and "noindex" not in metadata.robots.lower():
            add("warning", "active_surface_indexable", path, "Active or process page is missing a noindex robots directive.")

    for manifest in sorted(root.glob("search/corpora.json")):
        counts["search_manifests"] += 1
        try:
            payload = json.loads(manifest.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            add("error", "invalid_search_manifest", manifest, f"Search corpus manifest is invalid JSON: {exc}")
            continue
        corpora = payload.get("corpora") if isinstance(payload, dict) else None
        if not isinstance(corpora, list):
            add("error", "invalid_search_manifest_shape", manifest, "Search corpus manifest must contain a corpora list.")
            continue
        for item in corpora:
            if not isinstance(item, dict):
                add("error", "invalid_search_manifest_item", manifest, "Search corpus manifest item is not an object.")
                continue
            rel_path = str(item.get("path") or item.get("file") or "")
            if not rel_path:
                add("error", "missing_search_corpus_path", manifest, "Search corpus manifest item has no path/file.")
                continue
            corpus_path = root / "search" / rel_path
            if not corpus_path.exists():
                add("error", "missing_search_corpus_file", manifest, f"Search corpus file is missing: search/{rel_path}")
                continue
            seen_keys: set[str] = set()
            for line_no, line in enumerate(corpus_path.read_text(encoding="utf-8").splitlines(), start=1):
                if not line.strip():
                    continue
                try:
                    record = json.loads(line)
                except json.JSONDecodeError as exc:
                    add("error", "invalid_search_record", corpus_path, f"Line {line_no} is invalid JSON: {exc}")
                    continue
                if not isinstance(record, dict):
                    add("error", "invalid_search_record_shape", corpus_path, f"Line {line_no} is not an object.")
                    continue
                counts["search_records"] += 1
                key = str(record.get("route") or record.get("url") or record.get("key") or "")
                if key in seen_keys:
                    add("error", "duplicate_search_record", corpus_path, f"Duplicate search record key: {key}")
                seen_keys.add(key)
                text = str(record.get("text") or record.get("body") or record.get("content") or "").strip()
                if not text:
                    add("error", "blank_search_record", corpus_path, f"Line {line_no} has no searchable text.")

    summary = {
        "errors": sum(1 for finding in findings if finding["level"] == "error"),
        "warnings": sum(1 for finding in findings if finding["level"] == "warning"),
        "total": len(findings),
    }
    return {
        "schema": "scisiteforge.public_surface_guardrails.v1",
        "counts": counts,
        "summary": summary,
        "findings": findings,
    }
