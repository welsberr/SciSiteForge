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
