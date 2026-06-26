# GenieHive Translation Configuration

This guide covers the optional SciSiteForge translation path:

- `scripts/translate_site.py`
- the `translation` block in a SciSiteForge site config
- the GenieHive OpenAI-compatible chat endpoint used by the translator

The translator is intentionally separate from the static build path. It does
not own the translation model or routing policy. It reads site config, loads
optional glossaries, and sends paragraph-sized requests to GenieHive.

## Client-Side Configuration

SciSiteForge reads translation settings from the `translation` object in the
site config:

```json
{
  "translation": {
    "provider": "geniehive",
    "base_url": "http://172.24.50.65:8800",
    "model": "scientific_translator",
    "api_key": "change-me-client-key",
    "timeout": 120,
    "system_prompt": "You are a careful scientific translator. Preserve meaning, structure, and technical terms. Return only the translation."
  }
}
```

Recommended meaning of the fields:

- `base_url`: GenieHive control-plane URL or a reverse-proxied client URL. For the TalkOrigins proof-of-concept from `bwng.us`, use `http://172.24.50.65:8800`.
- `provider`: translation backend. The supported provider is currently
  `geniehive`.
- `model`: a GenieHive role ID or directly addressable model name.
- `api_key`: the GenieHive client key, sent as the `X-Api-Key` request header.
- `timeout`: request timeout in seconds.
- `system_prompt`: the translation policy for the client.

The CLI also accepts overrides:

- `--base-url`
- `--model`
- `--api-key`
- `--timeout`

Those flags override the site config for a single run.

## Request Shape

`scripts/translate_site.py` sends GenieHive a standard chat-completions request:

- `POST /v1/chat/completions`
- `model`: from the translation config
- `messages`: one system message plus one user prompt
- `temperature`: low, so translations stay stable

The user prompt asks for:

- translation into the target language
- no commentary
- preservation of structure and technical terminology

## Glossaries

If `scripts/glossary_<lang>.json` exists, the translator loads it and passes
the glossary entries into the prompt.

Use glossaries for:

- fixed technical terms
- proper names that should not be translated
- site-specific terminology

Keep each glossary small and explicit. The translator is not a terminology
database.

## Practical Workflow

1. Set the SciSiteForge `translation` block.
2. Confirm GenieHive is reachable at the configured `base_url`.
3. Confirm the selected GenieHive model or role exists.
4. Run `scripts/translate_site.py`.
5. Review the translated tree before publishing it.

For site-specific translation runs, keep the source tree and destination tree
separate. Translation should not overwrite the English source.

Automatically translated pages must carry a visible disclaimer before the page
content. SciSiteForge templates provide this as
`.translation-quality-disclaimer`, inserted after the site header and before
the main content. The generated page also carries
`<meta name="scisiteforge:translation-review" content="automated-unreviewed">`
until the translation has been reviewed.

The disclaimer appears when:

- the page language differs from the configured source language
- `translation.status` or `translation.review` is `automated` or
  `automated-unreviewed`
- `translation.automated` is `true`

Set `translation.source_language` when building a translated page. If no source
language is provided, SciSiteForge treats English as the source language. Set
`translation.feedback_url` when the site has a public feedback route; otherwise
the disclaimer falls back to the configured `contact_email`.

## Small Translation Fixes

Use a separate Spark patch mode for small, targeted translation corrections
when a full translation queue is already running or when updating the queue
state would be disproportionate to the correction.

This mode is for cases such as:

- a short homepage or shell phrase mistranslates badly in one or more
  languages
- the English source text needs a small wording change to avoid ambiguous
  translation
- a translated metadata, navigation, or footer string needs replacement across
  the generated language trees

Do not use the normal queue worker for this mode unless changing
`translation-status/queue.json` is intended. Queue workers often mark pages
complete, update lease state, or rewrite status artifacts as a side effect.

The expected process is:

1. Search GroundRecall first for prior site-specific Spark translation work and
   the current site convention.
2. Patch the source generator or source content first, so future rebuilds keep
   the corrected wording.
3. Create an isolated run directory under
   `build/translation-runs/<site>-spark-patch-YYYYMMDDTHHMMSSZ/`.
4. Save a prompt file and JSON Schema file in that directory.
5. Run Codex Spark directly and capture the model output in the same directory.
6. Apply the returned JSON with a deterministic script or reviewable manifest
   that touches only the intended generated fields.
7. Verify queue JSON parseability and, if a resilient queue is running, verify
   that its locks or leases were not changed.
8. Search the updated pages and generator for the rejected wording.
9. Save a GroundRecall source note with the run directory, command, fields
   touched, queue-isolation decision, and verification results.

The run directory should contain enough material for a maintainer to reproduce
or audit the correction:

- `prompt.md`
- `output-schema.json`
- `spark-output.json`
- `apply_<scope>.py` or an equivalent deterministic apply script
- `apply-manifest.json`

The apply manifest should explicitly record:

- `model`
- `queue_touched: false`
- updated files
- updated fields or selectors
- verification notes where practical

Example Spark invocation:

```bash
codex exec -m gpt-5.3-codex-spark \
  -C /path/to/site-repo \
  -s workspace-write \
  --output-schema build/translation-runs/site-spark-patch-YYYYMMDDTHHMMSSZ/output-schema.json \
  -o build/translation-runs/site-spark-patch-YYYYMMDDTHHMMSSZ/spark-output.json \
  - < build/translation-runs/site-spark-patch-YYYYMMDDTHHMMSSZ/prompt.md
```

Prompt constraints should be explicit for the failure being corrected. For
example, if a phrase translated into wording that implies censorship or
editorial suppression, list the forbidden meanings directly and ask Spark for
JSON only. Preserve site names, technical terms, and accepted glossary choices.

Minimum verification:

```bash
python3 -m json.tool build/translation-runs/site-spark-patch-YYYYMMDDTHHMMSSZ/spark-output.json
python3 -m json.tool public_html/translation-status/queue.json
python3 -m py_compile build/translation-runs/site-spark-patch-YYYYMMDDTHHMMSSZ/apply_scope.py
rg -n "rejected phrase|bad back-translation|source ambiguity" public_html/ path/to/generator.py
```

If the generated pages cannot be safely rebuilt without clobbering in-progress
translations, apply the targeted generated-page correction and document that
rebuild risk in the run manifest and GroundRecall note.

## Suggested Defaults

For local development:

- `base_url`: `http://127.0.0.1:8800`
- `model`: a translation-focused GenieHive role
- `timeout`: `120`

For the current ZeroTier-backed TalkOrigins proof-of-concept:

- `base_url`: `http://172.24.50.65:8800`
- `model`: `scientific_translator`
- `api_key`: `change-me-client-key`

For production or a LAN host:

- use the reverse-proxied GenieHive URL
- keep the API key required
- prefer a translation role with conservative prompt policy

## Relationship to Site Themes

Theme choice and translation are independent.

- themes control layout, styling, and rendering
- translation controls content generation for alternate language trees

Use the same translation setup across `evo-edu`, `talkorigins-modern`, and
`pandasthumb` unless a site has language-specific terminology that needs a
custom glossary or prompt.

For the TalkOrigins modernization proof-of-concept, keep the language switcher
in priority order rather than alphabetical order. A practical top-ten ordering
is:

1. Spanish
2. French
3. Portuguese
4. German
5. Italian
6. Russian
7. Chinese
8. Japanese
9. Arabic
10. Hindi

That order keeps the most broadly useful and generally stable translations near
the top of the chooser while still exposing the full target set.

Use the `coverage` flag on each language entry to decide what appears in the
main switcher. Keep the full intended list in `language_policy.planned_languages`
so the site can show the broader roadmap without advertising unfinished locales
as active.
