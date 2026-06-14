# SciSiteForge

A lightweight, responsive, static-site framework for open educational resources in science.

## 🎯 Purpose
This repository provides a reusable foundation for science, education, and
public-knowledge sites. It is being proven through sites such as
**evo-edu.org**, `talkorigins.org`, `talkdesign.org`, `evolutionnews.net`, and
`pandasthumb.net`, but the framework is intended for broader reuse, featuring:
- Mobile-first responsive design
- Modular content loading (HTML fragments)
- Language-switching support for multilingual static trees, including visible planned-language options and fallback behavior when translations are still pending
- Public search, workbench, feedback, bibliography, portable static build, and
  Notebook patterns that can be implemented in site repos while sharing the
  SciSiteForge shell conventions
- Integrated app-card and notebook-section templates
  - Intended to host JavaScript web apps
    -- With study guides, alignment documents, reading (links to notebook sections)
- Bibliography rendering (journal style + BibTeX)
- Multiple theme presets, including:
  - `evo-edu`
  - `talkorigins-modern`
  - `pandasthumb`
- Optional content bridges for `doclift`, `GroundRecall`, `Didactopus`, and `CiteGeist`
- A generic notebook pattern for topic-level study modules that combine goals,
  apps, source-derived sections, and bibliographies. See
  [docs/NOTEBOOKS.md](docs/NOTEBOOKS.md)
- Recommended public-facing Notebook UX patterns for beginner routes, concept
  pages, learning-path presentation, and trust/status cues. See
  [docs/NOTEBOOK_UX.md](docs/NOTEBOOK_UX.md)
- Recommended graph maturity model for expandable Notebook coverage across
  evolving domains. See [docs/NOTEBOOK_GRAPH.md](docs/NOTEBOOK_GRAPH.md)
- Recommended seeding/synchronization model for cloning the `evo-edu` Notebook
  into broader Foundation Notebook work. See
  [docs/NOTEBOOK_SEEDING.md](docs/NOTEBOOK_SEEDING.md)
- Recommended repo boundary and lifecycle model for framework-versus-site
  ownership. See [docs/SITE_REPOS.md](docs/SITE_REPOS.md)
- TalkDesign sister-site migration plan following the `talkorigins-modern`
  poc3 modernization pattern. See
  [docs/TALKDESIGN_MIGRATION_PLAN.md](docs/TALKDESIGN_MIGRATION_PLAN.md)
- TalkOrigins Foundation Notebook planning for static review surfaces over
  GroundRecall, doclift, Didactopus, CiteGeist, and wolfe artifacts. See
  [docs/FOUNDATION_NOTEBOOK.md](docs/FOUNDATION_NOTEBOOK.md)
- New-project orientation for maintainers who need to prepare source material,
  configure Notebook early, and decide which features belong in a site repo.
  See [docs/ADOPTION_GUIDE.md](docs/ADOPTION_GUIDE.md)
- Blog-to-archive publication model for projects that need dated posts and
  stable knowledge-graph-backed topic pages. See
  [docs/BLOG_ARCHIVE_PATTERN.md](docs/BLOG_ARCHIVE_PATTERN.md)
- Public-surface guardrails for scoped updates, canonical metadata, JSON-LD,
  search corpora, bibliography preservation, portable builds, performance
  checks, and archive/status separation. See
  [docs/PUBLIC_SURFACE_GUARDRAILS.md](docs/PUBLIC_SURFACE_GUARDRAILS.md)
- Optional translation tooling can use local GenieHive LLM endpoints. See
  [docs/GENIEHIVE_TRANSLATION.md](docs/GENIEHIVE_TRANSLATION.md)
- Framework-generated translation queue and status pages under `translation-status/`
- Framework-generated build regression reports under `build/site_regression_report.{json,md}`

## 🛠️ Features
- Vanilla HTML/CSS/JS (no heavy frameworks)
- Lazy-loaded sections for performance
- Accessible navigation and UI
- Offline-compatible (no external dependencies)
- Bibliography content per section/subsection
  - Based on Bibtex
  - Renders to a journal style ('Evolution' is the sole style so far)
  - Loads bibliography from host on demand  

## 📂 Structure
```
/framework
├── theme/              # Shared assets plus theme presets
│   └── themes/        # Shipped theme variants
├── templates/          # Reusable HTML snippets
├── docs/               # Usage guide and examples
├── scripts/            # Language translation script and example glossary 
└── LICENSE             # MIT License
```

## 🧩 How to Use
1. Read [docs/ADOPTION_GUIDE.md](docs/ADOPTION_GUIDE.md) before starting a real site.
2. Create a site repo and source-content inventory.
3. Choose a theme preset and optional content sources in `site.json`.
4. Provision Notebook manifests early so source review, search, bibliography,
   translation, and reader paths are coordinated.
5. Build with `scripts/build.py`.
6. Use `main.js` for dynamic section loading and language switching.

Example configs:
- [examples/talkorigins-modern.site.json](examples/talkorigins-modern.site.json)
- [examples/evo-edu-notebook.site.json](examples/evo-edu-notebook.site.json)

Build all shipped examples with:

```bash
python3 scripts/build_examples.py
```

Build output now includes, when configured:
- `index.html`
- `notebook/index.html` for notebook-mode study surfaces
- `translation-status/index.html`
- `translation-status/queue.json`
- `build/site_regression_report.json`
- `build/site_regression_report.md`

> Use the `talkorigins-modern` preset as the proving ground for the
> `www2.talkorigins.org` modernization line.

## 📜 License
MIT — free to use, modify, and redistribute.

## AI Disclosure

This code and documentation was primarily provided by Alibaba's Qwen3 Max generative AI model with prompting by Wesley R. Elsberry.

## Comments

I've run web sites since 1995, and some of the most fraught and trying
times I've experienced are when a site gets hacked due to
vulnerabilities in dynamic content. So one goal here is to provide
content that is responsive and looks to some extent dynamic, while the
content itself is in static files that have no modification due to
operations in the website itself. I hope this reduces the attack
surface considerably, and also should make it easier to simply restore
from a good backup in case of a problem and carry on. The bibliography
is meant to be targeted to topics, but not require a database to
obtain the correct bibliography items to display.  Content folding
with lazy-loading aims to prevent pages from growing in size without
bound, and provide modularity in collaboration. Models, programs, and
simulations are meant to be implemented in a browser friendly form,
either JavaScript, WebGL, or similar, so that processing takes place
client-side, preventing heavy loads on servers. The current model of
content I am pursuing with this is to have a site landing page, a
collection of web apps for a topic, and a 'notebook' on that topic
that includes didactic material sufficient to ground a naive user in
the relevant concepts that the models, programs, and simulations
address.

The other major feature here is the architecture to support multiple
languages. The core framework can present static language trees and switch
between covered locales without requiring a translation backend. Planned
languages can remain visible in the shared site shell, while untranslated
pages fall back to the default language together with a translation-status
queue that makes the pending work explicit. Optional translation tooling can
use locally-hosted multilingual large language models routed through
GenieHive; see
[docs/GENIEHIVE_TRANSLATION.md](docs/GENIEHIVE_TRANSLATION.md) for that
separate client-side configuration.

This came together in a hurry, but I hope that other people may find
some utility in it to aid in disseminating domain knowledge they and
their collaborators may have.

Wesley R. Elsberry, 2025-10-14
