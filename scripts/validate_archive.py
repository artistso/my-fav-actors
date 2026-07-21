#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
ERRORS: list[str] = []


def error(message: str) -> None:
    ERRORS.append(message)


def load(path: str):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


site = load("data/site.json")
people = load("data/people.json")
films = load("data/films.json")

if site["people_count"] != len(people):
    error(f"people_count={site['people_count']} but records={len(people)}")
if site["film_count"] != len(films):
    error(f"film_count={site['film_count']} but records={len(films)}")

for label, records in (("person", people), ("film", films)):
    ids = [record.get("id") for record in records]
    profiles = [record.get("profile") for record in records]
    if len(ids) != len(set(ids)):
        error(f"duplicate {label} IDs")
    if len(profiles) != len(set(profiles)):
        error(f"duplicate {label} profile paths")
    for record in records:
        for field in ("id", "profile"):
            if not record.get(field):
                error(f"{label} missing {field}: {record}")
        if not (ROOT / record["profile"]).is_file():
            error(f"missing profile: {record['profile']}")

# Stress-test the roster equation:
# canonical performer records = unique performer Markdown profiles.
profile_files: list[Path] = []
for folder in ("wagons-east", "back-to-the-future", "personal-favorites"):
    profile_files.extend(
        path for path in (ROOT / folder).glob("*.md") if path.name != "README.md"
    )
canonical_profiles = {ROOT / record["profile"] for record in people}
if set(profile_files) != canonical_profiles:
    error(
        "performer profile set mismatch: "
        f"filesystem={len(profile_files)}, canonical={len(canonical_profiles)}"
    )


class LinkParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.references: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        values = dict(attrs)
        for key in ("href", "src"):
            if key in values:
                self.references.append(values[key])


html_files = list(ROOT.rglob("*.html"))
for page in html_files:
    text = page.read_text(encoding="utf-8")
    if "Objectivity notice:" not in text and page != ROOT / "disclaimer/index.html":
        error(f"missing objectivity notice: {page.relative_to(ROOT)}")

    parser = LinkParser()
    parser.feed(text)
    for reference in parser.references:
        parsed = urlparse(reference)
        if parsed.scheme or reference.startswith(("#", "mailto:", "javascript:")):
            continue
        clean_path = parsed.path
        if not clean_path:
            continue
        target = (page.parent / clean_path).resolve()
        if clean_path.endswith("/"):
            target = target / "index.html"
        if not target.exists():
            error(f"broken local target in {page.relative_to(ROOT)}: {reference}")

# Detect likely precise street addresses without storing any redacted value.
address_pattern = re.compile(
    r"\b\d{3,5}\s+[A-Z][A-Za-z'-]+\s+"
    r"(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Villa|Drive|Dr)\b"
)
for path in list(ROOT.rglob("*.md")) + list(ROOT.rglob("*.html")) + list(ROOT.rglob("*.json")):
    if address_pattern.search(path.read_text(encoding="utf-8")):
        error(f"possible precise street address in {path.relative_to(ROOT)}")

if ERRORS:
    print("Archive validation failed:", file=sys.stderr)
    for item in ERRORS:
        print(f"- {item}", file=sys.stderr)
    raise SystemExit(1)

print(
    f"Validated {len(people)} people, {len(films)} films, "
    f"{len(html_files)} HTML pages, and all local links."
)
