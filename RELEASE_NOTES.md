# Syzeteo 1.1.1

**Final release.**

Syzeteo 1.1.1 consolidates the functional work since 1.1.0: course-specific team names, deterministic schema migration, literal question rendering, question-level analysis, localized duplicate-student validation, and a round-selection UI fix.

## Added

- freely configurable team names per course (US #27 / GR #12);
- immutable team-name snapshots on games;
- question-level analysis for one course or all courses (US #28 / GR #13);
- attempts, correct, incorrect, and success-rate metrics per played question version;
- CSV export of question analysis;
- support for optional locally installed presentation-profile catalogs.

## Fixed and changed

- question and model-answer content is rendered literally so numbered lines are preserved;
- Challenge Card title and subtitle are sourced from the active translation catalog;
- duplicate student names within one course produce localized domain errors;
- round question selectors no longer display an overlay that can cover the save button;
- exactly eight subject questions remain enforced by the domain layer;
- Streamlit updated to 1.54.0;
- `.dockerignore` prevents persistent databases and backups from entering Docker images.

## Question analysis semantics

Only regularly scored subject questions from games with status `finished` are included. Challenge Cards and the final Instructor-resolved card are excluded. Team Assist answers count as normal attempts. Changed question versions remain separate through stored question snapshots. No student names or individual performance analytics are used.

## Upgrade from 1.1.0

SQLite schema version changes from `2` to `3`. Schema 3 adds:

- `courses.team1_name`
- `courses.team2_name`
- `games.team1_name_snapshot`
- `games.team2_name_snapshot`

The migration is additive and idempotent. Existing records receive `Team 1` and `Team 2`. Container startup performs migration and verifies schema version, SQLite integrity, and foreign keys before Streamlit is launched. A failed preflight aborts startup.

## Internationalization

The public release ships the two official catalogs `en` and `de`, with identical key sets and compatible placeholders. Optional complete local presentation profiles remain supported but are not included in the public release tree.

## Verification

- full automated test suite: **97/97 passed**;
- Python compile check: pass;
- `en` / `de` catalog parity: pass;
- schema-2 → schema-3 migration preservation: pass.
