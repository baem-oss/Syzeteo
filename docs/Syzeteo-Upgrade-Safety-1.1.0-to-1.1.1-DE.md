# Syzeteo – Upgrade-Sicherheit 1.1.0 → 1.1.1

Stand: 10.09.2026

## Ziel

Syzeteo `1.1.1` migriert eine bestehende Syzeteo-1.1.0-Datenbank automatisch von SQLite-Schema 2 auf Schema 3. Die Migration dient ausschließlich der Einführung kursbezogener Teamnamen und historisch stabiler Teamnamen-Snapshots.

## Vor dem Upgrade

Vor jedem produktiven Upgrade ist eine konsistente Sicherung von `persistent/` anzulegen. Ein Rückwechsel auf älteren Anwendungscode soll nicht als Datenbank-Downgrade behandelt werden; für einen kontrollierten Rollback ist die vor dem Upgrade erzeugte Sicherung zu verwenden.

## Automatische Migration

Beim Öffnen einer Schema-2-Datenbank werden, sofern noch nicht vorhanden, folgende Spalten additiv ergänzt:

- `courses.team1_name TEXT NOT NULL DEFAULT 'Team 1'`
- `courses.team2_name TEXT NOT NULL DEFAULT 'Team 2'`
- `games.team1_name_snapshot TEXT NOT NULL DEFAULT 'Team 1'`
- `games.team2_name_snapshot TEXT NOT NULL DEFAULT 'Team 2'`

Danach wird `PRAGMA user_version` auf `3` gesetzt. Die Migration ist idempotent: Bereits vorhandene Spalten werden nicht erneut angelegt.

## Erhalt bestehender Daten

Vorhandene Kurse, Studierende, Teamzuordnungen, Lerneinheiten, Fragen, Runden, Spiele, Karten, Spielstände und Protokolldaten bleiben unverändert erhalten. Da vor Version 1.1.1 keine frei wählbaren Teamnamen existierten, bilden `Team 1` und `Team 2` den korrekten historischen Ausgangswert für bestehende Kurse und Spiele.

## Verifikation

Automatisiert geprüft werden:

- `PRAGMA user_version = 3` nach Migration;
- Erhalt bestehender Kurs- und Spieldaten;
- korrekte Default-Teamnamen für migrierte Datensätze;
- `PRAGMA integrity_check = ok`;
- leerer `PRAGMA foreign_key_check`.

## Startup-Migrationsgate

Der Container führt vor Streamlit `startup.py` aus. Dabei wird die konfigurierte Datenbank über die Storage-Schicht geöffnet, die Schemamigration ausgeführt und anschließend Schemaversion 3, `PRAGMA integrity_check = ok` sowie ein leerer `PRAGMA foreign_key_check` verlangt. Bei einem Fehler wird Streamlit nicht gestartet.
