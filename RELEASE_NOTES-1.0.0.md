# Syzeteo 1.0.0

**Knowledge. Teams. Rounds.**

*An open-source team-based active recall game for the classroom.*

Syzeteo 1.0.0 is the first public baseline under the Syzeteo name. It provides a complete two-team active-recall classroom game with course and question administration, configurable rounds, persistent team-level results, and a fully internationalized English/German interface.

## Name

The name derives from the Ancient Greek **συζητέω (syzēteō)**: *to seek or examine together*, and in context also *to discuss or question together*. The name reflects the collaborative learning concept behind the application.

## Included

- complete English and German UI;
- English reference/fallback locale;
- language selection on login/first-run and in Instructor Settings;
- brief bilingual explanation of the Syzeteo name on the login/first-run page;
- persistent UI locale;
- eight Question Cards plus one Challenge Card per round;
- strict team alternation;
- configurable manual or random regular player selection from player 2 onward;
- Team Assist without blocking a later regular turn for the assisting person;
- final-card rule with Instructor answer and zero points regardless of card type;
- Question Pool JSON/CSV export and JSON import using the native Syzeteo format;
- SQLite persistence using `syzeteo.sqlite3`;
- Docker deployment;
- no individual student performance analytics;
- automated regression, release and i18n consistency tests (**56 tests, all passing**).

## Technical identifiers

- data directory environment variable: `SYZETEO_DATA_DIR`
- database file: `syzeteo.sqlite3`
- Question Pool format: `Syzeteo question pool`, version 1
- SQLite schema version: `2`

## License

Apache License 2.0.
