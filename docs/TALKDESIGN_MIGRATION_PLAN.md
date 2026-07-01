# TalkDesign Migration Plan

This document captures a review of the `poc3.talkorigins.org`
modernization pattern and a migration plan for the sister site
`talkdesign.org`.

The goal is not to merge TalkDesign into TalkOrigins. The goal is to give
TalkDesign the same static, route-preserving, reviewable modernization
pipeline while keeping a distinct site identity for Intelligent Design-focused
material.

## Source Review

### TalkOrigins poc3 Pattern

The current `poc3.talkorigins.org` candidate demonstrates the right operating
model for old Foundation-associated sites:

- keep legacy routes stable where possible
- convert article pages into a responsive reading shell
- promote index/menu pages into generated navigation surfaces
- strip repeated legacy page chrome into a shared header and footer
- exclude unavailable dynamic routes unless they are replaced by managed
  modern surfaces
- expose corpus-aware search, feedback, translation status, workbench review,
  and Notebook paths as explicit public surfaces
- mark provenance with route/content-kind metadata in generated pages

The successful design correction in poc3 is that landing pages are no longer
just legacy tables inside a new wrapper. The root page, FAQ browser, FAQ Q/A
page, section pages, site outline, alphabetical index, and claim index are
being treated as reader-task surfaces. That is the pattern TalkDesign should
reuse.

### TalkDesign Corpus Shape

Local source tree inspected:

- `/path/to/talkdesign.org`
- approximately 1,633 files under `public_html`
- major visible surfaces:
  - legacy root pages such as `index.html`, `tdo.html`, `introfaq.html`,
    `articles.html`, `faq2002.html`, `aboutus.html`, `submissions.html`,
    and `volunteers.html`
  - article/FAQ pages under `faqs/`
  - captured Drupal-style static routes under `cs/`
  - legacy PHP/PostNuke/Drupal files under `pn/`, `cs/`, and root-level PHP
    paths
  - legacy image/CSS assets in `images/`, `extras/`, `cs/themes/`, and
    `cs/misc/`

The public site currently has two different historical front doors:

- `https://www.talkdesign.org/` uses the older table-based `Talkdesign.org`
  shell with banner imagery and three-column navigation.
- `https://www.talkdesign.org/cs/` uses a Drupal-era `TalkDesign` shell with
  sidebars, taxonomy links, user/login surfaces, RSS, and node pages.

That split should be resolved into one modern root experience while preserving
important old paths as canonical or redirecting legacy duplicates to canonical
static equivalents.

## Recommended Identity

Use the `talkorigins-modern` theme family as the base so Foundation-associated
sites feel related, but give TalkDesign a restrained palette shift.

Recommended TalkDesign palette:

```css
:root {
  --bg: #f1f4f1;
  --panel: #fffdf8;
  --panel-warm: #f8f4ea;
  --panel-cool: #eef5f3;
  --ink: #1c2422;
  --muted: #5d6863;
  --line: rgba(28, 36, 34, 0.13);
  --blue: #276064;
  --blue-deep: #163f43;
  --blue-soft: #d7e8e6;
  --gold: #a8742a;
  --gold-soft: #f1dfba;
  --brick-soft: #eadfdb;
}
```

This keeps the scholarly warm-paper feel of TalkOrigins but shifts the main
accent from archive blue to teal-green, which fits TalkDesign's analytical
identity without drifting into a separate design language.

Site copy should use:

- site title: `TalkDesign`
- kicker: `intelligent design analysis archive`
- concise summary: `Static archive and reviewed paths for criticism of
  Intelligent Design claims, arguments, and public controversy.`

## Migration Strategy

### 1. Create a Site-Specific Modernization Repo

Follow the repo model in `docs/SITE_REPOS.md`.

Recommended repo name:

- `talkdesign-modern`

It should own:

- TalkDesign source inventory
- route map and canonicalization decisions
- conversion script
- TalkDesign-specific theme override
- public output tree
- deployment wrapper
- regression checks
- review/workbench queue exports

SciSiteForge should own only reusable improvements discovered during the
migration.

### 2. Inventory Routes and Decide Canonicals

Build a route inventory from `public_html`.

Classify each route as:

- `article`: long-form FAQ/article content
- `landing`: root, articles, FAQ, about, volunteer, submissions, and section
  pages
- `drupal_node`: static captured `/cs/<slug>/index.html` article pages
- `taxonomy`: `/cs/taxonomy_menu/*`, `/cs/taxonomy/*`, and related menus
- `mail_archive`: `tdomail/*`
- `asset`: images, CSS, PDF, JS, text downloads
- `dynamic_unavailable`: executable PHP/PostNuke/Drupal routes with no static
  public replacement
- `duplicate_or_query_snapshot`: files/directories encoding `?q=` or
  `index.php?q=...` variants of cleaner canonical routes

Initial canonical policy:

- preserve clean static routes such as `/introfaq.html`, `/faqs/flagellum.html`,
  `/faqs/naturalism.html`, and `/cs/welcome/`
- canonicalize `/cs/index.php?q=welcome` to `/cs/welcome/`
- canonicalize `/cs/?q=...` variants to the clean `/cs/<slug>/` route when a
  clean route exists
- preserve PDFs under their current paths
- exclude executable internals such as `/pn/*.php`, login/register/user
  mutation routes, search forms, aggregator feeds that are not static pages,
  and database/config files
- replace taxonomy/menu pages with generated static navigation where useful

### 3. Build the First Modern Surfaces

Start with a small public candidate, equivalent to TalkOrigins poc3:

- `/` root landing page
- `/articles.html` or generated `/articles/` article browser
- `/introfaq.html`
- `/faqs/introfaq.html`
- `/faqs/flagellum.html`
- `/faqs/flagellum_background.html`
- `/faqs/naturalism.html`
- `/faqs/demskiscompass.html`
- `/faqs/Evolving_Immunity.html`
- `/cs/` modern landing for the Drupal-era content
- `/cs/welcome/`
- `/cs/td_faq/`
- `/cs/taxonomy_menu/2/` as generated article/category navigation
- `/search/`
- `/translation-status/`
- `/workbench/`

This seed set covers both historical shells and the highest-value Intelligent
Design critique content before doing a full-tree conversion.

### 4. Convert Page Types

Use the TalkOrigins conversion lessons directly:

- landing routes should render directly in the site shell, not inside narrow
  article wrappers
- repeated table/sidebar navigation should be extracted into generated cards
  and link lists
- article routes should keep author/date/provenance front matter where present
- legacy sidebars should become either page-local related links or generated
  browser surfaces, not duplicated on every page
- legacy comments, login/register forms, search blocks, and feed widgets should
  be removed unless there is a managed replacement
- malformed encodings in older root pages should be normalized to UTF-8 during
  conversion
- image assets should be copied when they are content-bearing, but spacer GIFs
  and layout-only images should be stripped

### 5. Generate Navigation Surfaces

Do not hand-maintain the old menu pages.

Generate:

- root decision cards: FAQ, Articles, ID concepts, authors/series, sister sites
- article index from titles and route inventory
- FAQ browser from `/faqs/*`
- `/cs/` article browser from clean Drupal slugs
- taxonomy/category pages from captured taxonomy routes where recoverable
- sitemap from the canonical route inventory
- duplicate-route report for query snapshots and PHP aliases

### 6. Search and Notebook Integration

Give TalkDesign its own corpus in the Foundation search model.

Suggested search corpora:

- `talkdesign_articles`
- `talkdesign_faqs`
- `talkdesign_drupal_archive`
- `talkorigins_claims`
- `talkorigins_archive`
- `pandasthumb_archive`

Suggested Notebook seeds:

- `Intelligent Design Overview`
- `Irreducible Complexity and the Flagellum`
- `Specified Complexity and Dembski`
- `Naturalism, Methodology, and Science`
- `Dover/ID Public Controversy`

Each Notebook should link back to stable TalkDesign pages, relevant
TalkOrigins claim entries, and Foundation search results.

### 7. Regression Checks

Minimum checks for the candidate:

- build output contains no executable `.php`, `.cgi`, `.pl`, `.plx`, or
  config/database files
- no public link points to internal dynamic mutation routes such as login,
  register, admin, user password, or PostNuke modules
- all canonical seed routes return HTTP 200 locally
- duplicate query routes either redirect or are excluded from public navigation
- generated pages include `scisiteforge:theme`, legacy-route, and content-kind
  metadata
- root, `/articles`, `/faqs`, and `/cs` landing pages have no narrow article
  wrapper
- article pages keep readable max-width and do not retain old table chrome
- spacer/layout images are not referenced from generated article bodies
- search index excludes assets and unavailable dynamic pages
- translation queue is generated for planned languages but does not imply
  completed coverage

### 8. Deployment Candidate

Recommended first candidate hostname:

- `poc1.talkdesign.org`

After the seed set is acceptable:

- expand to all canonical static routes
- add generated route reports and workbench review queue
- run public HEAD checks for seed and high-value routes
- compare old and modern pages route-by-route before switching production

## Implementation Notes

Keep this split:

- reusable shell, translation, Notebook, and regression features go into
  `SciSiteForge`
- TalkDesign route conversion, duplicate handling, old Drupal/PostNuke cleanup,
  and deployment belong in `talkdesign-modern`

The work should start as an archive modernization and not as a full redesign.
The strongest parts of the TalkOrigins poc3 approach are provenance,
route-preservation, and progressive replacement of generated surfaces. Those
should remain the engineering constraints for TalkDesign.
