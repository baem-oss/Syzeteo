# Syzeteo – Technische Baseline 1.1.0-dev1

Datum: 2026-08-31

## 1. Status und Zweck

Dieses Dokument beschreibt den Entwicklungsstand **Syzeteo 1.1.0-dev1** auf Basis der veröffentlichten Version 1.0.0. Der Stand implementiert US #26 „Spiel abbrechen und löschen“ einschließlich GR #11 und der zugehörigen Use Cases.

`1.1.0-dev1` ist ein Entwicklungsstand und kein veröffentlichtes Release.

## 2. Laufzeit und Deployment

Die technische Basis von Syzeteo 1.0.0 bleibt unverändert:

- Anwendungsframework: Streamlit
- Implementierungssprache: Python
- Persistenz: SQLite
- Deployment: Docker / Docker Compose
- Standard-Host-Port: `8502`
- Anwendungsversion: `1.1.0-dev1`

## 3. Persistenz und Kompatibilität

- Datenbankdatei: `syzeteo.sqlite3`
- Standard-Datenverzeichnis: `./persistent`
- optionale Environment-Variable: `SYZETEO_DATA_DIR`
- SQLite-Schemaversion: `PRAGMA user_version = 2`

Für US #26 ist **keine Änderung des SQLite-Schemas erforderlich**. Die bestehende Spalte `games.status` ist als `TEXT` definiert und kann den zusätzlichen sprachneutralen Domänenstatus `aborted` aufnehmen. Die Schemaversion bleibt deshalb `2`.

Bestehende Datenbanken der veröffentlichten Version 1.0.0 können ohne Datenmigration weiterverwendet werden. Die bestehende Migrationsrandbedingung RANF #01 bleibt bestehen.

## 4. Spielstatus

Für Spiele werden in diesem Entwicklungsstand folgende fachlich relevante Statuswerte verwendet:

| Status | Bedeutung |
|---|---|
| `running` | laufendes Spiel; kann fortgesetzt oder abgebrochen werden |
| `finished` | regulär abgeschlossenes Spiel; fließt in Ergebnisse ein und ist über US #26 nicht löschbar |
| `aborted` | abgebrochenes Spiel; kann nicht fortgesetzt werden, fließt nicht in reguläre Ergebnisse ein und kann auf der Instructor-Seite gelöscht werden |

Der fachliche Übergang für US #26 lautet:

`running` → `aborted` → gelöscht

Ein direkter Löschpfad von `running` oder `finished` über US #26 ist nicht zulässig.

## 5. Abbruch eines Spiels

Die Domänenfunktion `abort_game(conn, game_id)`:

- akzeptiert ausschließlich vorhandene Spiele mit Status `running`;
- setzt den Status atomar auf `aborted`;
- lässt alle bis zum Abbruch vorhandenen spielbezogenen Daten zunächst erhalten;
- entfernt das Spiel aus der Menge der fortsetzbaren laufenden Spiele;
- verändert keine regulär abgeschlossenen Spiele.

In der Spielansicht steht dafür die Funktion „Spiel abbrechen“ / „Abort game“ mit Bestätigung zur Verfügung. Nach erfolgreichem Abbruch wechselt die Anwendung auf die Instructor-Seite.

## 6. Löschen eines abgebrochenen Spiels

Die Domänenfunktion `delete_aborted_game(conn, game_id)`:

- akzeptiert ausschließlich vorhandene Spiele mit Status `aborted`;
- löscht den Datensatz aus `games` atomar;
- löscht über die bestehenden Fremdschlüssel mit `ON DELETE CASCADE` die ausschließlich zum Spiel gehörenden Einträge aus `game_roster`, `game_cards` und `game_undo`;
- lässt Kurs, Studierende, Runde, Lerneinheiten und globalen Fragenpool unverändert;
- macht durch Wegfall der bestehenden Eindeutigkeitsbelegung `(round_id, course_id)` die betreffende Runde für den Kurs wieder startbar.

Abgebrochene Spiele werden auf der Instructor-Seite angezeigt und können dort nach Bestätigung gelöscht werden. Regulär abgeschlossene Spiele werden über diese Funktion nicht angeboten und von der Domänenfunktion zurückgewiesen.

## 7. Auswertungen und Rundenabdeckung

- `course_scoreboard()` wertet weiterhin ausschließlich Spiele mit Status `finished` aus. Abgebrochene Spiele verändern daher weder Team-Gesamtpunkte noch Anzahl regulär gespielter Spiele, Siege oder Unentschieden.
- Die Rundenabdeckung unterscheidet `open`, `running`, `aborted` und `played`.
- Solange ein abgebrochenes Spiel noch vorhanden ist, wird die Kombination aus Runde und Kurs als `aborted` angezeigt.
- Erst nach dem Löschen des abgebrochenen Spiels wird die Kombination wieder `open`.
- Abgebrochene Spiele werden nicht als fortsetzbare Spiele angeboten.

## 8. Internationalisierung

Die neuen UI-Texte und Fehlermeldungen sind in den beiden offiziellen Sprachkatalogen Englisch und Deutsch enthalten. Dazu gehören insbesondere:

- Status „Aborted“ / „Abgebrochen“;
- Abbruchdialog und Bestätigung;
- Bereich „Aborted games“ / „Abgebrochene Spiele“ in den Instructor Settings;
- Löschdialog und Bestätigung;
- sprachneutrale Storage-Fehler für unzulässige Abbruch- und Löschoperationen.

Die bestehenden i18n-Konsistenztests prüfen weiterhin identische Schlüsselbestände und kompatible Platzhalter.

## 9. Automatisierte Verifikation

Der Build des Entwicklungsstands wurde mit Python 3.12 gegen die vollständige automatisierte Testsuite geprüft:

- **61/61 Tests erfolgreich**;
- davon **5 neue Tests** speziell für US #26;
- geprüft werden insbesondere:
  - `running` → `aborted`;
  - Ausschluss abgebrochener Spiele aus regulären Ergebnissen;
  - Abbruch nur für laufende Spiele;
  - Löschung nur für abgebrochene Spiele;
  - Cascade-Löschung der spielbezogenen Daten;
  - erneute Startbarkeit der Runde nach Löschung;
  - bestehende Regression-, Release- und i18n-Prüfungen.

Die automatisierte Suite enthält keine browserbasierte End-to-End-Prüfung der Streamlit-Interaktion. Die UI-Integration ist daher zusätzlich durch einen manuellen Smoke Test im Zielsystem zu prüfen.

## 10. Abnahmepunkte für den manuellen Smoke Test

1. Ein laufendes Spiel zeigt „Spiel abbrechen“.
2. Verwerfen der Bestätigung führt zurück zum unveränderten laufenden Spiel.
3. Bestätigter Abbruch öffnet die Instructor-Seite und zeigt eine Erfolgsmeldung.
4. Das Spiel erscheint dort unter „Abgebrochene Spiele“.
5. Das Spiel ist nicht mehr über „Laufendes Spiel fortsetzen“ erreichbar.
6. Dashboard-Gesamtergebnisse berücksichtigen das abgebrochene Spiel nicht.
7. Die Rundenabdeckung zeigt vor Löschung „Abgebrochen“.
8. Verwerfen der Löschbestätigung erhält das Spiel.
9. Bestätigte Löschung entfernt das Spiel.
10. Die Rundenabdeckung zeigt danach „Offen“ und die Runde kann für den Kurs erneut gestartet werden.
11. Ein regulär abgeschlossenes Spiel kann über diese Funktion nicht gelöscht werden.

## 11. Referenz auf die fachliche Spezifikation

Maßgeblich für diesen Entwicklungsstand sind die Spezifikationsdokumente vom 31.08.2026:

- `Syzeteo-L-US-DE.md` / `Syzeteo-L-US-EN.md`
- `Syzeteo-RANF-etc-DE.md` / `Syzeteo-RANF-etc-EN.md`
- `Syzeteo-Use-Cases-US26-DE.md` / `Syzeteo-Use-Cases-US26-EN.md`
- `Syzeteo-Traceability-Matrix-DE.md` / `Syzeteo-Traceability-Matrix-EN.md`
