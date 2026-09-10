# Syzeteo – Technische Baseline 1.1.1

Datum: 2026-09-10

## 1. Status und Zweck

`1.1.1` ist die Syzeteo-1.1.1-Version auf Basis von Syzeteo 1.1.0. Er enthält die Rendering-Korrekturen für Fragen, US #27 „Teamnamen verwalten“, GR #12 „Kursbezogene Teamnamen“, den deterministischen Schema-3-Startup-Preflight, die lokalisierte Duplikatprüfung für Studierendennamen, US #28 „Fragen auswerten“ mit GR #13 „Fragenbezogene Ergebnisaggregation“ sowie die Korrektur der Runden-Fragenauswahl.

## 2. Laufzeit und Deployment

- Anwendungsframework: Streamlit 1.54.0
- Implementierungssprache: Python
- Persistenz: SQLite
- Deployment: Docker / Docker Compose
- Datenverzeichnis: `SYZETEO_DATA_DIR`, Standard `./persistent`
- Datenbankdatei: `syzeteo.sqlite3`
- Anwendungsversion: `1.1.1`
- SQLite-Schemaversion: `PRAGMA user_version = 3`

## 3. Schemaänderung 2 → 3

Schema 3 ergänzt ausschließlich additive Spalten:

- `courses.team1_name`
- `courses.team2_name`
- `games.team1_name_snapshot`
- `games.team2_name_snapshot`

Bestehende Datenbanken mit Schema 2 werden beim Containerstart vor dem Start von Streamlit automatisch und idempotent auf Schema 3 erweitert. Bestehende Kurse und Spiele erhalten die bisherigen Anzeigenamen `Team 1` und `Team 2`. Bestehende fachliche Daten werden nicht gelöscht oder umgeschrieben.

## 4. Teamnamen

- Teamnamen sind kursbezogen.
- Beide Namen müssen nicht leer und innerhalb des Kurses verschieden sein.
- Interne Teamkennungen bleiben `1` und `2`.
- Teamnamen können beim Anlegen eines Kurses festgelegt und später geändert werden.
- Während für den Kurs ein Spiel mit Status `running` existiert, ist die Änderung gesperrt.
- Beim Start eines Spiels werden beide Teamnamen als Snapshots im Spiel gespeichert.
- Spätere Umbenennungen verändern laufende, abgebrochene oder abgeschlossene Spiele nicht rückwirkend.

## 5. Rendering und Rundenbearbeitung

Frage- und Musterantworttexte werden als Nutzdaten behandelt und nicht als Markdown interpretiert. Nummerierte Zeilen bleiben sowohl auf Fragekarten als auch in geöffneten Fragen und in der Rundenübersicht wortgetreu erhalten. Die Runden-Fragenauswahl verwendet kein Streamlit-Auswahlmaximum mehr, dessen Overlay den Speichern-Button verdecken konnte; die Domänenlogik erzwingt weiterhin exakt acht Fachfragen.

## 6. Internationalisierung

- Offiziell ausgeliefert werden `en.json` und `de.json`.
- Beide Kataloge besitzen denselben Schlüsselbestand und kompatible Platzhalter.
- Optional installierte vollständige lokale Präsentationsprofile werden als eigenständige Locale-IDs unterstützt.
- Die aufgedeckte Challenge Card bezieht Titel und Unterzeile aus dem aktiven Katalog.
- Domänenwerte, Datenmodell, Spielregeln und das technische Question-Pool-Austauschformat bleiben sprachneutral.

## 7. Fragenauswertung

- Die Auswertung ist in die bestehende Seite „Fragenprotokoll“ integriert.
- Der Instructor kann zwischen einem einzelnen Kurs und einer kursübergreifenden Aggregation wählen.
- Ausgewertet werden ausschließlich Fachfragekarten aus Spielen mit Status `finished`.
- Challenge Card und die letzte, vom Instructor beantwortete Karte werden ausgeschlossen.
- Team-Assist-Antworten zählen als normale Beantwortungsversuche.
- Kennzahlen pro gespielter Fragefassung: Beantwortungen, richtig, falsch und Erfolgsquote.
- Geänderte Fragefassungen werden anhand von `question_id` plus gespeichertem `question_text_snapshot` getrennt ausgewertet.
- Es werden keine Studierendennamen oder individuellen Leistungsdaten ausgewertet.
- CSV-Export ist verfügbar.

## 8. Repository-Hygiene

`persistent/`, SQLite-Dateien, WAL/SHM-Dateien und Backups sind über `.dockerignore` vom Docker-Build-Kontext ausgeschlossen. Der Release-Test REL-10 prüft zusätzlich, dass keine persistenten Datenbankdateien in den Release-Baum gelangen.

## 9. Verifikation

Der Release enthält Domänen-, Migrations-, Rendering-, Release-, Navigations-, Authentifizierungs- und i18n-Tests. Geprüft werden insbesondere:

- Teamnamen-Validierung, Änderungssperre und unveränderliche Spiel-Snapshots;
- automatische Migration einer Schema-2-Datenbank auf Schema 3 ohne Datenverlust;
- fail-closed Startup-Preflight bei falscher Schemaversion oder Foreign-Key-Verletzungen;
- wortgetreues Fragen-Rendering;
- lokalisierte Duplikatfehler für Studierendennamen;
- Schlüssel- und Platzhalterparität von `en` und `de`;
- Unterstützung optional installierter lokaler Präsentationsprofile;
- kursbezogene und kursübergreifende Fragenauswertung ohne Individualauswertung;
- Domänenvalidierung von exakt acht Fachfragen pro Runde.
