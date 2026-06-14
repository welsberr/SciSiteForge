# SciSiteForge Site Repo Model

This document describes how a real site should relate to `SciSiteForge`.

The short version is:

- `SciSiteForge` is the reusable framework repo
- each real public site should usually have its own repo
- bespoke content, editorial workflow, deployment logic, and local regression
  rules belong in the site repo, not in `SciSiteForge`

## Why Separate Site Repos Exist

The framework can be shared. The site plan usually cannot.

Even when two sites use the same shell, theme family, translation queue
mechanics, Notebook mode, and regression conventions, they still diverge in:

- corpus and source structure
- URL policy
- editorial standards and workflow
- modernization backlog
- deployment targets
- translation priorities
- app/tool integrations
- public UX choices

Trying to keep all of that inside `SciSiteForge` would turn the framework into
an accumulation point for site-local exceptions.

## Default Repository Split

Use this as the default model.

### `SciSiteForge`

Owns:

- shared static-site build logic
- theme presets and common shell behavior
- Notebook-mode support
- translation queue and fallback mechanics
- public-surface regression conventions
- reusable public-surface guardrail policy
- example configs and framework docs

Should not own:

- a specific site's editorial backlog
- site-local route inventory
- a site's deployment target and publishing wrappers
- corpus-specific review policy
- modernization queue state
- site-specific work maps

### Site Repo

Owns:

- the site plan
- `site.json` or equivalent build config
- content/notebook artifacts
- source bundles and review outputs
- local build/publish wrappers
- deployment docs
- site-specific regression checks
- site-specific scoped publish wrappers and warning thresholds
- theme overrides that are truly local
- editorial decision records and modernization queues

## What a New Site Repo Should Contain

At minimum, a site repo should usually have:

- a build config that targets `SciSiteForge`
- a short architecture/intent document
- deployment notes
- local regression checks or wrappers
- example publish command(s)
- content directories or pointers to source/review artifacts

For a Notebook-heavy site, also expect:

- learning paths
- concept pages or source-derived Notebook artifacts
- translation-status policy
- public UX notes or reader-route decisions

## Framework Dependency Models

There are several workable ways to consume `SciSiteForge`.

### 1. Copy/Vendor Snapshot

The site repo carries a local snapshot of framework code or generated outputs.

Pros:

- simple operationally
- easy to deploy in isolated environments

Cons:

- framework updates drift quickly
- harder to tell what is local override versus framework history

### 2. Git Subtree or Periodic Sync

The site repo periodically pulls framework updates in explicitly.

Pros:

- practical for teams that want a local copy but still want controlled upgrades
- upgrade events are visible and reviewable

Cons:

- still requires discipline around local modifications

### 3. Direct Dependency / Shared Checkout

The site repo depends on `SciSiteForge` as a separate checked-out framework.

Pros:

- cleanest conceptual split
- easiest to evolve the framework centrally

Cons:

- requires a clearer local build environment
- deployment wrappers need to know where the framework checkout lives

For your current projects, the practical architecture already resembles:

- `SciSiteForge`: framework repo
- `evo-edu.org`: site repo
- `talkorigins-modern`: site repo

That is the right direction.

## Upgrade Procedure

When a site repo wants a framework improvement:

1. Add or prove the improvement in `SciSiteForge`
2. Verify it with framework tests or example builds
3. Pull the change into the site repo through the chosen dependency model
4. Re-run the site-local build/publish/regression workflow
5. Keep any truly bespoke behavior in the site repo unless it is obviously
   reusable

This prevents site repos from becoming silent framework forks.

## What Should Be Generalized Upward

Move behavior into `SciSiteForge` when it is:

- theme-generic or multi-theme reusable
- needed by more than one site
- part of the shared build contract
- part of the shared translation/status contract
- part of the shared Notebook/public-surface model

Examples:

- language selector behavior
- translation fallback banner logic
- translation queue/status page generation
- generic Notebook page generation
- public-surface regression reporting
- shared guardrails for scoped updates, canonical metadata, search corpus
  contracts, portable artifacts, and performance audit categories

## What Should Stay Site-Local

Keep behavior in the site repo when it is:

- corpus-specific
- editorially specific
- tied to a site's actual URL policy
- tied to a site's work queue or modernization decisions
- uniquely useful to only one site

Examples:

- TalkOrigins-specific archive routes and case pages
- TalkOrigins bibliography source policy and exact route-class allowlists
- evo-edu beginner-route content and specific concept sequencing
- site-local source bundles and review artifacts
- deployment commands for a particular host tree

## Recommended Discipline

Use this rule of thumb:

- framework repo for reusable capabilities
- site repo for actual published identity and editorial reality

If a change feels necessary for two sites, it probably belongs in
`SciSiteForge`.

If a change depends on the meaning, backlog, audience, or corpus of one site,
it probably belongs in that site's repo.
