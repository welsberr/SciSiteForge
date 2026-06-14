# Using SciSiteForge

For a real site, start with the broader project orientation in
[ADOPTION_GUIDE.md](ADOPTION_GUIDE.md). This usage page is the short build
workflow once the site owner has decided what source material, public/private
boundaries, Notebook surfaces, translation policy, and dynamic routes are in
scope.

## 1. Choose a Theme
Select one of the shipped presets under `/theme/themes/` and let the build
script materialize it into your site’s output tree.

## 2. Start from a Site Config
SciSiteForge is now primarily driven by a `site.json` config passed to
`scripts/build.py`.

Example configs:

- `examples/talkorigins-modern.site.json`
- `examples/evo-edu-notebook.site.json`

Build with:

```bash
python3 scripts/build.py --config examples/evo-edu-notebook.site.json --output out
```

The build writes the public surface and the framework-generated status
artifacts into the chosen output directory.

To build all shipped example configs at once:

```bash
python3 scripts/build_examples.py
```

That writes outputs under `examples/_build/` by default.

## 3. Add Dynamic Behavior (Optional)
Include `/theme/main.js` for:
- Year auto-update
- Language switching
- Translation fallback/status behavior for planned languages

## 4. Customize Styling
Edit `style.css` to match your project’s visual identity.

## 5. Multilingual Support
- Declare languages in `site.json`
- Use `coverage: true/false` to distinguish current versus planned locales
- Planned languages can remain visible in the shared shell while pages still
  fall back to the default language
- SciSiteForge generates:
  - `translation-status/index.html`
  - `translation-status/queue.json`
- Translation generation is optional and separate from the static build path.
  See [GENIEHIVE_TRANSLATION.md](GENIEHIVE_TRANSLATION.md) for the optional
  GenieHive client settings and workflow.

## 6. Supported Presets and Bridges
- `evo-edu` for the learning-platform shell
- `talkorigins-modern` for the `www2.talkorigins.org` modernization proof-of-concept
- `pandasthumb` for the archive/news shell
- Content bridges for `doclift`, `GroundRecall`, `Didactopus`, and `CiteGeist`

## 7. Notebook Pattern
SciSiteForge notebooks are topic-level study modules. A notebook groups:

- goals and audience
- apps or labs
- source-derived sections from `doclift`, `GroundRecall`, and `Didactopus`
- bibliography entries from `CiteGeist`
- provenance-oriented links back to source material

Use notebooks when a site needs more than loose cards but does not need a full
learner application. The evo-edu instance can use this for digital evolution
study paths, while TalkOrigins can use the same pattern for claim-to-evidence
modules and Panda's Thumb can use it for topic dossiers.

Provision Notebook early in a migration. Notebook manifests make the project
identify concepts, source documents, citation bundles, search corpora,
translation terminology, review status, and public/private boundaries before
those decisions become scattered across rendered pages.

See [NOTEBOOKS.md](NOTEBOOKS.md) for the generic notebook pattern and the
site-specific application notes. See [NOTEBOOK_UX.md](NOTEBOOK_UX.md) for the
recommended public-facing Notebook UX patterns.

## 8. Blog and Archive Sites

For projects moving from blogs or mixed publication systems, keep dated posts
and stable archive pages as related but distinct content modes. A post can link
to source records, concepts, citations, and Notebook pages without becoming the
canonical long-term topic page itself.

See [BLOG_ARCHIVE_PATTERN.md](BLOG_ARCHIVE_PATTERN.md) for the recommended
content model, routes, search corpora, and translation policy.

## 9. Site Repo Boundary
Use `SciSiteForge` as the framework repo, and keep real site plans in separate
site repos by default.

See [SITE_REPOS.md](SITE_REPOS.md) for:

- what belongs in the framework
- what belongs in a site repo
- how to pull framework improvements into sites
- when to keep behavior site-local instead of generalizing it upward

## 10. Build Outputs and Regression Surface
The framework build now produces more than a single HTML file. Depending on
configuration, expect:

- `index.html`
- `notebook/index.html`
- `translation-status/index.html`
- `translation-status/queue.json`
- `build/public_surface_guardrails.json`
- `build/site_regression_report.json`
- `build/site_regression_report.md`

These reports are part of the framework contract. They are meant to make
public-surface regressions visible during the build instead of only after
deployment.

`public_surface_guardrails.json` is a machine-readable audit report using the
`scisiteforge.public_surface_guardrails.v1` schema. It checks built HTML pages
for titles, descriptions, canonical links, JSON-LD validity, canonical/JSON-LD
URL consistency, active/process-surface separation, and basic search corpus
manifest/JSONL shape when a `search/corpora.json` manifest is present. The
Markdown regression report summarizes the guardrail error and warning counts.

For archive-scale sites, pair these reports with the reusable public-surface
guardrails in [PUBLIC_SURFACE_GUARDRAILS.md](PUBLIC_SURFACE_GUARDRAILS.md):
scoped updates, canonical and JSON-LD checks, search corpus validation,
bibliography preservation, portable artifact checks, and performance guardrails.

## 11. Dynamic Route Expectations

SciSiteForge keeps static pages as the default, but mature sites often need
dynamic app points. The common pattern is:

- `/search` for corpus-aware search
- `/fb` for feedback submission and moderation intake
- `/workbench` for private/editorial review queues
- `/notebook` only when the Notebook needs dynamic support; otherwise keep
  Notebook pages static

Dynamic apps should use the same visual shell and public/private boundary rules
as the static site. The deployment details belong in the site repo.
