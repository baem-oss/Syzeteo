# Syzeteo – Technical Baseline 1.1.1

Date: 2026-09-10

## 1. Status and purpose

`1.1.1` is the Syzeteo 1.1.1 release, based on Syzeteo 1.1.0. It contains question-rendering fixes, US #27 “Manage Team Names”, GR #12 “Course-specific Team Names”, the deterministic schema-3 startup preflight, localized duplicate-student validation, US #28 “Analyze Questions” with GR #13 “Question-level Result Aggregation”, and the round-question-selection usability fix.

## 2. Runtime and deployment

- Application framework: Streamlit 1.54.0
- Implementation language: Python
- Persistence: SQLite
- Deployment: Docker / Docker Compose
- Data directory: `SYZETEO_DATA_DIR`, default `./persistent`
- Database file: `syzeteo.sqlite3`
- Application version: `1.1.1`
- SQLite schema version: `PRAGMA user_version = 3`

## 3. Schema change 2 → 3

Schema 3 adds only additive columns:

- `courses.team1_name`
- `courses.team2_name`
- `games.team1_name_snapshot`
- `games.team2_name_snapshot`

Existing schema-2 databases are migrated automatically and idempotently to schema 3 during container startup before Streamlit starts. Existing courses and games receive the previous display names `Team 1` and `Team 2`. Existing domain data is not deleted or rewritten.

## 4. Team names

- Team names are course-specific.
- Both names must be non-empty and distinct within the course.
- Internal team identifiers remain `1` and `2`.
- Team names can be set when a course is created and changed later.
- Changes are blocked while the course has a game with status `running`.
- Both team names are snapshotted when a game starts.
- Later renaming does not retroactively change running, aborted, or completed games.

## 5. Rendering and round editing

Question and model-answer text is treated as user content and is not interpreted as Markdown. Numbered lines remain literal on Question Cards, in opened questions, and in the round overview. The round question selector no longer uses Streamlit's selection-limit popover, which could cover the save button; the domain layer still enforces exactly eight subject questions.

## 6. Internationalization

- `en.json` and `de.json` are the official shipped catalogs.
- Both catalogs have identical key sets and compatible placeholders.
- Fully installed optional local presentation profiles are supported as distinct locale IDs.
- The revealed Challenge Card obtains its title and subtitle from the active catalog.
- Domain values, data model, game rules, and the technical Question Pool interchange format remain language-neutral.

## 7. Question analysis

- Analysis is integrated into the existing Question Log page.
- The Instructor can select one course or an all-courses aggregation.
- Only subject Question Cards from games with status `finished` are analyzed.
- Challenge Cards and the final Instructor-resolved card are excluded.
- Team Assist answers count as normal attempts.
- Metrics per played question version: attempts, correct, incorrect, and success rate.
- Changed question versions are kept separate using `question_id` plus the stored `question_text_snapshot`.
- No student names or individual performance data are analyzed.
- CSV export is available.

## 8. Repository hygiene

`persistent/`, SQLite files, WAL/SHM files, and backups are excluded from the Docker build context through `.dockerignore`. Release test REL-10 additionally verifies that no persistent database files enter the release tree.

## 9. Verification

The release contains domain, migration, rendering, release, navigation, authentication, and i18n tests. In particular, it verifies:

- team-name validation, running-game lock, and immutable game snapshots;
- automatic schema-2 to schema-3 migration without data loss;
- fail-closed startup preflight for unsupported schema versions or foreign-key violations;
- literal question rendering;
- localized duplicate-student errors;
- key and placeholder parity for `en` and `de`;
- support for optionally installed local presentation profiles;
- course-specific and all-courses question analysis without individual analytics;
- domain validation of exactly eight subject questions per round.
