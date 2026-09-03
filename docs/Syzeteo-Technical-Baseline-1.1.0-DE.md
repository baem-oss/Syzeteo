# Syzeteo – Technische Baseline 1.1.0

Datum: 2026-09-03

## 1. Zweck

Dieses Dokument definiert die technische Baseline für Syzeteo 1.1.0. Version 1.1.0 erweitert die veröffentlichte Baseline 1.0.0 um US #26 „Spiel abbrechen und löschen“ und GR #11.

## 2. Laufzeit und Deployment

- Anwendungsframework: Streamlit
- Implementierungssprache: Python
- Persistenz: SQLite
- vorgesehener Deployment-Weg: Docker / Docker Compose
- Standard-Host-Port: `8502`
- Anwendungsversion: `1.1.0`

## 3. Persistenz und Kompatibilität

- Datenbankdatei: `syzeteo.sqlite3`
- Standard-Datenverzeichnis: `./persistent`
- optionale Environment-Variable: `SYZETEO_DATA_DIR`
- SQLite-Schemaversion: `PRAGMA user_version = 2`

Syzeteo 1.1.0 führt keine Schemaänderung gegenüber 1.0.0 durch. Es ist keine Datenmigration erforderlich. Bestehende 1.0.0-Datenbanken können unverändert weiterverwendet werden.

Der bestehende Textstatus eines Spiels kann zusätzlich den sprachneutralen Wert `aborted` annehmen. Dieser neue fachliche Zustand wird nur durch den expliziten Abbruch eines laufenden Spiels erzeugt.

## 4. Spielzustände

Syzeteo 1.1.0 unterscheidet fachlich:

- `running`: laufendes Spiel;
- `finished`: regulär abgeschlossenes Spiel;
- `aborted`: abgebrochenes Spiel.

Ein abgebrochenes Spiel:

- gilt nicht mehr als laufend;
- kann nicht fortgesetzt werden;
- zählt nicht als regulär abgeschlossenes Ergebnis;
- bleibt mit seinen spielbezogenen Daten erhalten, bis es explizit gelöscht wird;
- kann auf der Instructor-Seite gelöscht werden;
- gibt nach seiner Löschung die betreffende Kombination aus Kurs und Runde wieder frei.

Regulär abgeschlossene Spiele sind durch diese Funktion nicht löschbar.

## 5. Löschverhalten

Die Löschung nach US #26 ist auf Spiele mit Status `aborted` beschränkt. Beim Löschen werden das Spiel und die ausschließlich diesem Spiel zugeordneten Datensätze über die vorhandenen Fremdschlüsselbeziehungen mit `ON DELETE CASCADE` entfernt.

Die bestehende Datenhistorie regulär abgeschlossener Spiele bleibt geschützt.

## 6. Rundenabdeckung und Ergebnisse

Die Rundenabdeckung unterscheidet `open`, `running`, `played` und `aborted`.

Abgebrochene Spiele werden nicht in reguläre Team- oder Kursergebnisse eingerechnet. Nach der Löschung eines abgebrochenen Spiels gilt die zugehörige Runde für den betreffenden Kurs wieder als offen.

## 7. Navigation

Programmatische Seitenwechsel werden über einen vorgemerkten Navigationswert ausgeführt, der vor der Instanziierung des Streamlit-Navigationswidgets angewendet wird. Damit wird vermieden, den Session-State-Key eines bereits erzeugten Widgets im selben Streamlit-Lauf zu verändern.

## 8. Internationalisierung

Die offiziellen Sprachkataloge `locales/en.json` und `locales/de.json` enthalten jeweils 493 identische Übersetzungsschlüssel. Die US-#26-Oberfläche einschließlich Status, Bestätigungsdialogen, Löschdialogen und Fehlermeldungen ist in beiden Sprachen vollständig enthalten.

## 9. Tests und Abnahme

Für Syzeteo 1.1.0 wurden folgende Prüfungen durchgeführt:

- vollständige automatisierte Testsuite: **62/62 Tests erfolgreich**;
- fünf Domänentests für Abbruch/Löschung;
- ein Regressionstest für die Streamlit-Navigation;
- Stage-Test mit einer Kopie des bestehenden Datenbestands;
- manueller Smoke-Test der Use Cases „Spiel abbrechen“ und „Spiel löschen“;
- produktiver Cutover ohne Schemaänderung;
- anschließende HTTP-, SQLite-Integritäts- und Fremdschlüsselprüfung erfolgreich;
- Bestandszählungen vor und nach dem Cutover unverändert.

## 10. Release-Status

Syzeteo 1.1.0 ist die freigegebene Nachfolgeversion von Syzeteo 1.0.0. Die Entwicklungsstände `1.1.0-dev1` und `1.1.0-dev2` sind keine eigenständigen Releases.
