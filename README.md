# Syzeteo

**Knowledge. Teams. Rounds.**

*An open-source team-based active recall game for the classroom.*

Syzeteo is a Streamlit-based classroom game for structured knowledge review in two teams. Instructors manage courses, students, questions and rounds, run the game, and track results at team and course level.

## Why Syzeteo?

The name derives from the Ancient Greek **συζητέω (syzēteō)**, meaning *to seek or examine together* and, depending on context, *to discuss or question together*. That captures the core idea of the application: students actively recall knowledge, answer questions, and learn together in teams.

## Core principles

- two teams and strict team alternation;
- eight Question Cards plus one Challenge Card per round;
- configurable random or manual regular player selection from player 2 onward;
- one regular turn per person and round;
- Team Assist as an exception: helping through Team Assist does not count as a regular turn;
- the final remaining card is always answered by the Instructor and scores 0 points;
- no individual performance analytics: names are used only for game organization;
- running games can be aborted; only aborted games can be deleted by the Instructor;
- persistent SQLite storage and Docker-based deployment;
- complete English and German application UI.

## Quick start with Docker

```bash
docker compose up -d --build
```

By default Syzeteo is available on host port `8502`.

On the first start, create the single Instructor account in the application. A new installation creates `persistent/syzeteo.sqlite3` automatically.

## Local start

Requirements: Python 3.12 or a compatible Python 3.x environment.

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Internationalization

English and German are available through JSON language catalogs, with English as the reference and fallback language. Language selection is intentionally exposed only on the login/first-run screen and in Instructor Settings; the saved default is reused for future logins.

All application UI pages are localized. Stable internal IDs and status codes are used for navigation, filters, configuration issues, undo actions and domain errors. Question Pool content remains user-provided content and is intentionally not translated.

## Game model

A round contains exactly eight Question Cards plus one Challenge Card. Cards are shuffled for every game. The two teams alternate strictly.

The Challenge Card uses its special scoring rules during normal play. If any card is the last remaining card, the Instructor answers it and no points are awarded, regardless of card type.

Each person may take only one regular turn per round. A Team Assist does not count as a regular turn, so an assisting person remains eligible for a later regular turn.

## Privacy by design

Syzeteo does not store or evaluate individual student performance. Student names are used only for organizational purposes such as team assignment, attendance, player selection and Team Assist. Scores, statistics and results are stored and shown only at team or course level.

## Question Pool import and export

Syzeteo JSON exports and imports use:

```json
{
  "format": "Syzeteo question pool",
  "version": 1
}
```

Question Pool imports and exports use the Syzeteo format shown above.

## Data directory and database

The optional environment variable is:

```text
SYZETEO_DATA_DIR
```

If it is not set, Syzeteo uses `./persistent`. The database file is always named:

```text
syzeteo.sqlite3
```

Syzeteo 1.1.0 uses SQLite schema version `2` (`PRAGMA user_version`). Application version and SQLite schema version are intentionally independent. The persisted domain identifiers include `challenge`, `team_assist_used`, `team1_assist_used` and `team2_assist_used`.


## Upgrade from 1.0.0

Syzeteo 1.1.0 keeps SQLite schema version `2`. No database migration is required. Existing 1.0.0 data can be reused unchanged. A consistent backup of `persistent/` is nevertheless recommended before changing application code.

## Tests

```bash
python -m unittest discover -v
```

The release contains regression tests, release-acceptance tests and internationalization consistency tests. The Syzeteo 1.1.0 release suite contains **62 automated tests**.

## Documentation

The `docs/` directory contains the complete requirements and traceability set in German and English, the technical baseline, and the internationalization specification for Syzeteo 1.1.0.

## Repository hygiene

The public repository must not contain productive databases, SQLite WAL/SHM files, backups, real student lists, account data or teaching content whose publication rights are unclear. The bundled student CSV contains only fictional demonstration names.

## License

Syzeteo is licensed under the **Apache License 2.0**. See [`LICENSE`](LICENSE).

The Apache License 2.0 applies to the Syzeteo source code and original project documentation. Before publishing or redistributing additional question sets, teaching materials or other third-party content, verify that you have the necessary rights for that content.
