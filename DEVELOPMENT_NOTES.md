# Syzeteo 1.1.0-dev1

Development state, 31 August 2026.

This system state implements US #26 / GR #11: an Instructor can abort an ongoing game, and an aborted game can subsequently be deleted from Instructor Settings. Aborted games are not resumable and do not contribute to regular result totals. The round remains marked as aborted until the game is deleted; after deletion, the round is open again for the course.

The SQLite schema remains at version 2. Existing Syzeteo 1.0.0 databases require no schema migration.

Automated verification: 61/61 tests passed in GitHub Actions, including five new tests for the abort/delete lifecycle. A manual Streamlit smoke test remains required before treating this development state as a release candidate.
