# Syzeteo – Phase 2: TDD-Pilot US #24 (Vorbereitung)

Stand: 29.10.2026  
Status: **Definition von „gespielt“ und Abbruchregel beschlossen; übrige Abnahmekriterien teilweise offen**  
Quelle: `docs/Syzeteo-L-US-DE.md` (US #24), `docs/Syzeteo-RANF-etc-DE.md` (GR #01, #02, #09, #11; NFANF #02), `storage.py::protocol_rows`, `app.py` (PAGE_QUESTION_LOG).

## Ziel

Gespielte Fachfragen pro Kurs und Runde nachvollziehbar protokollieren und den angezeigten, optional gefilterten Bestand als CSV exportieren. Akzeptanzkriterien werden vor der Testimplementierung fachlich abgestimmt.

## Befund (Quellcodeprüfung)

- `protocol_rows(conn)` liefert derzeit **aufgelöste** Fachfragekarten (`card_type='question' AND resolved=1`), nicht lediglich aufgedeckte Karten.
- Die Abfrage unterscheidet Ergebnisse aus laufenden, abgebrochenen und abgeschlossenen Spielen über das Statusfeld; die UI zeigt dieses Feld an.
- Die Werte für Fragennummer, Position, Lerneinheit, Fragetext, Kurs, Runde, Status und Datum werden angezeigt. Der Fragetext stammt aus einem Spiel-Snapshot.
- Die UI ermöglicht Kurs- und Rundenfilter; CSV ist UTF-8 mit BOM (`utf-8-sig`) und enthält die aktuell gefilterte Tabelle.
- Die Pipeline-Zuordnungen im Bestands-Mapping sind derzeit Kandidaten, kein nachgewiesener US-24-Akzeptanztest.

## Kandidaten für konkrete Akzeptanzkriterien (noch **nicht** beschlossen)

| ID | Gegeben | Wenn | Dann | Testart |
|---|---|---|---|---|
| AC-US24-01 | Runde mit mehreren Fachfragekarten; eine aufgedeckt, eine gewertet | Instructor öffnet das Fragenprotokoll | Es erscheint nur die gewertete Karte, sofern »gespielt« = gewertet definiert wird | automatisiert |
| AC-US24-02 | Zwei Kurse verwenden dieselbe Runde | Instructor zeigt das Protokoll | Tatsächlich gewertete Fachfragen werden je Kurs und Runde getrennt zugeordnet | automatisiert |
| AC-US24-03 | Eine Frage wurde nach Spielbeginn im globalen Pool geändert | Protokoll wird angezeigt | Historischer Fragetext bleibt der zum Spiel gehörende Snapshot | automatisiert |
| AC-US24-04 | Spiel wurde abgebrochen und noch nicht gelöscht | Protokoll wird angezeigt | Der Eintrag und sein Status folgen der noch zu bestätigenden Abbruchregel | automatisiert |
| AC-US24-05 | Abgebrochenes Spiel wurde ausdrücklich gelöscht | Protokoll wird erneut angezeigt | Seine ausschließlich spielbezogenen Einträge sind entfernt | automatisiert |
| AC-US24-06 | Mehrere Kurse und Runden sind im Protokoll enthalten | Instructor filtert und exportiert | CSV enthält ausschließlich die gefilterte Tabellenansicht | Integration/UI |
| AC-US24-07 | Das Protokoll enthält Sonder- und Abschlusskarten | Instructor zeigt die Übersicht | Umgang mit Challenge Card und letzter Instructor-Karte folgt noch zu klärender fachlicher Definition | automatisiert |

## Offene fachliche Entscheidungen

1. **»Tatsächlich gespielt«:** Bedeutet dies »aufgedeckt« oder erst »gewertet/abgeschlossen«? Der aktuelle Code verwendet `resolved=1`.
2. **Abgebrochene Spiele:** Sollen gewertete Fragen bis zur ausdrücklichen Löschung weiterhin sichtbar sein? Aktuell ja, mit Status `aborted`.
3. **Letzte Instructor-Karte:** Soll eine als letzte Karte aufgedeckte und nicht gewertete Fachfrage im Fragenprotokoll erscheinen? Aktuell ja, weil `resolved=1`; die Auswertung US #28 schließt sie dagegen ausdrücklich aus.
4. **CSV:** Reicht das aktuelle gefilterte Tabellenexportformat, oder wird ein vollständiger maschinenlesbarer Verlauf mit stabilen Feldnamen erwartet?

## Test- und Implementierungsreihenfolge nach Klärung

1. Fachlich entschiedene Kriterien als eindeutige Given/When/Then-Szenarien finalisieren.
2. Testfälle für `protocol_rows` mit isolierter temporärer Datenbank schreiben; zunächst gegen Bestandsverhalten ausführen und Differenzen dokumentieren (Red).
3. Falls notwendig Implementierung minimal korrigieren (Green) und unveränderte Historie absichern.
4. CSV-Filter-/Exportpfad gesondert testen; sichtbare Darstellung hybrid manuell abnehmen.
5. Mapping `Syzeteo-Akzeptanztests-Mapping.json` um **tatsächlich verifizierte** Testreferenzen erweitern; Akzeptanzkriteriumsänderungen ebenfalls im CI-Gate berücksichtigen.
6. Gesamte `regression_pipeline.py --native --release` ausführen, Pull Request erstellen.

## Abnahme

Ein Kriterium gilt erst als automatisiert abgedeckt, wenn der Test dessen Nachbedingung konkret prüft, reproduzierbar läuft und im Traceability-Mapping aufgeführt ist. Andere bestehende Tests behalten den Status »Kandidat«.

## Fachliche Festlegung vom 29.10.2026

- „Gespielt“ bedeutet **abschließend behandelt / resolved=1**, nicht lediglich aufgedeckt.
- Eine abgeschlossene Fachfrage wird unabhängig von richtiger oder falscher Wertung protokolliert.
- Bei Abbruch bleiben bereits abgeschlossene Fragen mit Status `aborted` bis zur ausdrücklichen Löschung nachvollziehbar.
- Durch die Löschung des abgebrochenen Spiels werden dessen Protokolleinträge vollständig entfernt.
- Der technische Nachweis erfolgt durch `test_us24_question_protocol.py`, einschließlich `test_us24_aborted_game_keeps_resolved_questions_until_deleted`.
- Die Interpretation der letzten Instructor-Karte und der CSV-Abnahme bleibt vorläufig; daraus wird keine geänderte Fachlogik abgeleitet.

## CSV-Abnahme – Implementierung 29.10.2026

Die bereits vorhandene Tabellenfilterung und der CSV-Export wurden ohne beabsichtigte Verhaltensänderung in `question_protocol.py` extrahiert. `app.py` verwendet diese beiden Funktionen nun unmittelbar. `test_us24_csv.py` prüft:

- gemeinsame Kurs- und Rundenfilterung für angezeigte und exportierte Zeilen;
- vollständigen Export ohne Filter, einschließlich Komma und Zeilenumbruch in Fragetexten;
- leere Trefferliste mit beibehaltenen CSV-Spaltenüberschriften;
- UTF-8 mit BOM, wie bislang von der Oberfläche erzeugt.

Die manuelle UI-Abnahme bleibt offen; auch die Frage, wie die letzte Instructor-Karte fachlich zu behandeln ist, wird dadurch nicht entschieden.

## Beschluss: letzte Instructor-Karte (29.10.2026)

Eine als letzte Karte abschließend behandelte Fachfrage wird gemäß US #24 im Fragenprotokoll dokumentiert, auch wenn der Instructor sie ohne Punkte beantwortet. Sie ist **kein studentischer Beantwortungsversuch** und bleibt gemäß GR #13 aus der statistischen Fragenauswertung (US #28) ausgeschlossen. Eine Challenge Card ist weiterhin keine Fachfrage und wird nicht in das Fragenprotokoll aufgenommen.

Automatisierter Nachweis: `test_us24_question_protocol.py::test_us24_final_instructor_question_is_logged_but_not_analyzed`.

## UI-Abnahme – Freigabe vom 29.10.2026

**Status: PASS (ausdrückliche Nutzerfreigabe im Chat).** Die UI-Abnahme wurde vom Projektverantwortlichen als bestanden gemeldet. Keine eigenständige Browserprüfung durch den Assistenten und kein separat übermitteltes Prüfprotokoll. Browser-Version, tatsächlich verwendete Auflösung und Zoomstufe sind nicht nachgewiesen. Die zugehörigen automatisierten Regressionstests bleiben unabhängige Nachweise. Für US #24 gilt diese Freigabe als gemeldete manuelle UI-Abnahme; weitergehende fachliche Vollabdeckung wird daraus nicht abgeleitet.
