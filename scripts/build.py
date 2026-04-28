#!/usr/bin/env python3
"""Static site generator for SciSiteForge."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from scisiteforge.config import DEFAULT_THEME, load_config, save_config
from scisiteforge.content import (
    SiteContent,
    load_citegeist_cards,
    load_didactopus_cards,
    load_doclift_cards,
    load_groundrecall_cards,
)
from scisiteforge.render import html_escape, read_text, render_template, write_text
from scisiteforge.notebook import load_notebooks, render_notebooks
from scisiteforge.themes import available_themes, get_theme, materialize_theme


def _prompt_for_config() -> dict[str, Any]:
    print("=== SciSiteForge Site Config ===")
    themes = available_themes()
    print("Available themes:")
    for theme in themes:
        print(f"  - {theme.name}: {theme.description}")
    theme_name = input(f"Theme name (default: {DEFAULT_THEME}): ").strip() or DEFAULT_THEME
    languages_input = input("Languages (code:name pairs, comma-separated; default: en:English): ").strip() or "en:English"
    languages = []
    for pair in languages_input.split(","):
        code, name = pair.strip().split(":", 1)
        languages.append({"code": code.strip(), "name": name.strip()})
    return {
        "lang": input("Language code (default: en): ").strip() or "en",
        "title": input("Page title (default: SciSiteForge Preview): ").strip() or "SciSiteForge Preview",
        "site_title": input("Site name (default: SciSiteForge): ").strip() or "SciSiteForge",
        "license": input("License text (default: CC BY-SA 4.0): ").strip() or "CC BY-SA 4.0",
        "github_url": input("GitHub URL (optional): ").strip() or "https://github.com/",
        "contact_email": input("Contact email (optional): ").strip() or "admin@example.org",
        "theme": theme_name,
        "languages": languages,
        "navigation": [
            {"label": "Home", "href": "/"},
        ],
        "hero": {
            "kicker": "Preview",
            "title": "A site shell that can adapt to more than one audience.",
            "lede": "SciSiteForge now supports multiple theme presets and local content loaders for reusable science sites.",
            "actions": [
                {"label": "Read the overview", "href": "#overview", "primary": True},
                {"label": "Theme catalog", "href": "#themes", "primary": False},
            ],
        },
        "content_sources": {},
        "notebooks": [],
    }


def _language_options_html(languages: list[dict[str, str]], current_lang: str) -> str:
    visible_languages = [
        item
        for item in languages
        if item.get("coverage", True) or item.get("code") == current_lang
    ]
    return "\n".join(
        f'<option value="{html_escape(item["code"])}" {"selected" if item["code"] == current_lang else ""}>{html_escape(item["name"])}</option>'
        for item in visible_languages
    )


def _language_policy_html(language_policy: dict[str, Any]) -> str:
    planned_languages = language_policy.get("planned_languages", [])
    if not planned_languages:
        return ""
    planned_names = ", ".join(html_escape(item.get("name", item.get("code", ""))) for item in planned_languages if item.get("name") or item.get("code"))
    if not planned_names:
        return ""
    return f'<p class="language-policy-note">Planned languages: {planned_names}</p>'


def _hero_actions_html(actions: list[dict[str, Any]]) -> str:
    if not actions:
        return ""
    return "\n".join(
        f'<a class="button-link{" button-link-secondary" if not action.get("primary") else ""}" href="{html_escape(action.get("href", "#"))}">{html_escape(action.get("label", "Open"))}</a>'
        for action in actions
    )


def _navigation_html(navigation: list[dict[str, str]]) -> str:
    return "\n".join(
        f'<a href="{html_escape(item.get("href", "#"))}">{html_escape(item.get("label", "Link"))}</a>'
        for item in navigation
    )


def _render_cards(cards: list, template_path: str | Path, lang: str) -> str:
    if not cards:
        return ""
    template = read_text(template_path)
    rendered: list[str] = []
    for card in cards:
        rendered.append(
            render_template(
                template,
                {
                    "lang": lang,
                    "app_title": html_escape(card.title),
                    "app_description": html_escape(card.body),
                    "app_slug": html_escape(card.source or card.title.lower().replace(" ", "-")),
                    "section_title": html_escape(card.title),
                    "section_meta": html_escape(card.meta),
                    "section_excerpt": html_escape(card.body),
                    "section_path": html_escape(card.source or card.title.lower().replace(" ", "-")),
                    "href": html_escape(card.href),
                    "link_label": "Open",
                },
            )
        )
    return "\n".join(rendered)


def build_site(config_file: str | Path, output_dir: str | Path) -> dict[str, Any]:
    config = load_config(config_file)
    theme = get_theme(config.get("theme"))
    out_path = Path(output_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    theme_context = materialize_theme(theme, out_path)
    template = read_text(theme.template_path)

    content_sources = config.get("content_sources", {})
    site_content = SiteContent()
    if source := content_sources.get("doclift_bundle"):
        site_content.section_cards.extend(load_doclift_cards(source))
    if source := content_sources.get("groundrecall_bundle"):
        site_content.section_cards.extend(load_groundrecall_cards(source))
    if source := content_sources.get("didactopus_pack"):
        site_content.feature_cards.extend(load_didactopus_cards(source))
    if source := content_sources.get("bibliography"):
        site_content.bibliography_entries.extend(load_citegeist_cards(source))
    notebooks = load_notebooks(config)

    languages = config.get("languages", [{"code": config.get("lang", "en"), "name": "English", "coverage": True}])
    language_policy = config.get("language_policy", {})
    hero = config.get("hero", {})
    page_context = {
        "lang": config.get("lang", "en"),
        "page_title": html_escape(config.get("title", config.get("site_title", "SciSiteForge"))),
        "site_title": html_escape(config.get("site_title", "SciSiteForge")),
        "description": html_escape(config.get("description", "")),
        "license": html_escape(config.get("license", "CC BY-SA 4.0")),
        "github_url": html_escape(config.get("github_url", "")),
        "contact_email": html_escape(config.get("contact_email", "")),
        "theme_name": html_escape(theme.name),
        "theme_display_name": html_escape(theme.display_name),
        "theme_description": html_escape(theme.description),
        "theme_stylesheet_href": theme_context["theme_stylesheet_href"],
        "theme_script_href": theme_context["theme_script_href"],
        "theme_asset_prefix": theme_context["theme_asset_prefix"],
        "body_class": html_escape(theme.body_class),
        "site_shell_class": html_escape(theme.shell_class),
        "page_class": html_escape(theme.page_class),
        "navigation_html": _navigation_html(config.get("navigation", [])),
        "language_options": _language_options_html(languages, config.get("lang", "en")),
        "language_policy_html": _language_policy_html(language_policy),
        "hero_kicker": html_escape(hero.get("kicker", theme.display_name)),
        "hero_title": html_escape(hero.get("title", config.get("title", ""))),
        "hero_lede": html_escape(hero.get("lede", config.get("description", ""))),
        "hero_actions_html": _hero_actions_html(hero.get("actions", [])),
        "feature_cards_html": _render_cards(site_content.feature_cards, Path(__file__).parent.parent / "templates" / "app-card.html", config.get("lang", "en")),
        "section_cards_html": _render_cards(site_content.section_cards, Path(__file__).parent.parent / "templates" / "notebook-section.html", config.get("lang", "en")),
        "app_cards_html": _render_cards(site_content.app_cards, Path(__file__).parent.parent / "templates" / "app-card.html", config.get("lang", "en")),
        "bibliography_html": "\n".join(
            f'<li><strong>{html_escape(card.title)}</strong> <span class="meta">{html_escape(card.body)}</span></li>'
            for card in site_content.bibliography_entries
        ),
        "notebook_html": render_notebooks(notebooks, site_content),
    }
    page_context.update(
        {
            "content_panels_html": page_context["feature_cards_html"] + "\n" + page_context["section_cards_html"],
        }
    )
    rendered = render_template(template, page_context)
    write_text(out_path / "index.html", rendered)
    return {"output_dir": str(out_path), "theme": theme.name, "theme_assets": theme_context["theme_assets"]}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a SciSiteForge site from a JSON config.")
    parser.add_argument("--init", action="store_true", help="Create site config interactively")
    parser.add_argument("--config", help="Path to site.json")
    parser.add_argument("--output", help="Output directory for built site")
    parser.add_argument("--themes", action="store_true", help="List the built-in theme presets")
    parser.add_argument("--save-config", help="Where to write the config when using --init", default="site.json")
    args = parser.parse_args()

    if args.themes:
        for theme in available_themes():
            print(f"{theme.name}: {theme.description}")
        return

    if args.init:
        config = _prompt_for_config()
        save_config(args.save_config, config)
        print(f"Wrote config to {args.save_config}")
        return

    if args.config and args.output:
        result = build_site(args.config, args.output)
        print(f"Built {result['output_dir']} with theme {result['theme']}")
        return

    parser.print_help()


if __name__ == "__main__":
    main()
