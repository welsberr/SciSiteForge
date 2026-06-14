# SciSiteForge Scripts

For a real public site, read `docs/ADOPTION_GUIDE.md` before using these
scripts. The build scripts assume the site repo already has a source inventory,
public/private boundary decisions, Notebook plan, language policy, and route
policy. Skipping that preparation usually produces a site shell without a
maintainable content model.

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

Build all shipped example configs:

```bash
python3 scripts/build_examples.py
```

That writes example outputs under `examples/_build/` by default and runs the
normal framework regression surface for each example bundle.

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
