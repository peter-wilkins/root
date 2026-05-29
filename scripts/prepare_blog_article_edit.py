#!/usr/bin/env python3
"""Create a blog article edit/grill worksheet from a Markdown file."""

from __future__ import annotations

import argparse
import re
from datetime import datetime, timezone
from pathlib import Path


HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
WORD_RE = re.compile(r"\b[\w'-]+\b")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("article", type=Path)
    parser.add_argument("--out", type=Path, help="worksheet output path")
    parser.add_argument("--max-body-chars", type=int, default=12000)
    args = parser.parse_args()

    article = args.article.expanduser().resolve()
    if not article.is_file():
        raise SystemExit(f"Missing article: {article}")
    if article.suffix.lower() not in {".md", ".mdx", ".markdown"}:
        raise SystemExit(f"Expected a Markdown article: {article}")

    parsed = parse_markdown(article.read_text(encoding="utf-8"))
    title = infer_title(article, parsed)
    tldr = first_present(parsed["frontmatter"], ["tldr", "description", "subtitle", "excerpt"])
    headings = extract_headings(parsed["body"])
    word_count = len(WORD_RE.findall(strip_markdown(parsed["body"])))
    output = args.out.expanduser().resolve() if args.out else article.with_suffix(article.suffix + ".edit.md")

    worksheet = render_worksheet(
        article=article,
        title=title,
        tldr=tldr,
        headings=headings,
        word_count=word_count,
        frontmatter=parsed["frontmatter"],
        body=parsed["body"],
        max_body_chars=args.max_body_chars,
    )
    output.write_text(worksheet, encoding="utf-8")
    print(f"wrote edit worksheet: {output}")
    return 0


def parse_markdown(text: str) -> dict[str, object]:
    if not text.startswith("---\n"):
        return {"frontmatter": {}, "body": text}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {"frontmatter": {}, "body": text}
    raw_frontmatter = parts[1]
    body = parts[2].lstrip()
    return {"frontmatter": parse_frontmatter(raw_frontmatter), "body": body}


def parse_frontmatter(raw: str) -> dict[str, str]:
    frontmatter: dict[str, str] = {}
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")
    return frontmatter


def infer_title(article: Path, parsed: dict[str, object]) -> str:
    frontmatter = parsed["frontmatter"]
    if isinstance(frontmatter, dict):
        title = frontmatter.get("title")
        if isinstance(title, str) and title.strip():
            return title.strip()
    body = str(parsed["body"])
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) == 1:
            return match.group(2).strip()
    return article.stem.replace("-", " ").replace("_", " ").title()


def first_present(frontmatter: object, keys: list[str]) -> str:
    if not isinstance(frontmatter, dict):
        return ""
    for key in keys:
        value = frontmatter.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def extract_headings(body: str) -> list[tuple[int, str]]:
    headings: list[tuple[int, str]] = []
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            headings.append((len(match.group(1)), match.group(2).strip()))
    return headings


def strip_markdown(markdown: str) -> str:
    text = re.sub(r"```.*?```", " ", markdown, flags=re.DOTALL)
    text = re.sub(r"`([^`]+)`", r"\1", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"[_*#>\-]+", " ", text)
    return re.sub(r"\s+", " ", text).strip()


def render_worksheet(
    *,
    article: Path,
    title: str,
    tldr: str,
    headings: list[tuple[int, str]],
    word_count: int,
    frontmatter: object,
    body: str,
    max_body_chars: int,
) -> str:
    generated = datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")
    body_excerpt = body if len(body) <= max_body_chars else body[:max_body_chars].rstrip() + "\n\n[TRUNCATED FOR WORKSHEET]\n"
    heading_lines = "\n".join(f"{'  ' * (level - 1)}- {text}" for level, text in headings) or "- No headings found."
    frontmatter_lines = render_frontmatter_block(frontmatter)
    recommended_core = tldr or title
    return f"""# Blog Article Edit Worksheet

Generated: {generated}

## Article Snapshot

| Field | Value |
| --- | --- |
| Source file | `{article}` |
| Title | {escape_table(title)} |
| Current TLDR/subtitle | {escape_table(tldr or "Not found")} |
| Word count | {word_count} |
| Heading count | {len(headings)} |

## Current Headings

{heading_lines}

## Grill Session

Ask these one at a time. Do not rewrite until the rewrite contract is clear.

| Order | Question | Recommended answer |
| --- | --- | --- |
| 1 | What is the one sentence this article must land? | {escape_table(recommended_core)} |
| 2 | Who is the reader? | Someone who might care about this topic but needs a clearer route in. |
| 3 | What should the reader do, feel, or understand afterwards? | Understand the point, trust the author more, and know the next practical step. |
| 4 | What part must survive unchanged? | Identify the strongest line, example, image, quote, or link before cutting. |
| 5 | What is probably noise? | Repetition, side quests, weak jokes, unsupported claims, or setup that does not serve the core point. |
| 6 | Which claims need evidence or softer wording? | Any numerical, scientific, legal, medical, financial, or public accusation claim. |
| 7 | What tone should it have? | Clear, personal, practical, not corporate. |
| 8 | Is anything private, legally risky, or not public-safe? | Remove secrets, raw private logs, personal data, unapproved quotes, and risky claims. |

## Rewrite Contract

Fill this before rewriting.

| Field | Value |
| --- | --- |
| Core point |  |
| Reader |  |
| Desired effect |  |
| Voice |  |
| Keep |  |
| Cut |  |
| Evidence/caveats |  |
| Safety/privacy |  |

## Rewrite Instructions For AI

```text
Rewrite the article after the rewrite contract is filled.

Rules:
1. Preserve Markdown frontmatter unless the contract says to change it.
2. Preserve links, images, embeds, and forms unless the contract says to remove them.
3. Do not invent facts, citations, quotes, numbers, outcomes, or external claims.
4. Make unsupported claims softer or flag them after the draft.
5. Keep the human voice, but make the structure clearer.
6. Prefer cutting and clarifying over adding generic prose.
7. Output rewritten Markdown plus a short change summary.
```

## Original Frontmatter

```yaml
{frontmatter_lines}
```

## Original Body Excerpt

```markdown
{body_excerpt}
```
"""


def render_frontmatter_block(frontmatter: object) -> str:
    if not isinstance(frontmatter, dict) or not frontmatter:
        return "(none)"
    return "\n".join(f"{key}: {value}" for key, value in frontmatter.items())


def escape_table(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


if __name__ == "__main__":
    raise SystemExit(main())
