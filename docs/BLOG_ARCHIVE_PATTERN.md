# Blog and Stable Archive Pattern

SciSiteForge can support sites that need both stable knowledge-graph-backed
archive pages and blog-centric posts. The goal is not to turn every post into a
permanent reference article. The goal is to let dated posts and durable archive
records reinforce each other without confusing their roles.

## Content Modes

Use four related content modes.

### Blog Post

A dated publication unit.

Use for:

- announcements
- commentary
- responses to current events
- release notes
- short research updates
- progress reports

Recommended fields:

- `post_id`
- `title`
- `slug`
- `published_at`
- `updated_at`
- `authors`
- `summary`
- `body`
- `tags`
- `related_topics`
- `source_artifacts`
- `citation_ids`
- `review_status`

### Topic Page

A durable explanatory page that can be revised over time.

Use for:

- concepts
- claim families
- recurring controversies
- evidence summaries
- resource guides

Recommended fields:

- `topic_id`
- `canonical_url`
- `title`
- `summary`
- `concept_ids`
- `claim_ids`
- `related_posts`
- `notebook_id`
- `citation_bundle`
- `search_corpora`
- `review_status`

### Notebook Page

A guided route through source material, concepts, citations, and apps.

Use for:

- learning paths
- claim-to-evidence paths
- source-document context
- concept clusters
- classroom or self-study routes

Recommended fields:

- `notebook_id`
- `audience`
- `goals`
- `source_artifacts`
- `concept_ids`
- `claim_ids`
- `apps`
- `related_reading`
- `citation_bundle`
- `public_safety_status`

### Source Record

A provenance record for a document, post, citation, file, transcript, scan, or
external resource.

Use for:

- source attribution
- copyright/licensing review
- citation resolution
- search indexing
- knowledge graph extraction
- public/private boundary decisions

Recommended fields:

- `source_id`
- `source_type`
- `canonical_url`
- `external_url`
- `title`
- `authors`
- `published_at`
- `license_status`
- `public_use_policy`
- `derived_records`
- `review_status`

## Knowledge Graph Relationship

Blog posts can mention claims, concepts, citations, people, organizations, and
source documents. Those links should enter the knowledge graph as reviewable
relations, not as hidden page text.

For example:

- a blog post responds to a current anti-science claim
- that post links to a stable claim record
- the claim record links to source instances and rebuttals
- the Notebook page gives a guided reader path
- the bibliography page lists citations and BibTeX
- search indexes each record in the appropriate corpus

This keeps the post timely while the archive remains durable.

## Recommended Routes

Use routes that make publication mode clear:

- `/blog/` for dated posts
- `/topics/` for durable topic pages
- `/notebook/` for guided study surfaces
- `/bibliography/` or content-specific bibliography routes for citations
- `/search/` for public corpus search
- `/workbench/` for review queues

Some sites may keep legacy routes, such as `/faqs/` or `/indexcc/`. In that
case, preserve those routes and add blog/topic/notebook routes around them
rather than forcing legacy content into a new URL scheme.

## Editorial Workflow

1. Draft or ingest the blog post.
2. Link it to source records, concepts, claims, and citations.
3. Generate search documents for the post and related records.
4. If the post creates durable value, add or update a topic page or Notebook
   page.
5. Queue citation and source-link enrichment.
6. Queue translation only after the page is stable enough for public use.
7. Publish through the normal static release process.

## Search Corpus Guidance

Keep blog and archive corpora separate:

- `site.blog.post`
- `site.topic`
- `site.notebook`
- `site.source`
- `site.bibliography.citation`

This lets readers search only dated commentary, only stable explanations, or
all public material together.

## Translation Guidance

Blog posts and archive pages have different translation priorities. Translate:

- site shell and navigation first
- durable topic and Notebook pages next
- high-value blog posts after that
- low-value dated posts only when needed

Use the same terminology compendium for both post and archive translation so a
reader does not see different technical terms in adjacent content.

## Public Safety

Blog systems often carry drafts, comments, spam, moderation metadata, and
private editorial notes. Do not export those into public static builds.

For converted blog archives, explicitly decide whether comments are:

- public historical content
- moderated public content
- private review material
- excluded entirely

If comments are preserved, index them as their own corpus or content type so
they do not blur with authorial article text.
