# Using SciSiteForge

## 1. Choose a Theme
Select one of the shipped presets under `/theme/themes/` and let the build
script materialize it into your site’s output tree.

## 2. Create Pages
Use the selected theme's `base.html` as a template. Replace `{{ }}` placeholders
with actual content.

## 3. Add Dynamic Behavior (Optional)
Include `/theme/main.js` for:
- Year auto-update
- Language switching

## 4. Customize Styling
Edit `style.css` to match your project’s visual identity.

## 5. Multilingual Support
- Organize content under `/en/`, `/es/`, etc.
- Update language switcher options in the theme template
- Translation generation is optional and separate from the static build path.
  See [GENIEHIVE_TRANSLATION.md](GENIEHIVE_TRANSLATION.md) for the optional
  GenieHive client settings and workflow.

## 6. Supported Presets and Bridges
- `evo-edu` for the learning-platform shell
- `talkorigins-modern` for the `www2.talkorigins.org` modernization proof-of-concept
- `pandasthumb` for the archive/news shell
- Content bridges for `doclift`, `GroundRecall`, `Didactopus`, and `CiteGeist`

## 7. Notebook Pattern
SciSiteForge notebooks are topic-level study modules. A notebook groups:

- goals and audience
- apps or labs
- source-derived sections from `doclift`, `GroundRecall`, and `Didactopus`
- bibliography entries from `CiteGeist`
- provenance-oriented links back to source material

Use notebooks when a site needs more than loose cards but does not need a full
learner application. The evo-edu instance can use this for digital evolution
study paths, while TalkOrigins can use the same pattern for claim-to-evidence
modules and Panda's Thumb can use it for topic dossiers.

See [NOTEBOOKS.md](NOTEBOOKS.md) for the generic notebook pattern and the
site-specific application notes.
