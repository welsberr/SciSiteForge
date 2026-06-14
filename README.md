# SciSiteForge

A lightweight, responsive, static-site framework for open educational resources in science.

## 🎯 Purpose
This repository provides a reusable foundation for sites like **evo-edu.org**, `www2.talkorigins.org`, and `pandasthumb.net`, featuring:
- Mobile-first responsive design
- Modular content loading (HTML fragments)
- Language-switching support for multilingual static trees
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
- TalkOrigins Foundation Notebook planning for static review surfaces over
  GroundRecall, doclift, Didactopus, CiteGeist, and wolfe artifacts. See
  [docs/FOUNDATION_NOTEBOOK.md](docs/FOUNDATION_NOTEBOOK.md)
- Public-surface guardrails for scoped updates, canonical metadata, JSON-LD,
  search corpora, bibliography preservation, portable builds, performance
  checks, and archive/status separation. See
  [docs/PUBLIC_SURFACE_GUARDRAILS.md](docs/PUBLIC_SURFACE_GUARDRAILS.md)
- Optional translation tooling can use local GenieHive LLM endpoints. See
  [docs/GENIEHIVE_TRANSLATION.md](docs/GENIEHIVE_TRANSLATION.md)

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
1. Clone this repo
2. Choose a theme preset and optional content sources in `site.json`
3. Build with `scripts/build.py`
4. Use `main.js` for dynamic section loading and language switching

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
between covered locales without requiring a translation backend. Optional
translation tooling can use locally-hosted multilingual large language models
routed through GenieHive; see
[docs/GENIEHIVE_TRANSLATION.md](docs/GENIEHIVE_TRANSLATION.md) for that
separate client-side configuration.

This came together in a hurry, but I hope that other people may find
some utility in it to aid in disseminating domain knowledge they and
their collaborators may have.

Wesley R. Elsberry, 2025-10-14
