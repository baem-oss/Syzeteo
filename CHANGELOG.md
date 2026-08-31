# Changelog

All notable changes to Syzeteo are documented here.

## [1.1.0-dev1] - 2026-08-31

Development state implementing US #26.

### Added

- abort an ongoing game after explicit confirmation;
- persistent language-neutral game status `aborted`;
- aborted-game management on the Instructor Settings page;
- deletion of aborted games after explicit confirmation;
- German and English UI texts for abort/delete workflows and aborted round coverage;
- five automated domain tests for abort/delete behavior.

### Changed

- round coverage now distinguishes `aborted` from `running`, `played`, and `open`;
- aborted games are excluded from regular team/course result totals and cannot be resumed;
- after deletion of an aborted game, the respective round becomes available again for that course;
- requirements, business rules, use cases, and traceability have been updated for US #26 / GR #11.

### Compatibility

- SQLite schema version remains `2`; no database migration is required.
- existing Syzeteo 1.0.0 data remains compatible.

## [1.0.0] - 2026-08-27

Initial public baseline under the Syzeteo name.

### Added

- Syzeteo branding with the claim `Knowledge. Teams. Rounds.` and the product description `An open-source team-based active recall game for the classroom.`;
- bilingual English/German application UI with English reference and fallback catalog;
- language selection on login/first-run and in Instructor Settings;
- short bilingual explanation of the Syzeteo name on the login/first-run page;
- persistent `ui_locale` setting;
- course, student, learning-unit and Question Pool administration;
- round configuration with exactly eight Question Cards and one Challenge Card;
- manual or random regular player selection from player 2 onward;
- Team Assist without consuming the assisting person's regular turn;
- last-card rule: the final remaining card is always answered by the Instructor and scores 0 points;
- team- and course-level result tracking without individual performance analytics;
- JSON Question Pool exchange format `Syzeteo question pool`, version 1;
- `syzeteo.sqlite3` as the application database;
- `SYZETEO_DATA_DIR` as the optional data-directory environment variable;
- Docker deployment and automated test suite;
- German and English requirements, traceability, technical baseline and i18n specification.
