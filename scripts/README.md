# SciSiteForge Scripts

## Build

Initialize a site config:

```bash
cd /opt/www/dev/SciSiteForge
python3 scripts/build.py --init
```

Build a site:

```bash
python3 scripts/build.py --config site.json --output /tmp/scisiteforge-site
```

The shipped theme presets are:

- `evo-edu`
- `talkorigins-modern`
- `pandasthumb`

Use `talkorigins-modern` as the proving ground for the
`www2.talkorigins.org` modernization line.

## Translate

Translation is optional and separate from the static build. The current
translation provider is GenieHive through its OpenAI-compatible chat endpoint.

See `docs/GENIEHIVE_TRANSLATION.md` for the SciSiteForge client-side
configuration guide and the GenieHive repository's
`docs/translation_support.md` for the control-plane and node-side notes.

```bash
python3 scripts/translate_site.py \
  --config site.json \
  --langs es,fr \
  --src content/en \
  --dest content
```

Optional translation settings can be provided in the site config under
`translation`:

- `provider`
- `base_url`
- `model`
- `api_key`
- `timeout`
- `system_prompt`

The translator loads language glossaries from `scripts/glossary_<lang>.json`
when present.
