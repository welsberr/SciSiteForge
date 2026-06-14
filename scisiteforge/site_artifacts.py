from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .public_surface import audit_public_surface
from .render import html_escape, write_text
from .themes import ThemeSpec


def collect_public_pages(config: dict[str, Any], output_dir: str | Path) -> list[dict[str, str]]:
    out = Path(output_dir)
    pages = [
        {
            "route": "/",
            "path": "index.html",
            "title": str(config.get("title") or config.get("site_title") or "Home"),
        }
    ]
    if config.get("notebooks"):
        pages.append(
            {
                "route": "/notebook/",
                "path": "notebook/index.html",
                "title": "Notebook",
            }
        )
    return [page for page in pages if (out / page["path"]).exists()]


def build_translation_queue_payload(config: dict[str, Any], pages: list[dict[str, str]]) -> dict[str, Any]:
    default_language = str(config.get("lang") or "en")
    languages = []
    for item in config.get("languages", [{"code": default_language, "name": "English", "coverage": True}]):
        if not isinstance(item, dict):
            continue
        code = str(item.get("code") or "").strip()
        if not code or code == default_language:
            continue
        languages.append(
            {
                "code": code,
                "name": str(item.get("name") or code),
                "coverage": bool(item.get("coverage", False)),
            }
        )

    queue_pages = []
    missing_by_language = {language["code"]: 0 for language in languages}
    for page in pages:
        statuses: dict[str, str] = {}
        for language in languages:
            status = "current" if language["coverage"] else "missing"
            statuses[language["code"]] = status
            if status == "missing":
                missing_by_language[language["code"]] += 1
        queue_pages.append(
            {
                "route": page["route"],
                "source_path": page["path"],
                "title": page["title"],
                "statuses": statuses,
            }
        )

    return {
        "schema": "scisiteforge.translation_queue.v1",
        "default_language": default_language,
        "languages": languages,
        "summary": {
            "total_pages": len(queue_pages),
            "missing_by_language": missing_by_language,
        },
        "pages": queue_pages,
    }


def render_translation_status_html(
    *,
    config: dict[str, Any],
    theme: ThemeSpec,
    theme_context: dict[str, str],
    navigation_html: str,
    payload: dict[str, Any],
) -> str:
    title = html_escape(str(config.get("site_title") or "SciSiteForge"))
    summary_cards = "\n".join(
        f"""        <article class="feature-card">
          <h3>{html_escape(language["name"])}</h3>
          <p>{payload["summary"]["missing_by_language"][language["code"]]} pages are queued for translation from {html_escape(payload["default_language"]).upper()}.</p>
        </article>"""
        for language in payload["languages"]
    )
    header_cells = "".join(f"<th>{html_escape(language['name'])}</th>" for language in payload["languages"])
    rows = "\n".join(
        "<tr>"
        + f'<td><a href="{html_escape(page["route"])}">{html_escape(page["title"])}</a></td>'
        + f'<td><code>{html_escape(page["route"])}</code></td>'
        + "".join(f"<td>{html_escape(page['statuses'][language['code']].title())}</td>" for language in payload["languages"])
        + "</tr>"
        for page in payload["pages"]
    )
    language_options = "".join(
        f'<option value="{html_escape(payload["default_language"])}">{html_escape(payload["default_language"]).upper()}</option>'
    )
    return f"""<!DOCTYPE html>
<html lang="{html_escape(payload["default_language"])}">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Translation Queue — {title}</title>
  <link rel="stylesheet" href="{theme_context['theme_stylesheet_href']}">
  <script src="{theme_context['theme_script_href']}" defer></script>
</head>
<body class="{html_escape(theme.body_class)}">
  <div class="{html_escape(theme.shell_class)}">
    <header class="site-topbar">
      <div class="brand-block">
        <span class="brand-mark">{html_escape(theme.display_name)}</span>
        <a href="/">{title}</a>
        <p class="brand-summary">Translation readiness and queue status for this SciSiteForge output.</p>
      </div>
      <nav class="site-nav" aria-label="Primary navigation">
        {navigation_html}
        <select id="lang-switch" aria-label="Language">
          {language_options}
        </select>
      </nav>
    </header>

    <section class="hero-card">
      <p class="eyebrow">Translation Queue</p>
      <div class="hero-grid">
        <div>
          <h1>Initial language rollout for this site</h1>
          <p class="lede">Planned or partial languages stay visible in the site shell so readers can see the intended coverage, while this queue shows what is still pending.</p>
        </div>
      </div>
    </section>

    <section class="content-card">
      <p class="section-kicker">Summary</p>
      <h2 class="section-heading">Queue by language</h2>
      <div class="feature-grid">
{summary_cards}
      </div>
    </section>

    <section class="content-card">
      <p class="section-kicker">Queued Pages</p>
      <h2 class="section-heading">Current translation status</h2>
      <div class="table-wrap">
        <table class="status-table">
          <thead>
            <tr>
              <th>Page</th>
              <th>Route</th>
              {header_cells}
            </tr>
          </thead>
          <tbody>
            {rows}
          </tbody>
        </table>
      </div>
    </section>
  </div>
</body>
</html>
"""


def write_translation_artifacts(
    *,
    config: dict[str, Any],
    theme: ThemeSpec,
    theme_context: dict[str, str],
    navigation_html: str,
    output_dir: str | Path,
) -> dict[str, Any]:
    out = Path(output_dir)
    pages = collect_public_pages(config, out)
    payload = build_translation_queue_payload(config, pages)
    translation_root = out / "translation-status"
    translation_root.mkdir(parents=True, exist_ok=True)
    write_text(translation_root / "queue.json", json.dumps(payload, indent=2) + "\n")
    html = render_translation_status_html(
        config=config,
        theme=theme,
        theme_context=theme_context,
        navigation_html=navigation_html,
        payload=payload,
    )
    write_text(translation_root / "index.html", html)
    return payload


def verify_public_output(
    config: dict[str, Any], output_dir: str | Path, translation_payload: dict[str, Any]
) -> dict[str, Any]:
    out = Path(output_dir)
    checks: list[dict[str, Any]] = []

    def add_check(label: str, path: Path, required_strings: list[str]) -> None:
        raw = path.read_text(encoding="utf-8") if path.exists() else ""
        failures = [needle for needle in required_strings if needle not in raw]
        checks.append(
            {
                "label": label,
                "path": str(path.relative_to(out) if path.exists() else path),
                "status": "pass" if path.exists() and not failures else "fail",
                "failures": failures if failures else ([] if path.exists() else ["missing file"]),
            }
        )

    add_check(
        "site home",
        out / "index.html",
        [theme_marker for theme_marker in ["/theme/style.css", "/theme/main.js"] if theme_marker],
    )
    add_check(
        "translation queue page",
        out / "translation-status" / "index.html",
        ["Translation Queue", "Current translation status"],
    )
    add_check(
        "translation queue json",
        out / "translation-status" / "queue.json",
        ['"schema": "scisiteforge.translation_queue.v1"'],
    )
    if config.get("notebooks"):
        add_check(
            "notebook page",
            out / "notebook" / "index.html",
            ["Notebook", "Goals", "Apps and Labs"],
        )

    summary = {
        "total": len(checks),
        "passed": sum(1 for item in checks if item["status"] == "pass"),
        "failed": sum(1 for item in checks if item["status"] == "fail"),
    }
    report = {
        "schema": "scisiteforge.public_surface_status.v1",
        "translation_queue": translation_payload,
        "checks": checks,
        "summary": summary,
    }
    build_root = out / "build"
    build_root.mkdir(parents=True, exist_ok=True)
    guardrail_report = audit_public_surface(config, out)
    write_text(build_root / "public_surface_guardrails.json", json.dumps(guardrail_report, indent=2) + "\n")
    write_text(build_root / "site_regression_report.json", json.dumps(report, indent=2) + "\n")
    lines = [
        "# Site Regression Report",
        "",
        f"- Passed: `{summary['passed']}`",
        f"- Failed: `{summary['failed']}`",
        f"- Total: `{summary['total']}`",
        "",
    ]
    for item in checks:
        lines.extend(
            [
                f"## {item['label']}",
                "",
                f"- Path: `{item['path']}`",
                f"- Status: `{item['status']}`",
            ]
        )
        for failure in item["failures"]:
            lines.append(f"- Missing: `{failure}`")
        lines.append("")
    lines.extend(
        [
            "## Public Surface Guardrails",
            "",
            f"- Errors: `{guardrail_report['summary']['errors']}`",
            f"- Warnings: `{guardrail_report['summary']['warnings']}`",
            f"- HTML pages audited: `{guardrail_report['counts']['html_pages']}`",
            f"- Active pages audited: `{guardrail_report['counts']['active_pages']}`",
            f"- Search records audited: `{guardrail_report['counts']['search_records']}`",
            "",
            "See `public_surface_guardrails.json` for the full finding list.",
            "",
        ]
    )
    write_text(build_root / "site_regression_report.md", "\n".join(lines).rstrip() + "\n")
    return report
