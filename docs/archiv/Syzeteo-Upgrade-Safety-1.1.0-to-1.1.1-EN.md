# Syzeteo – Upgrade Safety 1.1.0 → 1.1.1

Status: 10 September 2026

## Goal

Release `1.1.1` automatically migrates an existing Syzeteo 1.1.0 database from SQLite schema 2 to schema 3. The migration exists solely to introduce course-specific team names and historically stable team-name snapshots.

## Before upgrading

Create a consistent backup of `persistent/` before any productive upgrade. Reverting to older application code should not be treated as a database downgrade; use the pre-upgrade backup for a controlled rollback.

## Automatic migration

When a schema-2 database is opened, the following columns are added if absent:

- `courses.team1_name TEXT NOT NULL DEFAULT 'Team 1'`
- `courses.team2_name TEXT NOT NULL DEFAULT 'Team 2'`
- `games.team1_name_snapshot TEXT NOT NULL DEFAULT 'Team 1'`
- `games.team2_name_snapshot TEXT NOT NULL DEFAULT 'Team 2'`

`PRAGMA user_version` is then set to `3`. The migration is idempotent: existing columns are not added again.

## Preservation of existing data

Existing courses, students, team assignments, learning units, questions, rounds, games, cards, scores, and log data remain unchanged. Because freely chosen team names did not exist before 1.1.1, `Team 1` and `Team 2` are the correct historical defaults for existing courses and games.

## Verification

Automated checks cover:

- `PRAGMA user_version = 3` after migration;
- preservation of existing course and game data;
- correct default team names for migrated records;
- `PRAGMA integrity_check = ok`;
- empty `PRAGMA foreign_key_check`.

## Startup migration gate

The container runs `startup.py` before Streamlit. This opens the configured database through the storage layer, performs the schema migration, and then requires schema version 3, `PRAGMA integrity_check = ok`, and an empty `PRAGMA foreign_key_check`. If any check fails, Streamlit is not started.
