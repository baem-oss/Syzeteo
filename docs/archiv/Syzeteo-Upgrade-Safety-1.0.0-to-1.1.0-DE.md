# Syzeteo – Sicheres Upgrade auf 1.1.0

Stand: 03.09.2026

## Ziel

US #26 „Spiel abbrechen und löschen“ wird in den bestehenden Syzeteo-Stand integriert, ohne den vorhandenen Datenbestand unnötig zu verändern oder zu gefährden.

## Technische Ausgangslage

- Die Anwendung verwendet weiterhin SQLite.
- Das Datenbankschema bleibt auf `PRAGMA user_version = 2`.
- Für US #26 ist keine Schemaänderung und keine Datenmigration erforderlich.
- Der bestehende Wert `games.status` ist bereits als `TEXT` definiert; `aborted` kann deshalb ohne Änderung der Tabellenstruktur verwendet werden.
- Abgebrochene Spiele bleiben einschließlich ihrer spielbezogenen Daten erhalten, bis der Instructor sie ausdrücklich löscht.
- Bei der Löschung eines abgebrochenen Spiels werden ausschließlich die diesem Spiel zugeordneten Daten über die vorhandenen Fremdschlüsselbeziehungen mit `ON DELETE CASCADE` entfernt.
- Regulär abgeschlossene Spiele können über US #26 nicht gelöscht werden.

## Sicherheitsprinzip für die Übernahme

Die produktive SQLite-Datei wird nicht zum Testen der neuen Version verwendet. Vor einem Cutover wird eine konsistente Kopie der produktiven Datenbank erstellt und ausschließlich mit dieser Kopie geprüft.

## Vor dem Cutover

1. Syzeteo kontrolliert beenden, sodass keine Schreibzugriffe auf die SQLite-Datenbank stattfinden.
2. Eine vollständige Sicherung des Verzeichnisses `persistent/` erstellen.
3. Zusätzlich eine konsistente SQLite-Sicherung von `syzeteo.sqlite3` erstellen.
4. Auf der Sicherung `PRAGMA integrity_check` und `PRAGMA foreign_key_check` ausführen.
5. Anzahl der Kurse, Studierenden, Runden und Spiele sowie die Spielstatus vor dem Upgrade protokollieren.
6. Die neue Anwendung zunächst gegen eine Kopie der Datenbank starten.
7. Die automatisierten Tests sowie einen manuellen Smoke-Test für die bestehenden Kernfunktionen und US #26 durchführen.
8. Nach dem Test die Datenbestände und Integritätsprüfungen erneut vergleichen.

## Cutover

Erst wenn die Prüfung auf der Datenbankkopie erfolgreich ist, wird die produktive Anwendung auf den neuen Code umgestellt. Das bestehende `persistent/`-Verzeichnis wird dabei unverändert weiterverwendet.

## Rückfall

Falls nach dem Cutover ein Problem auftritt:

1. Anwendung beenden.
2. Vorherigen Anwendungscode wiederherstellen.
3. Falls seit dem Cutover keine produktiven Änderungen erfolgt sind, kann die bestehende Datenbank unverändert weiterverwendet werden.
4. Falls produktive Änderungen erfolgt sind oder Zweifel an der Datenintegrität bestehen, die vor dem Cutover erstellte Sicherung wiederherstellen.

## Abnahmekriterien

- `PRAGMA integrity_check` ergibt `ok`.
- `PRAGMA foreign_key_check` liefert keine Befunde.
- Schema-Version bleibt `2`.
- Bestehende Kurse, Studierende, Runden und abgeschlossene Spiele bleiben erhalten.
- Bestehende laufende Spiele bleiben als laufend verfügbar.
- Ein laufendes Testspiel kann abgebrochen werden.
- Ein abgebrochenes Spiel erscheint auf der Instructor-Seite und kann gelöscht werden.
- Ein regulär abgeschlossenes Spiel kann über diese Funktion nicht gelöscht werden.
- Nach Löschung eines abgebrochenen Spiels gilt die betreffende Runde für den Kurs wieder als offen.
- Die vollständige automatisierte Testsuite ist erfolgreich.


## Zusätzlicher Abnahmepunkt für 1.1.0

Nach erfolgreichem Spielabbruch muss die Navigation ohne Streamlit-Session-State-Fehler auf die Instructor-Seite erfolgen.
