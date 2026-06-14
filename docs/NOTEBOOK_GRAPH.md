# SciSiteForge Notebook Graph Maturity Model

This document describes how Notebook development can proceed before conceptual
coverage is complete.

The core idea is:

- the Notebook does not need to be complete before it is useful
- a graph-backed Notebook can expand flexibly over time
- curated public paths should sit on top of an uneven but explicit graph

This is especially important when:

- `evo-edu.org` provides the initial science-learning core
- broader Foundation sites need additional domains such as philosophy,
  theology, education, law, history, rhetoric, and political science
- site development must begin before the full Notebook is finished

## Starting Core and Expanding Outward

The practical starting core is the `evo-edu` Notebook domain:

- evolutionary biology
- ecology
- evolutionary computation
- computational biology

From there, a broader Foundation Notebook can grow outward into adjacent and
cross-cutting domains:

- philosophy of science
- theology and religion
- education
- law
- political science
- history of science
- rhetoric and public controversy

The broader Notebook should usually start from the `evo-edu` conceptual core
rather than waiting for all domains to be equally mature.
For the repo/artifact procedure for doing that seeding safely, see
[docs/NOTEBOOK_SEEDING.md](NOTEBOOK_SEEDING.md).

## Why a Graph Helps

A graph-backed Notebook allows:

- new concepts to be inserted without rewriting the whole structure
- concepts to belong to more than one path or domain
- bridge concepts to connect otherwise distant areas
- path generation from current coverage instead of ideal final coverage
- known gaps to be represented explicitly instead of remaining silent

Examples of bridge or threshold concepts:

- population thinking
- evidence and inference
- argument from incredulity
- science education
- church-state separation

## Curated Paths on Top of the Graph

The graph should not be the reader experience by itself.

Public Notebook use still needs:

- beginner routes
- threshold concepts
- curated learning paths
- trust and grounding markers

So the model should be:

- graph underneath
- curated paths on top

The graph makes expansion flexible. The curated path makes reading coherent.

## Maturity States

Notebook nodes should be allowed to exist at different maturity levels.

Recommended states:

### `scaffold_only`

The concept is recognized and named, but not yet ready for public study use.

Typical characteristics:

- basic node identity exists
- relation candidates may exist
- no public page yet
- grounding may be incomplete

### `path_usable`

The concept can participate in internal or semi-public path generation even if
its public page is thin or absent.

Typical characteristics:

- prerequisite or bridge value is understood
- path placement is plausible
- may still rely on neighboring concepts for explanation

### `public_page_ready`

The concept has enough material to stand as a public page.

Typical characteristics:

- a public concept page exists
- summary and relation context are present
- source or scaffold status is visible
- the node can be linked directly from public Notebook routes

### `reviewed_core`

The concept is a stable part of the Notebook’s main explanatory surface.

Typical characteristics:

- public page is in regular use
- path role is clear
- grounding and terminology are reasonably stable
- good candidate for translation priority

### `cross_domain_bridge`

The concept is useful across multiple domains or site families.

Typical characteristics:

- connects two or more domain clusters
- likely to appear in more than one learning path
- may deserve special treatment as a threshold concept

`cross_domain_bridge` can coexist with another maturity state. It is a role as
well as a maturity signal.

## Minimum Node Metadata

To make incomplete expansion manageable, a Notebook concept node should
ideally carry:

- concept or node ID
- title
- domain or domains
- relation types to neighboring nodes
- maturity state
- grounding/review status
- public page present or absent
- scaffold present or absent
- path memberships
- downstream uses, if known

This allows sites to distinguish:

- what is ready for readers now
- what is usable for internal sequencing
- what is known but still immature

## Site Development Before Notebook Completion

A site such as `talkorigins-modern` should be allowed to use the Notebook
before the entire graph is complete.

That is safe if:

- gaps are explicit
- reviewed nodes are distinguishable from provisional nodes
- public paths avoid over-promising
- expansion does not require reworking the whole model

So the requirement is not “finish the Notebook first.” The requirement is:

- give the Notebook an explicit graph and maturity model

## Framework Boundary

`SciSiteForge` should support the publication of graph-aware Notebook surfaces,
but should not become the canonical graph store.

Recommended ownership split:

- `GroundRecall`: graph relations, grounding, provenance, review state
- `Didactopus`: path and learner-flow consumption
- `SciSiteForge`: static rendering of current Notebook maturity and curated
  paths

## Practical Guidance

Use this rule of thumb:

- add nodes early
- label their maturity honestly
- publish curated paths only from stable enough nodes
- let the graph expand as time and material become available

That makes first-use site development possible without pretending the Notebook
is finished.
