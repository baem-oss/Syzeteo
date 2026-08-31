# Syzeteo – Technical Baseline 1.1.0-dev1

Date: 2026-08-31

## 1. Status and Purpose

This document describes the **Syzeteo 1.1.0-dev1** development state based on the published version 1.0.0. It implements US #26 “Abort and Delete Game”, including GR #11 and the associated use cases.

`1.1.0-dev1` is a development state and not a published release.

## 2. Runtime and Deployment

The technical basis of Syzeteo 1.0.0 remains unchanged:

- application framework: Streamlit
- implementation language: Python
- persistence: SQLite
- deployment: Docker / Docker Compose
- default host port: `8502`
- application version: `1.1.0-dev1`

## 3. Persistence and Compatibility

- database file: `syzeteo.sqlite3`
- default data directory: `./persistent`
- optional environment variable: `SYZETEO_DATA_DIR`
- SQLite schema version: `PRAGMA user_version = 2`

US #26 requires **no SQLite schema change**. The existing `games.status` column is defined as `TEXT` and can store the additional language-neutral domain status `aborted`. The schema version therefore remains `2`.

Existing databases from the published 1.0.0 version can continue to be used without data migration. The existing migration constraint RANF #01 remains in force.

## 4. Game Status

The following domain-relevant game status values are used in this development state:

| Status | Meaning |
|---|---|
| `running` | ongoing game; can be resumed or aborted |
| `finished` | regularly completed game; contributes to results and cannot be deleted through US #26 |
| `aborted` | aborted game; cannot be resumed, does not contribute to regular results, and can be deleted on the Instructor page |

The domain transition for US #26 is:

`running` → `aborted` → deleted

US #26 provides no direct deletion path from `running` or `finished`.

## 5. Aborting a Game

The domain function `abort_game(conn, game_id)`:

- accepts only existing games with status `running`;
- atomically changes the status to `aborted`;
- initially preserves all game-related data present at the time of abort;
- removes the game from the set of resumable ongoing games;
- does not modify regularly completed games.

The game view provides the “Abort game” function with confirmation. After a successful abort, the application opens the Instructor page.

## 6. Deleting an Aborted Game

The domain function `delete_aborted_game(conn, game_id)`:

- accepts only existing games with status `aborted`;
- atomically deletes the `games` row;
- uses the existing `ON DELETE CASCADE` foreign keys to remove game-exclusive rows from `game_roster`, `game_cards`, and `game_undo`;
- leaves the course, students, round, learning units, and global Question Pool unchanged;
- releases the existing unique `(round_id, course_id)` occupation, allowing that round to be started again for the course.

Aborted games are shown on the Instructor page and can be deleted there after confirmation. Regularly completed games are not offered through this function and are rejected by the domain function.

## 7. Results and Round Coverage

- `course_scoreboard()` continues to evaluate only games with status `finished`. Aborted games therefore do not affect team totals, the number of regularly played games, wins, or draws.
- Round coverage distinguishes `open`, `running`, `aborted`, and `played`.
- While an aborted game still exists, the round/course combination is shown as `aborted`.
- Only after the aborted game is deleted does the combination become `open` again.
- Aborted games are not offered as resumable games.

## 8. Internationalization

The new UI texts and error messages are included in both official locale catalogs, English and German. They include in particular:

- “Aborted” status;
- abort prompt and confirmation;
- “Aborted games” section in Instructor Settings;
- deletion prompt and confirmation;
- language-neutral storage errors for invalid abort and delete operations.

Existing i18n consistency tests continue to verify identical key sets and compatible placeholders.

## 9. Automated Verification

The development-state build was tested with Python 3.12 against the complete automated test suite:

- **61/61 tests passed**;
- **5 new tests** specifically cover US #26;
- verification includes in particular:
  - `running` → `aborted`;
  - exclusion of aborted games from regular results;
  - abort only for ongoing games;
  - deletion only for aborted games;
  - cascading deletion of game-related data;
  - ability to start the round again after deletion;
  - existing regression, release, and i18n checks.

The automated suite does not contain browser-based end-to-end testing of the Streamlit interaction. The UI integration must therefore additionally be checked with a manual smoke test in the target system.

## 10. Manual Smoke-Test Acceptance Points

1. An ongoing game displays “Abort game”.
2. Declining confirmation returns to the unchanged ongoing game.
3. Confirming abort opens the Instructor page and shows a success message.
4. The game appears under “Aborted games”.
5. The game is no longer available through “Resume ongoing game”.
6. Dashboard aggregate results do not include the aborted game.
7. Round coverage shows “Aborted” before deletion.
8. Declining deletion confirmation preserves the game.
9. Confirming deletion removes the game.
10. Round coverage then shows “Open” and the round can be started again for the course.
11. A regularly completed game cannot be deleted through this function.

## 11. Reference to the Domain Specification

The specification documents dated 31 August 2026 are authoritative for this development state:

- `Syzeteo-L-US-DE.md` / `Syzeteo-L-US-EN.md`
- `Syzeteo-RANF-etc-DE.md` / `Syzeteo-RANF-etc-EN.md`
- `Syzeteo-Use-Cases-US26-DE.md` / `Syzeteo-Use-Cases-US26-EN.md`
- `Syzeteo-Traceability-Matrix-DE.md` / `Syzeteo-Traceability-Matrix-EN.md`
