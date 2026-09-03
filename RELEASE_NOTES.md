# Syzeteo 1.1.0

**Knowledge. Teams. Rounds.**

*An open-source team-based active recall game for the classroom.*

Syzeteo 1.1.0 is the first functional update to the public 1.0.0 baseline. It adds a controlled lifecycle for games that were started accidentally or cannot be continued, while preserving completed game history and remaining fully compatible with the existing SQLite schema.

## Added

- Instructor can abort a running game after explicit confirmation;
- persistent language-neutral game status `aborted`;
- aborted games are shown on the Instructor page;
- only aborted games can be deleted through the new function;
- deleting an aborted game frees the corresponding course/round combination so the round can be played again;
- German and English UI texts for the complete abort/delete workflow;
- five domain tests for US #26 and one navigation regression test.

## Behavior

An aborted game is neither running nor regularly completed. It cannot be resumed and is excluded from regular team/course results. Its game-specific data remains stored until the Instructor explicitly deletes it.

Completed games remain protected from deletion through US #26.

## Compatibility

- SQLite schema version remains `2`;
- no data migration is required;
- existing Syzeteo 1.0.0 databases can be used unchanged;
- application and schema versions remain independent.

## Verification

- automated test suite: **62/62 passed**;
- staged test using a copy of the existing dataset: passed;
- manual smoke test for abort/delete workflow: passed;
- productive cutover: passed;
- post-cutover HTTP, SQLite integrity, and foreign-key checks: passed;
- inventory counts remained unchanged across the code upgrade.

## Internationalization

English and German catalogs each contain **493 translation keys** with identical key sets and compatible placeholders.

## Technical identifiers

- application version: `1.1.0`
- data directory environment variable: `SYZETEO_DATA_DIR`
- database file: `syzeteo.sqlite3`
- Question Pool format: `Syzeteo question pool`, version 1
- SQLite schema version: `2`

## License

Apache License 2.0.
