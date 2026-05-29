# Blog Article Editor

This is a public-safe playbook for improving an existing blog article with an
AI editor.

The tool is deliberately not "rewrite this immediately". The better flow is:

```text
load article -> understand current shape -> grill the human -> rewrite with a clear contract
```

## What It Is For

Use this when a human already has a rough article, draft, imported post, or
older blog page and says something like:

> Help me rewrite this. I know there is something good in it, but I am not sure
> what I am really trying to say.

## Default Behaviour

| Decision | Default |
| --- | --- |
| Input | Markdown article with optional frontmatter |
| First output | Editing worksheet, not rewritten prose |
| Conversation style | One focused grill question at a time |
| Rewrite goal | Preserve the human's real point and voice while making the article clearer |
| Safety | Do not invent facts, expose secrets, or publish private source |
| Final output | Updated Markdown article plus change notes |

## Agent Workflow

| Step | Agent action | Human outcome |
| --- | --- | --- |
| 1 | Run `scripts/prepare_blog_article_edit.py path/to/article.md`. | A worksheet appears next to the article. |
| 2 | Read the worksheet before rewriting. | The agent sees title, TLDR, headings, source excerpt, and risks. |
| 3 | Ask the first grill question. | The human clarifies the article's real purpose. |
| 4 | Continue one question at a time until the rewrite contract is clear. | The article gets a target, audience, tone, and evidence boundary. |
| 5 | Rewrite the article in Markdown. | The human gets a complete revised draft. |
| 6 | Show a short change summary. | The human can accept, reject, or ask for another pass. |
| 7 | Commit only after the human is happy or explicitly asks for implementation. | Git keeps the recovery point. |

## Grill Questions

Ask these one at a time. Provide a recommended answer when obvious from the
article.

| Order | Question | Why |
| --- | --- | --- |
| 1 | What is the one sentence this article must land? | Prevents decorative rewriting. |
| 2 | Who is the reader? | Controls explanation depth and examples. |
| 3 | What should the reader do, feel, or understand afterwards? | Turns writing into an outcome. |
| 4 | What part must survive unchanged? | Protects the human's strongest line or evidence. |
| 5 | What is probably noise? | Gives permission to cut. |
| 6 | Which claims need evidence or softer wording? | Avoids overclaiming. |
| 7 | What tone should it have? | Keeps the voice human. |
| 8 | Is anything private, legally risky, or not public-safe? | Prevents accidental exposure. |

Stop early if the rewrite contract is already clear.

## Rewrite Contract

Before rewriting, restate this contract:

| Field | Fill In |
| --- | --- |
| Core point | One sentence. |
| Reader | Specific audience. |
| Desired effect | What changes after reading. |
| Voice | Tone and style. |
| Keep | Lines, examples, images, links, or structure that must remain. |
| Cut | Sections or habits to remove. |
| Evidence | Claims that need support, caveats, or links. |
| Safety | What must not be exposed. |

Then rewrite.

## Output Rules

| Rule | Why |
| --- | --- |
| Preserve Markdown frontmatter unless changing it is part of the task. | Avoid breaking static site builds. |
| Keep links, images, embeds, and forms unless the human asks to remove them. | Existing articles often have functional assets. |
| Do not invent citations or facts. | Public trust matters. |
| Prefer clearer structure over more words. | Editing is often cutting. |
| Include a TLDR when the site supports it. | Readers should be able to scan the index. |
| Mention any major claim that still needs evidence. | Separates writing polish from truth checking. |

## Ready Prompt

Use `prompts/blog-article-editor.md` when starting an agent in this mode.

Use `scripts/prepare_blog_article_edit.py` to create the first worksheet.
