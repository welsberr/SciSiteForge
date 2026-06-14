from __future__ import annotations

import json
import unittest
from pathlib import Path
from types import SimpleNamespace
import sys
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "scripts"))

import build
import translate_site

from scisiteforge.content import SiteContent, cards_from_config, load_citegeist_cards, load_didactopus_cards, load_doclift_cards, load_groundrecall_cards
from scisiteforge.notebook import load_notebooks, render_notebooks
from scisiteforge.public_surface import audit_public_surface
from scisiteforge.themes import get_theme, materialize_theme
from scisiteforge.translations import GenieHiveTranslator, TranslationConfig


class SciSiteForgeTests(unittest.TestCase):
    def test_theme_materialization_copies_theme_assets(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            theme = get_theme("talkorigins-modern")
            payload = materialize_theme(theme, tmp_path)

            self.assertTrue((tmp_path / "theme" / "style.css").exists())
            self.assertTrue((tmp_path / "theme" / "main.js").exists())
            self.assertTrue((tmp_path / "theme" / "assets" / "toa.ico").exists())
            self.assertTrue((tmp_path / "theme" / "assets" / "toa_logo_001_edit_001.png").exists())
            self.assertEqual(payload["theme_name"], "talkorigins-modern")

    def test_content_loaders_parse_local_repo_artifacts(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)

            doclift_root = tmp_path / "doclift"
            doclift_root.mkdir()
            (doclift_root / "manifest.json").write_text(
                json.dumps(
                    {
                        "documents": [
                            {
                                "document_id": "doc-1",
                                "title": "Legacy Document",
                                "document_kind": "article",
                                "markdown_path": "documents/doc-1/document.md",
                                "source_path": "source/doc-1.html",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (doclift_root / "documents" / "doc-1").mkdir(parents=True)
            (doclift_root / "documents" / "doc-1" / "document.md").write_text("First paragraph.\n\nSecond.", encoding="utf-8")

            groundrecall_root = tmp_path / "groundrecall"
            groundrecall_root.mkdir()
            (groundrecall_root / "groundrecall_query_bundle.json").write_text(
                json.dumps(
                    {
                        "concept": {"concept_id": "concept::topic", "title": "GroundRecall Topic"},
                        "summary": "Grounded summary.",
                        "claims": [{"claim_id": "clm-1", "claim_text": "Claim one", "claim_kind": "summary"}],
                    }
                ),
                encoding="utf-8",
            )

            didactopus_root = tmp_path / "didactopus"
            didactopus_root.mkdir()
            (didactopus_root / "pack.yaml").write_text("name: test-pack\ndisplay_name: Test Pack\n", encoding="utf-8")
            (didactopus_root / "concepts.yaml").write_text(
                "concepts:\n  - id: prior\n    title: Prior\n    description: Previous knowledge.\n    prerequisites: []\n",
                encoding="utf-8",
            )

            citegeist_root = tmp_path / "citegeist"
            citegeist_root.mkdir()
            (citegeist_root / "refs.bib").write_text(
                """@article{smith2024,\n  title = {A Study},\n  author = {Smith, Jane and Roe, John},\n  year = {2024}\n}\n""",
                encoding="utf-8",
            )

            doclift_cards = load_doclift_cards(doclift_root)
            groundrecall_cards = load_groundrecall_cards(groundrecall_root)
            didactopus_cards = load_didactopus_cards(didactopus_root)
            citegeist_cards = load_citegeist_cards(citegeist_root)

            self.assertEqual(doclift_cards[0].title, "Legacy Document")
            self.assertEqual(doclift_cards[0].body, "First paragraph.")
            self.assertEqual(groundrecall_cards[0].title, "GroundRecall Topic")
            self.assertEqual(groundrecall_cards[1].title, "Claim one")
            self.assertEqual(didactopus_cards[0].title, "Prior")
            self.assertEqual(citegeist_cards[0].title, "A Study")

    def test_inline_config_cards_can_seed_example_content(self) -> None:
        cards = cards_from_config(
            [
                {
                    "title": "Foundation Search",
                    "body": "Corpus-aware search entry point.",
                    "href": "/search/",
                    "meta": "workbench",
                    "link_label": "Search",
                }
            ],
            default_kind="feature",
        )

        self.assertEqual(cards[0].title, "Foundation Search")
        self.assertEqual(cards[0].kind, "feature")
        self.assertEqual(cards[0].href, "/search/")
        self.assertEqual(cards[0].meta, "workbench")
        self.assertEqual(cards[0].link_label, "Search")

    def test_build_site_renders_selected_theme_and_content(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            content_root = tmp_path / "content"
            content_root.mkdir()

            doclift_root = content_root / "doclift"
            doclift_root.mkdir()
            (doclift_root / "manifest.json").write_text(
                json.dumps({"documents": [{"document_id": "doc-1", "title": "Legacy Document", "markdown_path": "documents/doc-1/document.md"}]}),
                encoding="utf-8",
            )
            (doclift_root / "documents" / "doc-1").mkdir(parents=True)
            (doclift_root / "documents" / "doc-1" / "document.md").write_text("Doclift content.", encoding="utf-8")

            didactopus_root = content_root / "didactopus"
            didactopus_root.mkdir()
            (didactopus_root / "pack.yaml").write_text("name: test-pack\ndisplay_name: Test Pack\n", encoding="utf-8")
            (didactopus_root / "concepts.yaml").write_text(
                "concepts:\n  - id: prior\n    title: Prior\n    description: Previous knowledge.\n    prerequisites: []\n",
                encoding="utf-8",
            )

            groundrecall_root = content_root / "groundrecall"
            groundrecall_root.mkdir()
            (groundrecall_root / "groundrecall_query_bundle.json").write_text(
                json.dumps({"concept": {"concept_id": "concept::topic", "title": "GroundRecall Topic"}, "summary": "Grounded summary."}),
                encoding="utf-8",
            )

            citegeist_root = content_root / "citegeist"
            citegeist_root.mkdir()
            (citegeist_root / "refs.bib").write_text(
                """@article{smith2024,\n  title = {A Study},\n  author = {Smith, Jane and Roe, John},\n  year = {2024}\n}\n""",
                encoding="utf-8",
            )

            config = {
                "lang": "en",
                "title": "TalkOrigins Preview",
                "site_title": "TalkOrigins Archive",
                "license": "CC BY-SA 4.0",
                "github_url": "https://example.invalid",
                "contact_email": "admin@example.invalid",
                "theme": "talkorigins-modern",
                "languages": [{"code": "en", "name": "English"}],
                "navigation": [{"label": "Home", "href": "/"}],
                "hero": {
                    "kicker": "Archive Preview",
                    "title": "Modernized, reviewable, and still archive-first.",
                    "lede": "Proof-of-concept output from SciSiteForge.",
                    "actions": [{"label": "Open", "href": "#overview", "primary": True}],
                },
                "content_sources": {
                    "doclift_bundle": str(doclift_root),
                    "groundrecall_bundle": str(groundrecall_root),
                    "didactopus_pack": str(didactopus_root),
                    "bibliography": str(citegeist_root),
                },
            }
            config_path = tmp_path / "site.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            out_dir = tmp_path / "out"
            result = build.build_site(config_path, out_dir)

            html = (out_dir / "index.html").read_text(encoding="utf-8")
            self.assertEqual(result["theme"], "talkorigins-modern")
            self.assertIn("TalkOrigins Preview", html)
            self.assertIn("Legacy Document", html)
            self.assertIn("GroundRecall Topic", html)
            self.assertIn("Prior", html)
            self.assertIn("A Study", html)
            self.assertTrue((out_dir / "theme" / "assets" / "toa.ico").exists())

    def test_build_site_keeps_planned_languages_visible_and_generates_translation_artifacts(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = {
                "lang": "en",
                "title": "TalkOrigins Preview",
                "site_title": "TalkOrigins Archive",
                "license": "CC BY-SA 4.0",
                "github_url": "https://example.invalid",
                "contact_email": "admin@example.invalid",
                "theme": "talkorigins-modern",
                "languages": [
                    {"code": "en", "name": "English", "coverage": True},
                    {"code": "es", "name": "Español", "coverage": False},
                    {"code": "fr", "name": "Français", "coverage": False},
                ],
                "language_policy": {
                    "planned_languages": [
                        {"code": "es", "name": "Español"},
                        {"code": "fr", "name": "Français"},
                    ]
                },
                "navigation": [{"label": "Home", "href": "/"}],
                "hero": {
                    "kicker": "Archive Preview",
                    "title": "Modernized, reviewable, and still archive-first.",
                    "lede": "Proof-of-concept output from SciSiteForge.",
                    "actions": [{"label": "Open", "href": "#overview", "primary": True}],
                },
                "content_sources": {},
            }
            config_path = tmp_path / "site.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            out_dir = tmp_path / "out"
            result = build.build_site(config_path, out_dir)

            html = (out_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn('<select id="lang-switch"', html)
            self.assertIn('value="es"', html)
            self.assertIn('value="fr"', html)
            self.assertIn('id="scisiteforge-shell-i18n"', html)
            self.assertIn("Multilingual access", html)
            self.assertIn("Language options remain visible in the shared site shell", html)
            self.assertIn("Target languages under consideration: Español, Français", html)

            queue_html = (out_dir / "translation-status" / "index.html").read_text(encoding="utf-8")
            queue_json = json.loads((out_dir / "translation-status" / "queue.json").read_text(encoding="utf-8"))
            report_md = (out_dir / "build" / "site_regression_report.md").read_text(encoding="utf-8")
            guardrail_json = json.loads((out_dir / "build" / "public_surface_guardrails.json").read_text(encoding="utf-8"))

            self.assertIn("Translation Queue", queue_html)
            self.assertIn("Current translation status", queue_html)
            self.assertEqual(queue_json["schema"], "scisiteforge.translation_queue.v1")
            self.assertEqual(queue_json["default_language"], "en")
            self.assertEqual(result["regression_summary"]["failed"], 0)
            self.assertIn("Passed:", report_md)
            self.assertIn("Public Surface Guardrails", report_md)
            self.assertEqual(guardrail_json["schema"], "scisiteforge.public_surface_guardrails.v1")
            self.assertGreaterEqual(guardrail_json["counts"]["html_pages"], 2)

    def test_public_surface_audit_reports_structural_metadata_errors(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            page = tmp_path / "index.html"
            page.write_text(
                """<!doctype html>
<html lang="en">
<head>
  <title>Example</title>
  <meta name="description" content="Example page">
  <link rel="canonical" href="https://example.org/">
  <link rel="canonical" href="https://example.org/duplicate">
</head>
<body>Example</body>
</html>
""",
                encoding="utf-8",
            )

            report = audit_public_surface({"base_url": "https://example.org"}, tmp_path)

            self.assertEqual(report["summary"]["errors"], 1)
            self.assertEqual(report["findings"][0]["code"], "duplicate_canonical")

    def test_build_site_localizes_shared_shell_strings_for_current_language(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = {
                "lang": "es",
                "title": "Vista previa",
                "site_title": "Evolución",
                "license": "CC BY-SA 4.0",
                "github_url": "https://example.invalid",
                "contact_email": "admin@example.invalid",
                "theme": "evo-edu",
                "languages": [
                    {"code": "en", "name": "English", "coverage": True},
                    {"code": "es", "name": "Español", "coverage": True},
                ],
                "navigation": [
                    {"label": "Home", "href": "/"},
                    {"label": "Roadmap", "href": "#roadmap"},
                ],
                "hero": {
                    "kicker": "Vista previa",
                    "title": "Superficie compartida",
                    "lede": "Comprobación de traducción de la interfaz común.",
                    "actions": [{"label": "Abrir", "href": "#overview", "primary": True}],
                },
                "content_sources": {},
            }
            config_path = tmp_path / "site.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            out_dir = tmp_path / "out"
            build.build_site(config_path, out_dir)

            html = (out_dir / "index.html").read_text(encoding="utf-8")
            self.assertIn(">Inicio</a>", html)
            self.assertIn(">Hoja de ruta</a>", html)
            self.assertIn("aria-label=\"Idioma\"", html)
            self.assertIn(">Tema</strong>", html)
            self.assertIn(">Idioma</strong>", html)

    def test_build_site_generates_notebook_page_when_notebooks_are_configured(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config = {
                "lang": "en",
                "title": "Notebook Preview",
                "site_title": "Evolution Education",
                "license": "CC BY-SA 4.0",
                "github_url": "https://example.invalid",
                "contact_email": "admin@example.invalid",
                "theme": "evo-edu",
                "languages": [
                    {"code": "en", "name": "English", "coverage": True},
                    {"code": "es", "name": "Español", "coverage": False},
                ],
                "navigation": [{"label": "Home", "href": "/"}],
                "hero": {
                    "kicker": "Notebook",
                    "title": "Concept notebook",
                    "lede": "Study modules and source-grounded explanations.",
                    "actions": [{"label": "Explore", "href": "#overview", "primary": True}],
                },
                "content_sources": {},
                "notebooks": [
                    {
                        "id": "first-ring",
                        "title": "First Ring Concepts",
                        "summary": "Core evolution ideas for beginners.",
                        "audience": "self-learners",
                        "goals": ["Build population-level reasoning about evolution"],
                        "apps": [{"title": "Allele Tracker", "href": "/apps/allele-tracker/", "description": "Population change sandbox"}],
                        "source_kinds": ["notebook"],
                    }
                ],
            }
            config_path = tmp_path / "site.json"
            config_path.write_text(json.dumps(config), encoding="utf-8")

            out_dir = tmp_path / "out"
            result = build.build_site(config_path, out_dir)

            notebook_html = (out_dir / "notebook" / "index.html").read_text(encoding="utf-8")
            self.assertIn("Notebook", notebook_html)
            self.assertIn("Goals", notebook_html)
            self.assertIn("Apps and Labs", notebook_html)
            self.assertIn("First Ring Concepts", notebook_html)
            self.assertEqual(result["regression_summary"]["failed"], 0)

    def test_notebook_pattern_groups_goals_apps_and_source_cards(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            doclift_root = tmp_path / "doclift"
            doclift_root.mkdir()
            (doclift_root / "manifest.json").write_text(
                json.dumps(
                    {
                        "documents": [
                            {
                                "document_id": "doc-1",
                                "title": "Legacy Reading",
                                "document_kind": "article",
                                "markdown_path": "documents/doc-1/document.md",
                            }
                        ]
                    }
                ),
                encoding="utf-8",
            )
            (doclift_root / "documents" / "doc-1").mkdir(parents=True)
            (doclift_root / "documents" / "doc-1" / "document.md").write_text("Recovered source paragraph.", encoding="utf-8")

            config = {
                "notebooks": [
                    {
                        "id": "digital-evolution",
                        "title": "Digital Evolution Notebook",
                        "summary": "Lab plus source-grounded study path.",
                        "audience": "self-learners",
                        "goals": ["Connect simulation output to evolutionary concepts"],
                        "apps": [{"title": "Avida-ED", "href": "/app4/", "description": "Digital evolution lab"}],
                        "source_kinds": ["notebook"],
                    }
                ]
            }
            notebooks = load_notebooks(config)
            content = SiteContent(section_cards=load_doclift_cards(doclift_root))
            html = render_notebooks(notebooks, content)

            self.assertIn("Digital Evolution Notebook", html)
            self.assertIn("Avida-ED", html)
            self.assertIn("Legacy Reading", html)
            self.assertIn("Recovered source paragraph.", html)

    def test_geniehive_translator_uses_openai_compatible_chat_payload(self) -> None:
        translator = GenieHiveTranslator(
            TranslationConfig(base_url="http://geniehive.local:8800", model="translation-role", api_key="abc123")
        )
        captured: dict[str, object] = {}

        def fake_post_json(path: str, payload: dict) -> dict:
            captured["path"] = path
            captured["payload"] = payload
            return {"choices": [{"message": {"content": "Hola"}}]}

        translator._post_json = fake_post_json  # type: ignore[method-assign]
        result = translator.translate("Hello world", "Spanish", {"evolution": "evolución"})

        self.assertEqual(result, "Hola")
        self.assertEqual(captured["path"], "/v1/chat/completions")
        payload = captured["payload"]
        self.assertEqual(payload["model"], "translation-role")
        user_text = payload["messages"][1]["content"]
        self.assertIn("Spanish", user_text)
        self.assertIn("evolución", user_text)

    def test_geniehive_translator_uses_geniehive_api_key_header(self) -> None:
        translator = GenieHiveTranslator(
            TranslationConfig(base_url="http://geniehive.local:8800", model="translation-role", api_key="abc123")
        )
        captured: dict[str, object] = {}

        class FakeResponse:
            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc, tb):
                return False

            def read(self):
                return b'{"choices":[{"message":{"content":"Hola"}}]}'

        def fake_urlopen(req, timeout):
            captured["headers"] = dict(req.header_items())
            captured["timeout"] = timeout
            return FakeResponse()

        with patch("scisiteforge.translations.request.urlopen", fake_urlopen):
            self.assertEqual(translator.translate("Hello", "Spanish"), "Hola")

        headers = captured["headers"]
        self.assertEqual(headers["X-api-key"], "abc123")
        self.assertNotIn("Authorization", headers)

    def test_translate_site_builds_translator_from_config(self) -> None:
        from tempfile import TemporaryDirectory

        with TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            config_path = tmp_path / "site.json"
            config_path.write_text(
                json.dumps(
                    {
                        "translation": {
                            "base_url": "http://geniehive.local:8800",
                            "model": "translation-role",
                            "api_key": "abc123",
                            "timeout": 33,
                            "system_prompt": "Translate carefully.",
                        }
                    }
                ),
                encoding="utf-8",
            )
            args = SimpleNamespace(base_url=None, model=None, api_key=None, timeout=None)
            translator = translate_site.build_translator(config_path, args)

            self.assertEqual(translator.config.provider, "geniehive")
            self.assertEqual(translator.config.base_url, "http://geniehive.local:8800")
            self.assertEqual(translator.config.model, "translation-role")
            self.assertEqual(translator.config.api_key, "abc123")
            self.assertEqual(translator.config.timeout, 33)


if __name__ == "__main__":
    unittest.main()
