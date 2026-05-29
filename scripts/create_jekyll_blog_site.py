#!/usr/bin/env python3
"""Create a small Jekyll Markdown blog scaffold."""

from __future__ import annotations

import argparse
import re
import shlex
from datetime import date
from pathlib import Path


SLUG_RE = re.compile(r"[^a-z0-9]+")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", required=True, type=Path, help="directory to create")
    parser.add_argument("--name", required=True, help="human-readable site name")
    parser.add_argument("--description", required=True, help="one-sentence site description")
    parser.add_argument("--subject", default="", help="short subject phrase")
    parser.add_argument("--slug", default="", help="package/site slug")
    parser.add_argument("--force", action="store_true", help="allow writing into an existing empty directory")
    args = parser.parse_args()

    target = args.target.expanduser().resolve()
    if target.exists() and any(target.iterdir()) and not args.force:
        raise SystemExit(f"Refusing to write into non-empty directory: {target}")

    site_name = args.name.strip()
    description = args.description.strip()
    subject = args.subject.strip() or site_name
    slug = clean_slug(args.slug or site_name)
    if not slug:
        raise SystemExit("Could not derive a safe slug")

    files = build_files(site_name=site_name, slug=slug, description=description, subject=subject)
    for relative_path, content in files.items():
        path = target / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    print(f"created Jekyll blog scaffold: {target}")
    print("next:")
    print(f"  cd {target}")
    print("  bundle install")
    print("  bundle exec jekyll build")
    print("  bundle exec jekyll serve")
    return 0


def build_files(*, site_name: str, slug: str, description: str, subject: str) -> dict[str, str]:
    today = date.today().isoformat()
    return {
        ".gitignore": """_site/
.jekyll-cache/
.sass-cache/
.bundle/
vendor/
.env
.env.*
""",
        "README.md": f"""# {site_name}

{description}

## Commands

```bash
bundle install
bundle exec jekyll serve
bundle exec jekyll build
```

Theme prototypes:

```text
/theme-preview/
```

Asset plan:

```bash
python3 scripts/plan_blog_assets.py --name {shell_quote(site_name)} --subject {shell_quote(subject)}
```

Posts live in:

```text
_posts/
```

Drafts live in:

```text
_drafts/
```
""",
        "Gemfile": """source "https://rubygems.org"

gem "jekyll", "~> 4.3"
gem "jekyll-feed", "~> 0.17"
gem "jekyll-seo-tag", "~> 2.8"
gem "webrick", "~> 1.8"
""",
        "_config.yml": f"""title: "{escape_yaml(site_name)}"
description: "{escape_yaml(description)}"
url: ""
baseurl: ""
permalink: /blog/:title/
markdown: kramdown
plugins:
  - jekyll-feed
  - jekyll-seo-tag
exclude:
  - README.md
  - Gemfile
  - Gemfile.lock
  - scripts/
""",
        "_layouts/default.html": f"""<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    {{% seo %}}
    <link rel="stylesheet" href="{{{{ '/assets/css/style.css' | relative_url }}}}">
  </head>
  <body>
    <header class="site-header">
      <nav aria-label="Primary">
        <a class="brand" href="{{{{ '/' | relative_url }}}}">{escape_html(site_name)}</a>
        <div class="nav-links">
          <a href="{{{{ '/blog/' | relative_url }}}}">Posts</a>
          <a href="{{{{ '/theme-preview/' | relative_url }}}}">Themes</a>
        </div>
      </nav>
    </header>
    <main>
      {{{{ content }}}}
    </main>
  </body>
</html>
""",
        "_layouts/post.html": """---
layout: default
---

<article class="post-page">
  <a class="back-link" href="{{ '/blog/' | relative_url }}">Back to posts</a>
  <h1>{{ page.title }}</h1>
  {% if page.tldr %}
    <p class="lede">{{ page.tldr }}</p>
  {% endif %}
  <div class="post-meta">{{ page.date | date: "%Y-%m-%d" }}</div>
  <div class="prose">
    {{ content }}
  </div>
</article>
""",
        "index.md": f"""---
layout: default
title: "{escape_yaml(site_name)}"
description: "{escape_yaml(description)}"
---

<section class="hero">
  <p class="eyebrow">Blog</p>
  <h1>{escape_html(site_name)}</h1>
  <p class="lede">{escape_html(description)}</p>
  <a class="button" href="{{{{ '/blog/' | relative_url }}}}">Read posts</a>
</section>

<section class="section">
  <h2>What This Is About</h2>
  <p>
    This site collects clear, practical writing about {escape_html(subject)}.
    It starts small: useful posts, plain language, and enough structure to keep
    writing easy to scan.
  </p>
</section>
""",
        "blog/index.html": """---
layout: default
title: Posts
---

<section class="page-title">
  <p class="eyebrow">Posts</p>
  <h1>Latest Writing</h1>
  <p class="lede">Each post has a TLDR so readers can scan before opening.</p>
</section>

<section class="post-list">
  {% for post in site.posts %}
    <article class="post-card">
      <a href="{{ post.url | relative_url }}">
        <span class="status">{{ post.date | date: "%Y-%m-%d" }}</span>
        <h2>{{ post.title }}</h2>
        {% if post.tldr %}
          <p>{{ post.tldr }}</p>
        {% endif %}
      </a>
    </article>
  {% endfor %}
</section>
""",
        "theme-preview.md": """---
layout: default
title: Theme Preview
description: Three quick visual directions for this blog.
permalink: /theme-preview/
---

<section class="page-title">
  <p class="eyebrow">Theme choice</p>
  <h1>Three directions</h1>
  <p class="lede">Pick the direction that feels closest. The site can keep one, combine parts, or ask for another three.</p>
</section>

<section class="theme-preview-grid" aria-label="Theme prototypes">
  <article class="theme-preview-card theme-field-guide">
    <p class="theme-label">Prototype 1</p>
    <h2>Field Guide</h2>
    <p>Practical, grounded, and useful. Good for teaching, nature, repair, field notes, and public-interest work.</p>
    <div class="theme-swatch-row"><span></span><span></span><span></span></div>
    <a href="{{ '/blog/' | relative_url }}">Read posts</a>
  </article>

  <article class="theme-preview-card theme-editorial">
    <p class="theme-label">Prototype 2</p>
    <h2>Editorial</h2>
    <p>More magazine-like. Good for public essays, stories, campaigning, opinion, and visual identity.</p>
    <div class="theme-swatch-row"><span></span><span></span><span></span></div>
    <a href="{{ '/blog/' | relative_url }}">Read posts</a>
  </article>

  <article class="theme-preview-card theme-notebook">
    <p class="theme-label">Prototype 3</p>
    <h2>Notebook</h2>
    <p>Quiet, direct, and low-friction. Good for personal notes, project logs, research, and frequent writing.</p>
    <div class="theme-swatch-row"><span></span><span></span><span></span></div>
    <a href="{{ '/blog/' | relative_url }}">Read posts</a>
  </article>
</section>
""",
        "assets/css/style.css": """html {
  color-scheme: light dark;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  line-height: 1.55;
}

body {
  margin: 0;
  color: CanvasText;
  background: Canvas;
}

a {
  color: inherit;
}

.site-header {
  border-bottom: 1px solid color-mix(in oklab, CanvasText 15%, transparent);
}

nav {
  max-width: 960px;
  margin: 0 auto;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  flex-wrap: wrap;
}

.brand {
  font-weight: 800;
  text-decoration: none;
}

.nav-links {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
}

main {
  max-width: 960px;
  margin: 0 auto;
  padding: 32px 20px 64px;
}

.hero,
.page-title,
.section,
.post-page {
  margin-bottom: 42px;
}

.eyebrow,
.status,
.post-meta {
  color: color-mix(in oklab, CanvasText 62%, transparent);
  font-size: 0.88rem;
  font-weight: 700;
  text-transform: uppercase;
}

h1 {
  max-width: 780px;
  margin: 8px 0 14px;
  font-size: clamp(2.2rem, 7vw, 4rem);
  line-height: 1.02;
}

h2 {
  margin-top: 0;
}

.lede {
  max-width: 760px;
  font-size: 1.15rem;
}

.button {
  display: inline-flex;
  min-height: 42px;
  align-items: center;
  padding: 0 16px;
  border: 1px solid CanvasText;
  border-radius: 6px;
  text-decoration: none;
  font-weight: 750;
}

.post-list {
  display: grid;
  gap: 14px;
}

.post-card {
  border-bottom: 1px solid color-mix(in oklab, CanvasText 15%, transparent);
  padding: 0 0 14px;
}

.post-card a {
  display: block;
  text-decoration: none;
}

.prose {
  max-width: 760px;
}

.theme-preview-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(230px, 1fr));
  gap: 16px;
}

.theme-preview-card {
  min-height: 310px;
  padding: 20px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  border: 1px solid color-mix(in oklab, CanvasText 16%, transparent);
}

.theme-preview-card h2 {
  font-size: 2rem;
  line-height: 1.05;
}

.theme-label {
  margin: 0;
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
}

.theme-swatch-row {
  display: flex;
  gap: 8px;
  margin: 18px 0;
}

.theme-swatch-row span {
  width: 34px;
  height: 34px;
  border-radius: 999px;
  border: 1px solid rgba(0, 0, 0, 0.16);
}

.theme-field-guide { background: #f6f4ea; color: #193f35; border-color: #9ab26d; }
.theme-field-guide .theme-swatch-row span:nth-child(1) { background: #193f35; }
.theme-field-guide .theme-swatch-row span:nth-child(2) { background: #9ab26d; }
.theme-field-guide .theme-swatch-row span:nth-child(3) { background: #d9a441; }

.theme-editorial { background: #fff8f2; color: #221b1b; border-color: #d5523f; }
.theme-editorial .theme-swatch-row span:nth-child(1) { background: #221b1b; }
.theme-editorial .theme-swatch-row span:nth-child(2) { background: #d5523f; }
.theme-editorial .theme-swatch-row span:nth-child(3) { background: #f1c27d; }

.theme-notebook { background: #f7f8fb; color: #1f2937; border-color: #8aa0b8; }
.theme-notebook .theme-swatch-row span:nth-child(1) { background: #1f2937; }
.theme-notebook .theme-swatch-row span:nth-child(2) { background: #8aa0b8; }
.theme-notebook .theme-swatch-row span:nth-child(3) { background: #e7edf3; }
""",
        f"_posts/{today}-welcome.md": f"""---
layout: post
title: "Welcome To {escape_yaml(site_name)}"
tldr: "A short introduction to what this blog is about and why it exists."
description: "{escape_yaml(description)}"
date: {today}
tags: [welcome]
---

This blog is about {subject}.

The aim is simple: collect useful notes, clear explanations, and practical
thinking in one place.

## What To Expect

| Kind Of Post | Purpose |
| --- | --- |
| Notes | Capture useful ideas before they disappear. |
| Guides | Explain how to do something clearly. |
| Reflections | Work out what is changing and why it matters. |

Start small. Publish what helps.
""",
        "_drafts/first-idea.md": f"""---
layout: post
title: "First Idea"
tldr: "A draft space for the first real post."
description: "A draft post for {escape_yaml(site_name)}."
tags: [draft]
---

Write the first real post here.

Useful shape:

1. What problem are you noticing?
2. Why does it matter?
3. What have you tried?
4. What would help someone else?
""",
        "scripts/plan_blog_assets.py": read_asset_planner_script(),
    }


def clean_slug(value: str) -> str:
    return SLUG_RE.sub("-", value.lower()).strip("-")


def escape_html(value: str) -> str:
    return value.replace("&", "&amp;").replace('"', "&quot;").replace("<", "&lt;").replace(">", "&gt;")


def escape_yaml(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def shell_quote(value: str) -> str:
    return shlex.quote(value)


def read_asset_planner_script() -> str:
    return (Path(__file__).with_name("plan_blog_assets.py")).read_text(encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
