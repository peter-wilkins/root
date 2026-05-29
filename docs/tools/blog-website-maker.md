# Blog Website Maker

This is a public-safe playbook for an agent that receives a request like:

> Please make me a blog website. It is about local gardening and practical ecology.

The goal is to turn that request into a small, editable, static blog site without
making the human learn hosting, themes, frontmatter, or build tooling first.

## Default Choice

Use a static Astro blog with Markdown posts.

| Decision | Default |
| --- | --- |
| Site generator | Astro |
| Post format | Markdown |
| Editing model | Files in GitHub first |
| Hosting target | Static host such as Cloudflare Pages or GitHub Pages |
| Public state | Drafts hidden until explicitly published |
| Asset rule | Put small images in the repo; use object storage later for large media |

## First Questions

Ask only the questions needed to create the first useful version.

| Question | Recommended default |
| --- | --- |
| What is the blog about? | Use the user's own phrase as the subject. |
| What should it be called? | Derive a plain name from the subject. |
| Who is it for? | Curious readers who want useful, practical posts. |
| What tone? | Clear, personal, practical, not corporate. |
| Do you already have posts? | If no, create one welcome post and one idea stub. |
| Do you have a domain? | If no, use local preview and leave deployment notes. |

Do not block on branding, logo, analytics, newsletter, comments, or CMS.

## Agent Workflow

| Step | Agent action | Human outcome |
| --- | --- | --- |
| 1 | Restate the site name, subject, audience, and tone in one short paragraph. | The human sees the shape before files are created. |
| 2 | Scaffold the Astro blog with `scripts/create_blog_site.py`. | A working local project appears. |
| 3 | Create a home page that says what the blog is and why it exists. | The first screen is real content, not template filler. |
| 4 | Create `/blog/` with title plus TLDR cards. | Readers can scan without opening every post. |
| 5 | Create one welcome post and one draft idea post. | The human has an editable starting point. |
| 6 | Run `npm install` and `npm run build` when tools/network allow it. | The agent proves the site builds. |
| 7 | Commit the scaffold. | Git becomes the recovery point. |
| 8 | Give one preview URL or one exact next hosting step. | The human is not left holding a setup puzzle. |

## Content Rules

| Rule | Why |
| --- | --- |
| Put a TLDR under every post title. | People should not need to open every post to understand the index. |
| Keep raw private notes out of public posts. | Source material is evidence, not automatically publishable copy. |
| Use drafts by default. | Publication should be explicit. |
| Prefer matrices for comparisons. | Tables make options easier to scan. |
| Keep pages plain and readable first. | The writing matters more than theme polish. |

## File Shape

```text
blog-name/
  README.md
  package.json
  astro.config.mjs
  src/
    content.config.ts
    content/posts/
    layouts/BaseLayout.astro
    pages/index.astro
    pages/blog/index.astro
    pages/blog/[slug].astro
    styles/global.css
```

## Publishing Safety

Before making a site public, check:

| Check | Pass condition |
| --- | --- |
| Secrets | No `.env`, tokens, private keys, device IDs, or account credentials. |
| Personal data | No raw private logs or unreviewed exports. |
| Drafts | Draft posts are hidden from production unless explicitly enabled. |
| Rights | Images and quoted material are owned, licensed, or replaced. |
| External services | No spending, domain changes, or account setup without human approval. |

## Hosting Defaults

For Cloudflare Pages, use:

| Field | Value |
| --- | --- |
| Framework preset | `Astro` |
| Build command | `npm run build` |
| Build output directory | `dist` |

If the site is in a subfolder of a larger repo, set the Cloudflare root directory
to that subfolder.

## Ready Prompt

Use `prompts/blog-website-maker.md` when starting an agent in this mode.

Use `scripts/create_blog_site.py` for the first scaffold.
