# Changelog

All notable changes to Syzeteo are documented here.

## [1.1.1] - 2026-09-10

Syzeteo 1.1.1 release.

### Added
- US #27: freely configurable, course-specific team names.
- GR #12: team-name validation, running-game lock, stable internal team IDs, and immutable game snapshots.
- SQLite schema version 3 with automatic additive migration from schema 2.
- Deterministic startup preflight before Streamlit starts.
- US #28 / GR #13: question-level analysis for one course or across all courses.
- Per-question-version metrics for attempts, correct, incorrect, and success rate, plus CSV export.
- Support for optional locally installed presentation-profile catalogs.

### Changed
- Game, attendance, student, settings, result, and history views use course- or game-specific team display names.
- The revealed Challenge Card obtains title and subtitle from translation keys rather than hard-coded UI literals.
- Round question selectors no longer use Streamlit's maximum-selection popover; exactly eight questions remain enforced by the domain layer.
- Streamlit dependency updated to 1.54.0.

### Fixed
- Question and model-answer content is rendered literally rather than interpreted as Markdown.
- Numbered lines remain visible on Question Cards and are not renumbered in opened questions or the round overview.
- Duplicate student display names in one course produce a localized domain error instead of a raw SQLite UNIQUE-constraint message.
- Persistent databases and backups are excluded from Docker build contexts through `.dockerignore`.

### Analysis behavior
- Only regularly scored subject questions from completed games contribute to question analysis.
- Challenge Cards and the final Instructor-resolved card are excluded.
- Team Assist answers count as normal attempts.
- Changed question texts are aggregated as separate played versions.
- No individual student performance data is used or displayed.

### Compatibility
- SQLite schema migrates from version 2 to version 3.
- Existing records receive `Team 1` and `Team 2` as initial team display names.
- Migration is additive and idempotent and runs before the UI starts.
- Existing Syzeteo 1.1.0 domain data is preserved.

## [1.1.0] - 2026-09-03

### Added
- abort a running game after explicit Instructor confirmation;
- persistent language-neutral game status `aborted`;
- management and deletion of aborted games on the Instructor page;
- German and English UI texts for US #26.

### Changed
- round coverage distinguishes `aborted` from `running`, `played`, and `open`;
- aborted games are excluded from regular results and cannot be resumed;
- deleting an aborted game makes the corresponding round available again for that course.

### Compatibility
- SQLite schema remains version `2`;
- no data migration is required.

## [1.0.0] - 2026-08-27

Initial public baseline under the Syzeteo name.
