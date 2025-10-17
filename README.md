# SciSiteForge

A lightweight, responsive, static-site framework for open educational resources in science.

## 🎯 Purpose
This repository provides a reusable foundation for sites like **evo-edu.org**, featuring:
- Mobile-first responsive design
- Modular content loading (HTML fragments)
- Language-switching support (for multilingual sites)
- Integrated app-card and notebook-section templates
  - Intended to host Javascript web apps
    -- With study guides, alignment documents, reading (links to notebook sections)
- Bibliography rendering (journal style + BibTeX)

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
├── theme/              # Base layout, CSS, JS
├── templates/          # Reusable HTML snippets
├── docs/               # Usage guide and examples
├── scripts/            # Language translation script and example glossary 
└── LICENSE             # MIT License
```

## 🧩 How to Use
1. Clone this repo
2. Copy `/theme/base.html` into your content project
3. Customize navigation and styling
4. Use `main.js` for dynamic section loading

> See [`evo-edu/en`](https://evo-edu.org/en) for a working example.

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
either Javascript, WebGL, or similar, so that processing takes place
client-side, preventing heavy loads on servers. The current model of
content I am pursuing with this to to have a site landing page, a
collection of web apps for a topic, and a 'notebook' on that topic
that includes didectic material sufficient to ground a naive user in
the relevant concepts that the models, programs, and simulations
address.

The other major feature here is the architecture to support multiple
languages. Because my efforts are currently down to one developer, me,
this is accomplished by use of one or more locally-hosted multilingual
large language models that can automaticlly provide decent translation
from a source language to a target language. In my case, the source
language will be English, I have a Python program for a batch offline
process to traverse the site directory tree, open and parse HTML
files, ask for translations at the paragraph level, and assemble those
back into the same HTML structure in order to obtain each translated
page. Each page will incorporate the language switcher Javascript code
in its header, which amounts to redirecting the user to a copy of the
site whose static files are in the target language. The translation
is to be done via an LLM running locally via Mozilla Llamafile.

This came together in a hurry, but I hope that other people may find
some utility in it to aid in disseminating domain knowledge they and
their collaborators may have.

Wesley R. Elsberry, 2025-10-14

