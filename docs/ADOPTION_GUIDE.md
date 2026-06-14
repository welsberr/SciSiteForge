# SciSiteForge Adoption Guide

SciSiteForge is meant to be a reusable framework for science, education, and
public-knowledge sites that need durable static publication plus selected
dynamic services. It should work for the TalkOrigins Foundation sites, but it
should not be limited to them.

Use this guide when starting a new site or converting an older site, blog,
archive, notebook, or document collection into a SciSiteForge-backed public
surface.

## What SciSiteForge Is For

SciSiteForge is a static-first site framework for projects that need:

- stable public pages that can be archived, mirrored, and restored easily
- responsive layouts and shared site shell behavior
- multilingual publication with visible translation status and fallback pages
- search over public corpora
- a workbench for review queues and editorial follow-up
- feedback routes that do not require the whole site to be dynamic
- bibliography and citation surfaces
- portable static builds for offline or USB distribution
- notebooks that connect content, source provenance, citations, and guided
  study

The framework should publish public-safe surfaces. It should not become the
private research database, learner-state system, or editorial backlog for a
specific site. Keep those in site repos or adjacent tools.

For mature archive migrations, read
[PUBLIC_SURFACE_GUARDRAILS.md](PUBLIC_SURFACE_GUARDRAILS.md) before designing
publish wrappers or rebuild workflows. It defines reusable SciSiteForge
expectations for scoped updates, canonical metadata, JSON-LD, search corpora,
bibliography preservation, portable builds, performance audits, and separation
between canonical archive pages and active operational surfaces.

## Recommended Starting Point

Start with a site repo, not with edits inside `SciSiteForge`.

The site repo should usually contain:

- a `site.json` build config
- source-content inventories and route policy
- content conversion scripts and review outputs
- site-specific theme overrides
- deployment notes and rollback procedure
- scoped update and publish policy
- search corpus definitions
- public-surface audit policy
- workbench queue policy
- feedback workflow notes
- translation glossary or terminology compendium
- Notebook manifests or generated Notebook artifacts

Use `SciSiteForge` for shared build behavior, theme presets, translation shell
logic, notebook rendering, and public-surface conventions. See
[SITE_REPOS.md](SITE_REPOS.md) for the repo boundary model.

## Feature Readiness Checklist

Before public deployment, decide which of these features your site needs.

### Multilingual Support

Declare language codes and native-language names in `site.json`. Planned
languages can be visible before every page is translated, but the fallback
behavior must be intentional:

- translated routes should serve the translated page
- missing translated routes should redirect to the default-language route
- the fallback page should show a message in the selected language
- the selected language preference should persist until the reader changes it
- translation-status pages should show page and, where possible, character
  progress

Use a technical phrase compendium early for projects with specialized terms.
This keeps translated terminology consistent across articles, notebooks, search
snippets, feedback pages, and bibliography summaries.

### Search

Treat search as a corpus feature, not just a rendered-page scrape. A mature
site usually needs separate corpora for different content classes, for example:

- articles or FAQs
- claim records
- bibliography topics and citation records
- glossary or jargon terms
- feedback archives
- blog posts
- Notebook topics
- sister-site or cross-domain material

Search documents should be generated from content records where possible. This
prevents duplicate and confusing results when one rendered page includes
navigation, related links, bibliography cards, and Notebook excerpts.

Search updates should be publishable as their own scope, with corpus manifests
and JSONL validation run before public deployment.

### Workbench

The workbench is for reviewable editorial work, not public page rendering.
Useful queues include:

- page conversion review
- translation review
- public feedback follow-up
- public mention monitoring
- broken-link or Archive.org replacement review
- citation enrichment review
- Notebook concept and provenance review
- claim/source evidence docket review

Keep private workbench data out of static public builds unless a specific
public artifact has been approved for publication.

### Feedback

A feedback route can be dynamic while the rest of the site remains static.
Plan:

- public feedback submission route
- moderation/review workflow
- static archive of past feedback, if the site has one
- styling that matches the public site shell
- accessibility cues that separate submitter text, responses, and metadata

### Bibliography

A SciSiteForge site can render bibliography topics and citations, but citation
quality depends on upstream preparation. For a serious bibliography, prepare:

- source bibliography provenance
- citation normalization
- DOI and source-link resolution
- open-access link discovery when available
- abstracts where appropriate and public-safe
- BibTeX exports
- review status for expanded or machine-matched entries

If the bibliography is expanded from an older source, the landing page should
explain the original source, retained attribution, and enrichment process.
Expanded bibliography pages should also have a route-class publish scope and
audit so unrelated rebuilds do not replace reviewed enriched output.

### Portable Static Build

A portable build is useful for review, classrooms, conferences, outreach, and
offline distribution. It should include only public-safe assets.

Plan for:

- static pages and assets
- offline-compatible search if needed
- translation fallback shims when no server routing is available
- stylesheet and script paths that work from local files
- a download landing page with OS-specific instructions
- versioned release filenames

Avoid bundling private workbench queues, raw source extraction, model logs, or
unreviewed Notebook source material.

### Dynamic App Routes

A static-first site can still have selected dynamic routes. The reusable route
pattern is:

- `/search` for search
- `/fb` for feedback
- `/workbench` for private/editorial review
- `/notebook` only when Notebook needs dynamic support; otherwise keep it
  static

Dynamic apps should use the same visual shell as the static site. For long-term
handoff, document their deployment, data directories, backups, and public/private
boundaries.

## Prepare Source Material Before Conversion

Most conversion problems come from weak source preparation. Before converting a
site, create a source inventory.

Record:

- canonical URL
- legacy URLs and aliases
- title and author attribution
- publication date when known
- content type
- source file or source system
- copyright/licensing status
- whether text can be quoted, summarized, paraphrased, or only linked
- figures, tables, and downloadable assets
- broken external links and Archive.org replacements
- related citations and bibliography records
- search corpus assignment
- translation priority
- review status

For legacy sites, also record which dynamic routes are unavailable and should be
removed, replaced, or reimplemented.

## Why Provision Notebook Early

Notebook should be provisioned early because it improves the rest of the site
preparation, even before public Notebook pages are complete.

Notebook planning forces the project to ask:

- What are the core concepts?
- What claims or questions recur?
- Which source documents support a reader path?
- Which citations belong near each topic?
- Which terms need translation consistency?
- Which pages are stable source material, and which are editorial guidance?
- What provenance can a reviewer inspect?
- Where are the gaps?

That work feeds better search, better bibliography grouping, better related
reading, better translation prompts, and better conversion reviews. The Notebook
is not just another page type. It is a coordination surface for source material,
knowledge graph records, citations, and public explanation.

## Notebook Preparation Workflow

For each topic or route, prepare a Notebook-compatible manifest with:

- topic or content ID
- canonical URL
- summary and intended audience
- source artifacts
- concept and claim links
- related pages
- citation bundle
- search corpus labels
- review status
- translation glossary terms
- public/private safety status

Use adjacent tools for their own jobs:

- `doclift` for recovered documents and source normalization
- `GroundRecall` for grounded concepts, claims, provenance, and graph review
- `Didactopus` for learner paths, prerequisites, and dynamic learning workflows
- `CiteGeist` for citation enrichment and bibliography exports
- search/indexing tools for public and private corpora

SciSiteForge should render reviewed artifacts. It should not silently promote
draft graph assertions, raw source extraction, or private review state.

## Blog-to-Archive Migration

Some projects need both a stable knowledge archive and ongoing blog-style
publication. Treat these as related but distinct content modes.

Use archive pages for:

- durable explanations
- reviewed topic pages
- claim or evidence records
- bibliographies
- notebooks and reading paths
- stable source-document pages

Use blog posts for:

- dated commentary
- announcements
- responses to current events
- progress reports
- release notes
- short updates that may later feed archive pages

Blog posts can still be knowledge-graph backed. The important distinction is
that the post remains a dated publication while concepts, citations, source
records, and claims can be linked into durable Notebook and archive records.

See [BLOG_ARCHIVE_PATTERN.md](BLOG_ARCHIVE_PATTERN.md) for the recommended
content model.

## Minimal Launch Sequence

For a small new site:

1. Create a site repo and `site.json`.
2. Pick a theme and language set.
3. Inventory source material and content types.
4. Define public/private boundaries.
5. Provision Notebook manifests for the first few topics.
6. Define search corpora.
7. Configure translation status and terminology compendium.
8. Build and run regression checks.
9. Deploy static pages through a staged release directory.
10. Add dynamic routes only where static output is insufficient.

For a large legacy migration:

1. Preserve a route inventory before conversion.
2. Convert a representative sample of each content type.
3. Run screenshot and responsive review against legacy where relevant.
4. Build Notebook and search manifests from source records, not from rendered
   pages alone.
5. Use workbench queues for conversion, translation, link repair, and citation
   review.
6. Deploy candidates under a preview route before promotion.
7. Promote through staged static releases with documented rollback.

## Handoff Expectations

A broader user base needs clean handoff. Each site should document:

- how to build
- how to run tests or regression checks
- how to deploy and roll back
- how translation queues are advanced
- how Notebook artifacts are reviewed
- how search corpora are generated
- where dynamic app data lives
- what must never be published

This is part of the framework discipline. A site that cannot be handed to
another maintainer is not ready for durable public service.
