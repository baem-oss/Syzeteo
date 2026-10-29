# Syzeteo – Technical Baseline 1.1.0

Date: 2026-09-03

## 1. Purpose

This document defines the technical baseline for Syzeteo 1.1.0. Version 1.1.0 extends the published 1.0.0 baseline with US #26 “Abort and Delete Game” and GR #11.

## 2. Runtime and deployment

- application framework: Streamlit
- implementation language: Python
- persistence: SQLite
- supported deployment path: Docker / Docker Compose
- default host port: `8502`
- application version: `1.1.0`

## 3. Persistence and compatibility

- database file: `syzeteo.sqlite3`
- default data directory: `./persistent`
- optional environment variable: `SYZETEO_DATA_DIR`
- SQLite schema version: `PRAGMA user_version = 2`

Syzeteo 1.1.0 does not change the database schema from 1.0.0. No data migration is required. Existing 1.0.0 databases can be used unchanged.

The existing textual game status may additionally contain the language-neutral value `aborted`. This new domain state is created only when an Instructor explicitly aborts a running game.

## 4. Game states

Syzeteo 1.1.0 distinguishes:

- `running`: running game;
- `finished`: regularly completed game;
- `aborted`: aborted game.

An aborted game:

- is no longer considered running;
- cannot be resumed;
- does not count as a regularly completed result;
- retains its game-specific data until explicitly deleted;
- can be deleted from the Instructor page;
- frees the respective course/round combination after deletion.

Regularly completed games cannot be deleted through this function.

## 5. Deletion behavior

Deletion under US #26 is restricted to games with status `aborted`. Deleting such a game removes the game and data exclusively associated with it through the existing foreign-key relations using `ON DELETE CASCADE`.

The history of regularly completed games remains protected.

## 6. Round coverage and results

Round coverage distinguishes `open`, `running`, `played`, and `aborted`.

Aborted games are excluded from regular team and course results. After deletion of an aborted game, the corresponding round is open again for that course.

## 7. Navigation

Programmatic page changes use a pending navigation value that is applied before the Streamlit navigation widget is instantiated. This avoids modifying the session-state key of an already-created widget during the same Streamlit run.

## 8. Internationalization

The official `locales/en.json` and `locales/de.json` catalogs each contain 493 identical translation keys. The US #26 UI, including status labels, confirmation dialogs, deletion dialogs, and error messages, is fully available in both languages.

## 9. Tests and acceptance

Syzeteo 1.1.0 was verified with:

- complete automated test suite: **62/62 tests passed**;
- five domain tests for abort/delete behavior;
- one regression test for Streamlit navigation;
- staged deployment using a copy of the existing dataset;
- manual smoke test of “Abort Game” and “Delete Game” use cases;
- productive cutover without schema change;
- successful post-cutover HTTP, SQLite integrity, and foreign-key checks;
- unchanged inventory counts before and after cutover.

## 10. Release status

Syzeteo 1.1.0 is the released successor to Syzeteo 1.0.0. Development states `1.1.0-dev1` and `1.1.0-dev2` are not separate releases.
