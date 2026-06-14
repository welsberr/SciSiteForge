# SciSiteForge Notebooks

A SciSiteForge notebook is a topic-level study module. It is smaller than a
full learner application and more structured than a list of cards.

For public-facing reader experience patterns, see
[docs/NOTEBOOK_UX.md](NOTEBOOK_UX.md).
For the expandable graph and maturity model behind incomplete-but-usable
Notebook coverage, see [docs/NOTEBOOK_GRAPH.md](NOTEBOOK_GRAPH.md).

Use a notebook when a site needs to connect:

- a concept or claim
- one or more interactive apps or labs
- recovered source documents
- grounded knowledge and provenance
- guided-study concepts
- citations or bibliography updates

## Role in the Ecosystem

The notebook pattern is intentionally generic:

- `doclift` rescues and normalizes legacy documents.
- `GroundRecall` provides grounded concepts, claims, observations, and
  provenance.
- `Didactopus` provides learner-facing concepts, prerequisites, pathways, and
  review-oriented packs.
- `CiteGeist` provides bibliography and literature-update material.
- SciSiteForge renders a static site shell that can present those artifacts in
  a coherent topic module.

SciSiteForge should not take over the job of those systems. It should render
their outputs in a predictable static format.

## Notebook Shape

In a site config, a notebook looks like this:

```json
{
  "notebooks": [
    {
      "id": "evidence-and-claims",
      "title": "Evidence and Claims Notebook",
      "summary": "Connect claims, evidence, source material, and citations.",
      "audience": "self-learners and instructors",
      "goals": [
        "Move from a claim to relevant evidence",
        "Expose provenance and review status",
        "Connect source documents to guided study"
      ],
      "apps": [
        {
          "title": "Public search",
          "href": "/search/",
          "description": "Search across related corpora"
        }
      ],
      "source_kinds": ["section", "notebook", "app", "bibliography"],
      "max_items": 8
    }
  ]
}
```

The build system renders each notebook as:

- title and summary
- audience note
- goals
- app/lab links
- selected study material from loaded content sources

## Content Sources

Notebook study material is selected from the loaded `content_sources`.

Recommended mapping:

- `doclift_bundle`: recovered legacy readings and source documents
- `groundrecall_bundle`: concepts, claims, observations, and provenance
- `didactopus_pack`: guided concepts and prerequisite structure
- `bibliography`: CiteGeist bibliography entries

The first implementation uses the existing card stream and filters by
`source_kinds`. That keeps the model simple while preserving room for richer
notebook manifests later.

## evo-edu.org Pattern

For evo-edu.org, notebooks should frame a learning pathway around:

- an app or lab, such as Avida-ED or an ecology/fitness landscape tool
- the concept sequence needed to use the tool well
- common misconceptions and review prompts
- source readings or curriculum fragments
- bibliography support for instructors or deeper learners

This supports the current evo-edu direction: lab, atlas, and guided study in
one coherent site.

## TalkOrigins Pattern

For the TalkOrigins modernization proof-of-concept, notebooks should frame:

- a claim or topic
- relevant Index to Creationist Claims entries
- stable Archive articles
- Panda's Thumb or TalkDesign context when appropriate
- bibliography updates and provenance

This fits the static/dynamic split: stable archive material remains stable,
while notebook pages can provide a modern guided route through it.

## Panda's Thumb Pattern

For Panda's Thumb, notebooks should work as topic dossiers:

- a recurring topic or controversy
- MT-era authoritative posts where available
- scraped-corpus posts for later years
- related Index to Creationist Claims material
- citations and source trails

The notebook should identify provenance clearly when the same topic is covered
by multiple corpora.

## Design Rule

Keep notebooks static, reviewable, and source-aware. If a workflow needs
learner state, mastery ledgers, evaluator behavior, or interactive mentoring,
that belongs in Didactopus. SciSiteForge should publish the durable study
surface.
