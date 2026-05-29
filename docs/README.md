# Root Docs

This folder is ready for public documentation.

## Tools

| Tool | Purpose |
| --- | --- |
| [Blog Website Maker](tools/blog-website-maker.md) | Agent playbook for turning "please make me a blog website" into a small Astro or Jekyll Markdown blog. |
| [Blog Article Editor](tools/blog-article-editor.md) | Agent playbook for loading an existing article, grilling the human on the real point, and rewriting safely. |

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/create_blog_site.py` | Creates the first Astro blog scaffold, including `/theme-preview/`. |
| `scripts/create_jekyll_blog_site.py` | Creates the first Jekyll blog scaffold, including `/theme-preview/`. |
| `scripts/plan_blog_assets.py` | Creates a licence-safe image plan with search links and attribution fields. |
| `scripts/prepare_blog_article_edit.py` | Creates a grill/rewrite worksheet from an existing Markdown article. |
