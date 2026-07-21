# My Favorite Actors, Actresses & Films

A personal archive by **artistso**.

## Objectivity and authorship notice

This repository combines externally verifiable entertainment facts with the first-person recollections, interpretations, rankings, and opinions of a 42-year-old author who describes having a rare hyperthymestic mind.

- **Verified fact**: externally checkable and source-supported.
- **Personal account**: what the author remembers experiencing or being told.
- **Opinion**: an aesthetic judgment, interpretation, ranking, or preference.

Read the complete [Objectivity and Authorship Disclaimer](DISCLAIMER.md).

## Absolute favorite film

### The Adventures of Milo and Otis

This is my absolute favorite movie of all time. I value its animal-centered visual storytelling: I can mute Dudley Moore's U.S.-version narration and still enjoy the story without visual distraction. When working from a personal-use copy I am legally permitted to edit, retaining the environmental sounds while reducing the vocal narration creates an especially calm experience to share with my cats.

Read the full profile: [The Adventures of Milo and Otis](favorite-films/milo-and-otis.md).

## Repository sections

| Path | Description |
| --- | --- |
| `favorite-films/` | Ranked favorite films and viewing accounts |
| `wagons-east/` | Cast profiles and personal retrospective statements |
| `back-to-the-future/` | Michael J. Fox and Christopher Lloyd |
| `personal-favorites/` | Performers across multiple genres |
| `about-the-author/` | First-person context for the recall framework |
| `data/` | Canonical structured records used for integrity checks |
| `scripts/` | Automated validation tools |

## Current performer roster

The canonical roster is stored in [`data/people.json`](data/people.json). It currently contains **15 unique performer records**. [`data/films.json`](data/films.json) contains the ranked film records.

## Validation

```bash
python scripts/validate_archive.py
```

CI fails if local links break, record identifiers collide, required profiles are missing, possible precise street addresses reappear, or the declared counts disagree with the canonical data.
