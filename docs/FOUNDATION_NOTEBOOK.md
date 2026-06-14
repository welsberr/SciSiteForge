# TalkOrigins Foundation Notebook

The Foundation Notebook is the reviewable study and evidence surface for
TalkOrigins Foundation sites. It should not become a new canonical knowledge
store. SciSiteForge should render static notebook pages from artifacts produced
by the adjacent tools.

For the graph-backed maturity model that allows the Notebook to be useful
before complete domain coverage exists, see
[docs/NOTEBOOK_GRAPH.md](NOTEBOOK_GRAPH.md).
For the recommended procedure for seeding a broader Foundation Notebook from
the `evo-edu` core without creating unmanaged forks, see
[docs/NOTEBOOK_SEEDING.md](NOTEBOOK_SEEDING.md).

## Roles

- `doclift`: normalize legacy documents and produce deterministic source
  bundles, chunks, figures, tables, and provenance sidecars.
- `GroundRecall`: own grounded claims, concepts, observations, relations,
  graph diagnostics, review queues, provenance, and promoted knowledge.
- `Didactopus`: own learner-facing packs, prerequisites, pathways, review and
  mastery workflows, and dynamic learner state when needed.
- `CiteGeist`: own bibliography ingestion, citation normalization, DOI/source
  enrichment, BibTeX-style exports, and literature-update workflows.
- `wolfe`: own large-corpus ingestion and search, including Library science
  context, source metadata, reference candidates, concept candidates, and
  public/private search corpora.
- `SciSiteForge`: render static notebook surfaces over these artifacts for
  public preview, editorial review, and low-risk deployment.

## Static-First Boundary

Public Foundation sites should serve static notebook pages and static data
assets wherever possible. Runtime services should be limited to features that
need them, such as public search. Privileged research, full corpora, review
queues, and generated graph evidence should remain on the development host or
other non-public infrastructure.

## Public Release Safety

Notebook publication should be deny-by-default. Public bundles may contain
reviewed learning pages, reviewed scaffold data, public citations, source
summaries, and short attributed quotations where a review record justifies the
use. They must not contain raw source extraction or private review state.

Exclude these from public artifacts:

- staging claims, draft examples, and draft questions
- raw OCR, local scan output, source-text dumps, and extraction chunks
- local filesystem paths and local scan/OCR locators
- model prompts, model logs, batch generation traces, and intermediate drafts
- unresolved source-slot analysis, review queues, and workbench state
- learner account/session state, mastery ledgers, and private mentor logs

For records derived from copyrighted source material, require source-use review
metadata before promotion:

- copyright/licensing status when known
- source citation and canonical source ID
- whether the public text is summary, paraphrase, or quotation
- verbatim quotation word count
- transformation/relevance rationale
- market-substitution risk note
- reviewer and review date

SciSiteForge deployments should enforce this boundary mechanically. Public
artifact exporters should allowlist reviewed Notebook paths, deny known private
paths, and fail the export when public Notebook files contain raw OCR/source
markers or local path markers.

## Artifact Inputs

A Foundation Notebook page can be assembled from:

- a typed content record, such as an Index to Creationist Claims entry,
  bibliography topic, jargon term, article, feedback item, or resource page
- a `GroundRecall` query bundle for the relevant concept, claim, or topic
- `GroundRecall` graph diagnostics and candidate relation review state
- a `doclift` bundle containing recovered legacy source material
- a `CiteGeist` bibliography bundle or topic export
- a `Didactopus` pack or pathway when learner-facing review is relevant
- `wolfe` search-context exports or corpus metadata for supporting research

The page should retain links back to canonical artifact IDs and source paths so
reviewers can inspect provenance without treating rendered HTML as canonical.

## Content-Type Pattern

Each TalkOrigins Foundation content type should emit a notebook-compatible
manifest:

- `content_id`
- `content_type`
- `canonical_url`
- `legacy_urls`
- `title`
- `summary`
- `language`
- `status`
- `source_artifacts`
- `groundrecall_bundle`
- `citation_bundle`
- `related_content`
- `search_corpora`
- `review_queues`

The initial high-priority content types are:

- `talkorigins.article`
- `talkorigins.indexcc.claim`
- `talkorigins.bibliography.topic`
- `talkorigins.bibliography.citation`
- `talkorigins.jargon.term`
- `talkorigins.biographica.person`
- `talkorigins.feedback.item`
- `talkorigins.links.resource`
- cross-domain records from Panda's Thumb, TalkDesign, evo-edu, and related
  Foundation sites

## Search Corpora

Search documents should be emitted by content type rather than scraped from
rendered pages. This avoids duplicated matches where an Index claim appears as
both its own record and as incidental text inside a broader page.

Recommended corpus labels:

- `talkorigins.article`
- `talkorigins.indexcc.claim`
- `talkorigins.bibliography.topic`
- `talkorigins.bibliography.citation`
- `talkorigins.jargon.term`
- `talkorigins.biographica.person`
- `talkorigins.feedback.item`
- `talkorigins.links.resource`
- `pandasthumb.article`
- `evoedu.resource`

Public search should use public-safe corpora. The full Foundation Notebook can
also reference privileged research corpora and the wolfe Library `science`
index on the development host.

## Knowledge Graph Use

GroundRecall's current graph adoption plan is the right boundary:

- extracted relations are candidates, not facts
- raw SPO triples are not canonical truth
- chunk IDs and source provenance must be preserved
- concept aliases and relation suggestions should enter review queues
- graph diagnostics should identify orphan concepts, disconnected components,
  noisy clusters, unsupported claims, and bridge concepts

SciSiteForge should render approved or reviewable graph context, not promote
graph facts itself.

## Translation Guidebook

The Notebook should support terminology review across all Foundation sites:

- collect technical terms with source contexts
- generate candidate translations for the target languages
- detect terms with multiple plausible translations
- preserve approved, alternate, and rejected translations per language
- link terminology decisions back to source examples and reviewer notes

This guidebook should be used by static renderers and translation workflows so
multilingual pages remain consistent across content types and domains.

## Initial Implementation Path

1. Generate notebook-compatible manifests for Index to Creationist Claims
   records, starting with the existing parser/artifact builder output.
2. Add a SciSiteForge content loader for those manifests or a generic
   `foundation_notebook` source kind.
3. Render a static claim notebook page that combines claim text, related Index
   entries, citation links, GroundRecall graph context, and wolfe search-context
   links.
4. Extend the same manifest shape to bibliography topics and jargon terms.
5. Keep review queues and full research corpora off the public deployment path;
   expose only static public artifacts and public-safe search documents.
