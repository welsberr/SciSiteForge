from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from .content import ContentCard, SiteContent
from .render import html_escape


@dataclass(slots=True)
class NotebookApp:
    title: str
    href: str
    description: str = ""


@dataclass(slots=True)
class Notebook:
    notebook_id: str
    title: str
    summary: str = ""
    audience: str = ""
    goals: list[str] = field(default_factory=list)
    apps: list[NotebookApp] = field(default_factory=list)
    source_kinds: list[str] = field(default_factory=list)
    max_items: int = 8


def load_notebooks(config: dict[str, Any]) -> list[Notebook]:
    notebooks: list[Notebook] = []
    for item in config.get("notebooks", []):
        if not isinstance(item, dict):
            continue
        apps = [
            NotebookApp(
                title=str(app.get("title") or app.get("href") or "App"),
                href=str(app.get("href") or "#"),
                description=str(app.get("description") or ""),
            )
            for app in item.get("apps", [])
            if isinstance(app, dict)
        ]
        notebooks.append(
            Notebook(
                notebook_id=str(item.get("id") or item.get("notebook_id") or item.get("title") or "notebook"),
                title=str(item.get("title") or "Notebook"),
                summary=str(item.get("summary") or item.get("description") or ""),
                audience=str(item.get("audience") or ""),
                goals=[str(goal) for goal in item.get("goals", [])],
                apps=apps,
                source_kinds=[str(kind) for kind in item.get("source_kinds", [])],
                max_items=int(item.get("max_items") or 8),
            )
        )
    return notebooks


def select_notebook_cards(notebook: Notebook, site_content: SiteContent) -> list[ContentCard]:
    cards = (
        site_content.section_cards
        + site_content.app_cards
        + site_content.feature_cards
        + site_content.bibliography_entries
    )
    if notebook.source_kinds:
        allowed = set(notebook.source_kinds)
        cards = [card for card in cards if card.kind in allowed or card.meta in allowed]
    return cards[: notebook.max_items]


def render_notebooks(notebooks: list[Notebook], site_content: SiteContent) -> str:
    if not notebooks:
        return ""
    return "\n".join(render_notebook(notebook, site_content) for notebook in notebooks)


def render_notebook(notebook: Notebook, site_content: SiteContent) -> str:
    cards = select_notebook_cards(notebook, site_content)
    goals_html = "".join(f"<li>{html_escape(goal)}</li>" for goal in notebook.goals)
    apps_html = "".join(
        (
            '<li>'
            f'<a href="{html_escape(app.href)}">{html_escape(app.title)}</a>'
            f' <span class="meta">{html_escape(app.description)}</span>'
            '</li>'
        )
        for app in notebook.apps
    )
    cards_html = "".join(
        (
            '<li>'
            f'<strong>{html_escape(card.title)}</strong>'
            f' <span class="meta">{html_escape(card.meta)}</span>'
            f'<p>{html_escape(card.body)}</p>'
            '</li>'
        )
        for card in cards
    )
    audience_html = f'<p class="meta">Audience: {html_escape(notebook.audience)}</p>' if notebook.audience else ""
    goals_block = f'<div><h3>Goals</h3><ul class="plain-list">{goals_html}</ul></div>' if goals_html else ""
    apps_block = f'<div><h3>Apps and Labs</h3><ul class="plain-list">{apps_html}</ul></div>' if apps_html else ""
    cards_block = f'<div><h3>Study Material</h3><ul class="plain-list">{cards_html}</ul></div>' if cards_html else ""
    return (
        f'<article class="notebook-panel" id="{html_escape(notebook.notebook_id)}">'
        f'<h2>{html_escape(notebook.title)}</h2>'
        f'<p>{html_escape(notebook.summary)}</p>'
        f'{audience_html}'
        f'<div class="notebook-grid">{goals_block}{apps_block}{cards_block}</div>'
        '</article>'
    )
