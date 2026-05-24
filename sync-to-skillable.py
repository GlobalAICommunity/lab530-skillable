"""Generate `skillable.md` and `index.html` for the workshop.

The workshop markdown files in this folder are deployed by the
`skillable-docs` GitHub Actions workflow to an Azure Static Web App. This
script just regenerates the two index files that reference them:

- `skillable.md`: page-separated list of `!INSTRUCTIONS[<title>](<url>)`
   entries, one per workshop step, used to import the workshop into
   Skillable.
- `index.html`: simple landing page linking each step, served at the root
   of the Static Web App.
"""

from __future__ import annotations

from pathlib import Path


SCRIPT_DIR = Path(__file__).resolve().parent
SKILLABLE_FILE = "skillable.md"
INDEX_FILE = "index.html"
BASE_URL = "https://raw.githubusercontent.com/GlobalAICommunity/lab530-skillable/refs/heads/main/"


def extract_title(md_path: Path) -> str:
    """Return the first H1 heading from a markdown file, or the filename stem."""
    with md_path.open("r", encoding="utf-8") as f:
        for line in f:
            stripped = line.strip()
            if stripped.startswith("# "):
                return stripped[2:].strip()
    return md_path.stem


def write_skillable(entries: list[tuple[str, str]]) -> Path:
    base = BASE_URL if BASE_URL.endswith("/") else BASE_URL + "/"
    content = "\n===\n".join(
        f"!INSTRUCTIONS[{title}]({base}{name})" for name, title in entries
    ) + "\n"
    path = SCRIPT_DIR / SKILLABLE_FILE
    path.write_text(content, encoding="utf-8")
    return path


def write_index(entries: list[tuple[str, str]]) -> Path:
    items = "\n".join(
        f'    <li><a href="{name}">{title}</a></li>' for name, title in entries
    )
    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Lost in the City — Workshop</title>
  <style>
    body {{ font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; }}
    li {{ margin: 0.25rem 0; }}
  </style>
</head>
<body>
  <h1>Lost in the City — Workshop</h1>
  <p>Workshop instructions:</p>
  <ul>
{items}
  </ul>
</body>
</html>
"""
    path = SCRIPT_DIR / INDEX_FILE
    path.write_text(html, encoding="utf-8")
    return path


def main() -> int:
    md_files = sorted(
        p for p in SCRIPT_DIR.glob("*.md") if p.name != SKILLABLE_FILE
    )
    if not md_files:
        print("No markdown files found.")
        return 0

    entries = [(md.name, extract_title(md)) for md in md_files]

    skillable_path = write_skillable(entries)
    print(f"Wrote {skillable_path}")

    index_path = write_index(entries)
    print(f"Wrote {index_path}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
