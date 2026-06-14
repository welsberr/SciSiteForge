# SciSiteForge Notebook Seeding Model

This document describes how to start a broader Notebook from an existing
Notebook without turning the two into unmanaged forks.

The immediate use case is:

- seed a Foundation Notebook from the current `evo-edu` Notebook
- allow both to continue evolving as new sources are ingested
- preserve a clean path for later synchronization

## Short Answer

Yes, it is reasonable to clone the `evo-edu` Notebook now for Foundation use.

But it should be treated as a seeded derivative, not as a casually duplicated
copy that will somehow be reconciled later by hand.

## Recommended Model

Use this pattern:

1. identify the current `evo-edu` science-core concept set
2. seed the Foundation Notebook from that set
3. preserve shared identifiers wherever possible
4. mark Foundation-only additions explicitly
5. plan later synchronization at the graph/artifact level, not by comparing
   rendered pages

This keeps the Notebook usable now without pretending the final broader
Foundation graph is already complete.

## What the Seed Should Include

The seed should usually include:

- core concept IDs
- concept titles
- relation structure
- maturity state
- public/scaffold artifact links
- learning-path membership where relevant
- source/grounding status metadata

In other words, copy the structured Notebook artifacts, not merely the prose
pages.

## Preserve Stable IDs

The most important rule is:

- preserve shared concept IDs and relation IDs where possible

If the Foundation Notebook starts with renamed or regenerated IDs for the same
concepts, later synchronization becomes needlessly difficult.

Shared concepts should continue to look like the same concepts across both
Notebook lines.

## Shared Versus Local Ownership

After seeding, explicitly divide concepts into two classes.

### Shared Core

These remain part of the science core that came from `evo-edu`, for example:

- allele frequency change
- genetic drift
- natural selection
- mutation
- adaptation
- speciation
- common descent
- population thinking

These should normally continue to track upstream improvements from the
`evo-edu` line unless intentionally promoted to a new broader canonical layer.

### Foundation-Local Expansion

These are concepts that belong to the broader Foundation growth around the core,
for example:

- science education
- church-state separation
- argument from incredulity
- legal precedent in anti-evolution cases
- philosophy-of-science bridge concepts

These can grow locally in the Foundation Notebook without forcing changes back
into the `evo-edu` Notebook.

## What to Record at Seeding Time

When the Foundation Notebook is first seeded, record:

- the source Notebook bundle or version
- the concept set included in the seed
- the path bundles included in the seed
- the date of the seed
- the ownership rule for shared versus local concepts

This should be treated as lineage metadata, not an informal assumption.

## How Later Updates Should Work

When both Notebook lines have evolved and more sources have been ingested:

- import updated shared-core artifacts from the `evo-edu` line
- compare by concept ID and relation ID
- merge changes into the Foundation Notebook graph or artifact store
- keep Foundation-local concepts separate unless they are intentionally promoted

Do not treat rendered HTML pages as the merge surface.

The merge surface should be:

- graph artifacts
- scaffold artifacts
- learning-path artifacts
- maturity metadata

## What to Avoid

Avoid this pattern:

- duplicate the current Notebook pages
- let both copies drift independently
- later try to reconcile them by eye

That produces:

- duplicated concepts with inconsistent wording
- unclear source of truth
- broken path logic
- unnecessary editorial merge work

## Practical Rule of Thumb

Use this rule:

- clone now if it helps site development move forward
- treat the clone as a seeded derivative with lineage
- keep shared concepts structurally shared
- let new Foundation domains expand around that core

This allows the broader Foundation Notebook to begin now, even though the
Notebook ecosystem is still expanding.
