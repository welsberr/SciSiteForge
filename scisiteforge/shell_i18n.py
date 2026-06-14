from __future__ import annotations

import json
from typing import Any


_SHELL_TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "theme": "Theme",
        "language": "Language",
        "sources": "Sources",
        "llm": "LLM",
        "overview": "Overview",
        "what_theme_supports": "What this theme supports",
        "notebook_and_apps": "Notebook and apps",
        "structured_sources": "Structured sources and learning artifacts",
        "theme_catalog": "Theme catalog",
        "github": "GitHub",
        "contact": "Contact",
        "feature_cards": "Feature cards",
        "notebook_app_content": "Notebook and app content",
        "bibliography": "Bibliography",
        "translation_preview_title": "Translation preview:",
        "translation_preview_body": "this language is in the translation queue for the current page set.",
        "translation_preview_link": "Open translation queue",
        "still_viewing_default": "You are still viewing the default language.",
        "language_selector_label": "Language",
    },
    "es": {
        "theme": "Tema",
        "language": "Idioma",
        "sources": "Fuentes",
        "llm": "LLM",
        "overview": "Resumen",
        "what_theme_supports": "Lo que admite este tema",
        "notebook_and_apps": "Cuaderno y aplicaciones",
        "structured_sources": "Fuentes estructuradas y materiales de aprendizaje",
        "theme_catalog": "Catálogo de temas",
        "github": "GitHub",
        "contact": "Contacto",
        "feature_cards": "Tarjetas destacadas",
        "notebook_app_content": "Contenido del cuaderno y las aplicaciones",
        "bibliography": "Bibliografía",
        "translation_preview_title": "Vista previa de traducción:",
        "translation_preview_body": "este idioma está en la cola de traducción para el conjunto actual de páginas.",
        "translation_preview_link": "Abrir cola de traducción",
        "still_viewing_default": "Todavía está viendo el idioma predeterminado.",
        "language_selector_label": "Idioma",
    },
    "fr": {
        "theme": "Thème",
        "language": "Langue",
        "sources": "Sources",
        "llm": "LLM",
        "overview": "Aperçu",
        "what_theme_supports": "Ce que ce thème prend en charge",
        "notebook_and_apps": "Carnet et applications",
        "structured_sources": "Sources structurées et ressources d'apprentissage",
        "theme_catalog": "Catalogue des thèmes",
        "github": "GitHub",
        "contact": "Contact",
        "feature_cards": "Cartes mises en avant",
        "notebook_app_content": "Contenu du carnet et des applications",
        "bibliography": "Bibliographie",
        "translation_preview_title": "Aperçu de traduction :",
        "translation_preview_body": "cette langue est dans la file de traduction pour l'ensemble actuel de pages.",
        "translation_preview_link": "Ouvrir la file de traduction",
        "still_viewing_default": "Vous consultez toujours la langue par défaut.",
        "language_selector_label": "Langue",
    },
    "de": {
        "theme": "Thema",
        "language": "Sprache",
        "sources": "Quellen",
        "llm": "LLM",
        "overview": "Überblick",
        "what_theme_supports": "Was dieses Thema unterstützt",
        "notebook_and_apps": "Notebook und Anwendungen",
        "structured_sources": "Strukturierte Quellen und Lernmaterialien",
        "theme_catalog": "Themenkatalog",
        "github": "GitHub",
        "contact": "Kontakt",
        "feature_cards": "Merkmale",
        "notebook_app_content": "Notebook- und Anwendungsinhalte",
        "bibliography": "Bibliografie",
        "translation_preview_title": "Übersetzungsvorschau:",
        "translation_preview_body": "diese Sprache steht für den aktuellen Seitensatz in der Übersetzungswarteschlange.",
        "translation_preview_link": "Übersetzungswarteschlange öffnen",
        "still_viewing_default": "Sie sehen weiterhin die Standardsprache.",
        "language_selector_label": "Sprache",
    },
    "pt": {
        "theme": "Tema",
        "language": "Idioma",
        "sources": "Fontes",
        "llm": "LLM",
        "overview": "Visão geral",
        "what_theme_supports": "O que este tema oferece",
        "notebook_and_apps": "Caderno e aplicativos",
        "structured_sources": "Fontes estruturadas e materiais de aprendizagem",
        "theme_catalog": "Catálogo de temas",
        "github": "GitHub",
        "contact": "Contato",
        "feature_cards": "Cartões em destaque",
        "notebook_app_content": "Conteúdo do caderno e dos aplicativos",
        "bibliography": "Bibliografia",
        "translation_preview_title": "Prévia da tradução:",
        "translation_preview_body": "este idioma está na fila de tradução para o conjunto atual de páginas.",
        "translation_preview_link": "Abrir fila de tradução",
        "still_viewing_default": "Você ainda está vendo o idioma padrão.",
        "language_selector_label": "Idioma",
    },
}

_COMMON_NAV_LABELS: dict[str, dict[str, str]] = {
    "Home": {"es": "Inicio", "fr": "Accueil", "de": "Startseite", "pt": "Início"},
    "Search": {"es": "Buscar", "fr": "Recherche", "de": "Suche", "pt": "Pesquisar"},
    "Roadmap": {"es": "Hoja de ruta", "fr": "Feuille de route", "de": "Fahrplan", "pt": "Roteiro"},
    "Start Here": {"es": "Empiece aquí", "fr": "Commencez ici", "de": "Hier beginnen", "pt": "Comece aqui"},
    "Key Resources": {"es": "Recursos clave", "fr": "Ressources clés", "de": "Wichtige Ressourcen", "pt": "Recursos principais"},
    "Overview": {"es": "Resumen", "fr": "Aperçu", "de": "Überblick", "pt": "Visão geral"},
    "Concepts": {"es": "Conceptos", "fr": "Concepts", "de": "Konzepte", "pt": "Conceitos"},
    "Notebook": {"es": "Cuaderno", "fr": "Carnet", "de": "Notebook", "pt": "Caderno"},
    "Learning Paths": {"es": "Rutas de aprendizaje", "fr": "Parcours d'apprentissage", "de": "Lernpfade", "pt": "Percursos de aprendizagem"},
    "Source Trails": {"es": "Rastros de fuentes", "fr": "Pistes des sources", "de": "Quellenpfade", "pt": "Trilhas de fontes"},
    "Support": {"es": "Apoyo", "fr": "Soutien", "de": "Unterstützung", "pt": "Suporte"},
    "Feedback": {"es": "Comentarios", "fr": "Retour", "de": "Feedback", "pt": "Feedback"},
    "Legacy Archive": {"es": "Archivo histórico", "fr": "Archive historique", "de": "Archiv", "pt": "Arquivo histórico"},
}


def shell_text(lang: str, key: str) -> str:
    bundle = _SHELL_TRANSLATIONS.get(lang) or _SHELL_TRANSLATIONS["en"]
    return bundle.get(key) or _SHELL_TRANSLATIONS["en"].get(key, key)


def shell_catalog_json() -> str:
    return json.dumps(_SHELL_TRANSLATIONS, ensure_ascii=False)


def nav_label(item: dict[str, Any], lang: str) -> str:
    translations = item.get("translations", {})
    if isinstance(translations, dict) and translations.get(lang):
        return str(translations[lang])
    label = str(item.get("label", "Link"))
    fallback = _COMMON_NAV_LABELS.get(label, {})
    return fallback.get(lang, label)


def nav_translation_payload(item: dict[str, Any]) -> str:
    payload: dict[str, str] = {}
    label = item.get("label")
    if label:
        payload["en"] = str(label)
        payload.update(_COMMON_NAV_LABELS.get(str(label), {}))
    translations = item.get("translations", {})
    if isinstance(translations, dict):
        for code, translated in translations.items():
            if translated:
                payload[str(code)] = str(translated)
    return json.dumps(payload, ensure_ascii=False)
