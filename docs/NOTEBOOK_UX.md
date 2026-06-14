# SciSiteForge Notebook UX Patterns

This document captures public-facing Notebook patterns that emerged from
walkthrough review of beginner-oriented science sites. These are not tied to a
single site. They are recommended presentation conventions for any SciSiteForge
Notebook surface that aims to teach, not merely to expose artifacts.

## Core Principle

A Notebook should feel like a readable study surface first and a structured
artifact bundle second.

SciSiteForge can publish machine-readable artifacts beside the public pages,
but the reader should encounter:

- a clear front door
- an obvious next step
- concept pages that stand on their own
- visible trust/status cues
- lateral navigation that keeps the reader inside the Notebook

## Recommended Public Surface

When a site uses Notebook mode, the public-facing surface should usually
include:

- a Notebook landing page
- an overview or introduction page
- a concept index
- a learning-path page
- a source-trails or grounding-status page
- direct concept pages that load the shared site shell and stylesheet

The framework should keep the machine-readable artifacts public, but those
artifacts should sit behind reader-facing pages rather than acting as the main
entry point.

## Beginner Hospitality

If the Notebook is meant for new learners, provide a clear beginner route.

Recommended pattern:

- a `Start here` block on the landing page
- a brief introduction that explains the subject in plain language
- a short ordered route through the first few concept pages
- direct links to the next step in that route

The first fifteen minutes should be obvious. A new reader should not have to
infer where to begin from a concept index or a JSON path artifact.

## Learning-Path Presentation

A path page should not be only a list of artifacts or concept IDs.

For each step, prefer to show:

- the concept title
- why this step comes now
- what the learner should understand afterward
- a direct `Read this next` link

This keeps the path usable for ordinary readers while preserving its value as a
machine-readable sequencing artifact for Didactopus and related tools.

## Concept Page Pattern

Concept pages should be complete documents, not bare fragments.

Recommended elements:

- concise summary
- one or more concrete worked examples
- related concept links
- source-trail or grounding-status note
- a short retention block such as `If you remember only three things`

Where possible, lead with the learner's question rather than system language
about scaffolds, bundles, or review infrastructure.

## Trust and Source Status

If citations or translations are incomplete, show that honestly in ways that
help a reader decide how to use the page.

Helpful language tends to look like:

- good for learning now
- conceptually strong, bibliography still growing
- exploratory or still under review

Status should guide reader expectations, not merely expose workflow state.

## Cross-Cutting Threshold Concepts

Some ideas are not just ordinary concept pages. They organize how several other
pages should be read.

Examples:

- population thinking
- null-model reasoning
- evidence versus interpretation

When these threshold ideas matter, promote them explicitly:

- mention them across related concept pages
- consider giving them their own concept page
- place them deliberately in beginner routes or learning paths

## Generic Versus Editorial Responsibilities

These UX patterns are partly framework-level and partly site-level.

Framework-level support should include:

- stable public page locations
- shared shell/navigation
- consistent theming for direct concept pages
- translation-state UI
- export and regression surfaces

Editorial/site-level work still decides:

- the actual beginner route
- concept ordering
- retention summaries
- examples and analogies
- threshold concepts worth promoting

SciSiteForge should make these choices easy to publish consistently, but it
should not hard-code the content decisions themselves.
