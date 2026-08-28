# Syzeteo – Technical Baseline 1.0.0

Date: 2026-08-27

## 1. Purpose

This document defines the technical baseline for Syzeteo 1.0.0. The first public Syzeteo release uses a native Syzeteo data model and language-neutral persisted domain identifiers.

## 2. Runtime and deployment

- application framework: Streamlit
- implementation language: Python
- persistence: SQLite
- supported deployment path: Docker / Docker Compose
- default host port: `8502`
- application version: `1.0.0`

## 3. Persistence

- database file: `syzeteo.sqlite3`
- default data directory: `./persistent`
- optional environment variable: `SYZETEO_DATA_DIR`
- SQLite schema version: `PRAGMA user_version = 2`

Application version and SQLite schema version are independent. Schema version 2 is the first published Syzeteo schema baseline and includes the `app_settings` table used for persistent UI settings.

Syzeteo 1.0.0 does not use legacy pre-release database names or environment variables at runtime.

## 4. Persisted domain terminology

| Domain term | Persisted identifier |
|---|---|
| Question Card | `card_type = 'question'` |
| Challenge Card | `card_type = 'challenge'` |
| Team Assist on a card | `team_assist_used` |
| Team Assist Team 1 | `team1_assist_used` |
| Team Assist Team 2 | `team2_assist_used` |
| UI locale setting | `app_settings.ui_locale` |

Domain-neutral table names do not receive a product prefix.

## 5. Core tables

Syzeteo 1.0.0 uses, among others:

- `courses`
- `students`
- `learning_units`
- `questions`
- `rounds`
- `round_questions`
- `games`
- `game_roster`
- `game_cards`
- `game_undo`
- `app_settings`
- authentication tables created by `auth.py`

## 6. Question Pool exchange format

JSON imports and exports use:

```json
{
  "format": "Syzeteo question pool",
  "version": 1
}
```

Question Pool imports accept only the native Syzeteo format. Other format identifiers and unsupported format versions are rejected.

CSV is available as a human-readable export format. JSON is the defined exchange format for import between Syzeteo installations.

## 7. Internationalization architecture

- locale catalogs: `locales/en.json`, `locales/de.json`
- reference and fallback locale: English (`en`)
- persistent setting: `ui_locale`
- locale selection points: login/first-run and Instructor Settings only
- stable language-neutral page IDs and domain/status codes
- Question Pool content is user-provided content and is not translated by the application

The two official catalogs must contain the same key set and compatible placeholders.

## 8. Technically enforced domain rules

- A round contains exactly eight Question Cards and one Challenge Card.
- The two teams alternate strictly during regular turns.
- A person can take at most one regular turn in a round.
- A Team Assist is not a regular turn and does not make the assisting person ineligible for a later regular turn.
- The last remaining card is always answered by the Instructor and scores 0 points, regardless of card type.
- Individual student performance data is neither stored nor evaluated.

## 9. Release acceptance criteria

| ID | Criterion |
|---|---|
| REL-01 | A new installation uses `syzeteo.sqlite3`. |
| REL-02 | `SYZETEO_DATA_DIR` is the supported data-directory environment variable. |
| REL-03 | Foreign Question Pool format identifiers are rejected. |
| REL-04 | New exports use `Syzeteo question pool`, version 1. |
| REL-05 | Runtime/UI source contains no obsolete product branding. |
| REL-06 | Challenge Cards are persisted as `challenge`. |
| REL-07 | The schema uses the native Team Assist fields. |
| REL-08 | Team Assist does not block the assisting person from a later regular turn. |
| REL-09 | The last card scores 0 points regardless of card type. |
| REL-10 | The release contains no persistent SQLite database or backup file. |
| REL-11 | The generated SQLite schema contains no obsolete product/domain identifiers. |
| REL-12 | Runtime code contains no legacy pre-release database/path identifiers. |
| REL-13 | SQLite schema version is `2` and includes `app_settings`. |
| REL-14 | English and German catalogs have identical key sets and compatible placeholders. |
| REL-15 | All literal translation keys referenced by runtime code exist in the reference catalog. |

## 10. Release verification

Verification performed for the Syzeteo 1.0.0 baseline:

- complete automated suite: **56/56 tests passed**;
- official locale catalogs: **473 keys each**, identical key sets;
- SQLite schema version: `2`;
- release tree contains no persistent SQLite database, WAL/SHM file or backup.

## 11. Future schema changes

After publication, the database is part of product compatibility. Any later schema change must:

1. increment the SQLite schema version when required,
2. provide an explicit and tested migration path for released Syzeteo databases,
3. preserve data integrity and domain consistency, and
4. be protected by automated regression tests.
