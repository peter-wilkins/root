#!/usr/bin/env python3
"""Create a licence-safe image asset plan for a blog."""

from __future__ import annotations

import argparse
from datetime import date
from pathlib import Path
from urllib.parse import quote_plus


DEFAULT_ROLES = [
    ("hero", "Homepage hero image"),
    ("about", "About/mission supporting image"),
    ("post-card", "Generic blog card thumbnail"),
    ("social-share", "Default social sharing image"),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--name", required=True, help="site name")
    parser.add_argument("--subject", required=True, help="blog subject")
    parser.add_argument("--audience", default="curious readers", help="target audience")
    parser.add_argument("--out", type=Path, default=Path("asset-plan.md"))
    args = parser.parse_args()

    output = args.out.expanduser().resolve()
    output.write_text(
        render_plan(name=args.name.strip(), subject=args.subject.strip(), audience=args.audience.strip()),
        encoding="utf-8",
    )
    print(f"wrote asset plan: {output}")
    return 0


def render_plan(*, name: str, subject: str, audience: str) -> str:
    today = date.today().isoformat()
    rows = []
    for role, purpose in DEFAULT_ROLES:
        query = f"{subject} {role.replace('-', ' ')}"
        rows.append(
            "| {role} | {purpose} | `{query}` | [Openverse]({openverse}) / [Unsplash]({unsplash}) / [Pexels]({pexels}) / [Pixabay]({pixabay}) | | | | | | | |".format(
                role=role,
                purpose=purpose,
                query=query,
                openverse=f"https://openverse.org/search/image?q={quote_plus(query)}",
                unsplash=f"https://unsplash.com/s/photos/{quote_plus(query)}",
                pexels=f"https://www.pexels.com/search/{quote_plus(query)}/",
                pixabay=f"https://pixabay.com/images/search/{quote_plus(query)}/",
            )
        )

    return f"""# Asset Plan For {name}

Generated: {today}

Subject: {subject}

Audience: {audience}

## Principle

Do not treat "free image" as "safe image".

Use images that fit the story, avoid recognisable people/trademarks unless needed,
and keep enough attribution/source metadata that the site can be audited later.

## Image Candidates

Fill this matrix before committing images to the site.

| Role | Purpose | Search query | Source search links | Chosen URL | Creator | Licence | Attribution text | Local filename | Alt text | Approval |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

## Source Defaults

| Source | Best Use | Notes |
| --- | --- | --- |
| Openverse | Creative Commons or public-domain material where attribution metadata matters. | Prefer when attribution and licence clarity are important. |
| Unsplash | High-quality editorial and landscape photography. | Attribution is appreciated even when not required. |
| Pexels | Website/blog/app photos and videos with simple terms. | Avoid implying endorsement by people or brands in images. |
| Pixabay | Broad media pool including images, video, audio, and illustrations. | Check prohibited uses and trademarks/recognisable people. |

## Safety Checklist

| Check | Pass Condition |
| --- | --- |
| Licence | Source licence allows website/blog use. |
| Attribution | Creator/source recorded even if attribution is optional. |
| People | No identifiable person used in a bad light or sensitive context. |
| Brands | No recognisable logo/trademark used commercially unless safe. |
| Standalone resale | Image is not being sold or redistributed as stock/wallpaper. |
| Fit | Image says something true about the article, not generic decoration. |
| Local copy | Filename is clear and source URL is recorded. |

## Suggested Site Folders

```text
public/assets/img/
src/content/posts/
```
"""


if __name__ == "__main__":
    raise SystemExit(main())
