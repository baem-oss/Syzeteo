# Syzeteo – US #24: Gespielte Fragen protokollieren

**Stand:** 29.10.2026 · **Status:** neun direkte automatisierte Teilnachweise, fachliche Sonderregeln beschlossen, UI-Freigabe PASS (vom Nutzer gemeldet).

## Fachliche Entscheidungen vom 29.10.2026

- **„Gespielt“** heißt: Die Fachfrage ist **abschließend behandelt** (`resolved=1`), nicht lediglich aufgedeckt. Das gilt unabhängig davon, ob eine reguläre Frage richtig oder falsch beantwortet wurde.
- Die Protokollübersicht ordnet verwendete Fachfragen ihrem **Kurs und ihrer Runde** zu. Der historische Fragetext stammt aus dem Snapshot der gespielten Karte.
- In einem **abgebrochenen** Spiel bleiben bereits abgeschlossene Fragen mit Status `aborted` sichtbar; bei ausdrücklicher **Löschung** des Spiels verschwinden seine Protokolleinträge.
- Die **Challenge Card** ist keine Fachfrage und gehört nicht in das Fragenprotokoll.
- Die **letzte Instructor-Fachfrage** gehört nach abschließender Behandlung in das Fragenprotokoll, aber **nicht** in die statistische Fragenauswertung (US #28).
- Der **CSV-Export** enthält dieselbe Kurs-/Rundenfilterung wie die Tabellenansicht; UTF-8-BOM bleibt erhalten.

**Maschinenlesbares, derzeit einzig registriertes Kriterium:** `AC-US24-01`, Status `legacy_provisional`. Die **S-US24-xx** unten sind die fachlich abgestimmten Szenarien; sie sind **keine zusätzlichen, bereits in JSON registrierten AC-IDs**.

## Akzeptanzszenarien und direkte Tests

| Szenario | Nachbedingung | Automatischer Nachweis |
|---|---|---|
| S-US24-01 | Nur abschließend behandelte Fachfragen, keine bloß aufgedeckten oder Challenge Cards | `test_us24_unresolved_and_challenge_cards_not_in_question_protocol` |
| S-US24-02 | Kurs, Runde, Position und Frage bleiben korrekt zugeordnet | `test_us24_resolved_questions_have_course_round_and_position` |
| S-US24-03 | Historischer Fragetext bleibt trotz Änderung des Fragenpools erhalten | `test_us24_question_snapshot_is_independent_of_pool_changes` |
| S-US24-04 | Abbruchstatus/Zeitstempel sichtbar; Einträge bleiben bis zur Löschung bestehen | `test_us24_protocol_has_status_and_resolution_timestamp`, `test_us24_aborted_game_keeps_resolved_questions_until_deleted` |
| S-US24-05 | CSV enthält die gefilterten Zeilen, korrekte Sonderzeichen und Header auch ohne Treffer | `test_us24_csv_contains_only_course_and_round_filtered_rows`, `test_us24_csv_without_filters_preserves_all_rows_and_text`, `test_us24_filtered_empty_result_exports_header_only` |
| S-US24-06 | Letzte Instructor-Fachfrage ist protokolliert, aber aus der Statistik ausgeschlossen | `test_us24_final_instructor_question_is_logged_but_not_analyzed` |

Tests liegen in `test_us24_question_protocol.py` (sechs Methoden) und `test_us24_csv.py` (drei Methoden). Beide sind im Story-Mapping eingetragen. CSV-Filterung und -Kodierung werden über die auch von `app.py` verwendeten Funktionen aus `question_protocol.py` geprüft.

## UI-Abnahme

**PASS – vom Projektverantwortlichen am 29.10.2026 im Chat erteilt.** Keine eigenständige Browserprüfung durch den Assistenten; Browser-Version, tatsächliche Auflösung/Zoomstufe, Einzelbeobachtungen und Screenshots wurden nicht vorgelegt. Die Referenzumgebung lautet 1920×1080 bei 100 % Zoom.

## Grenzen des Nachweises

- Die neun automatisierten Tests belegen die genannten Teilaspekte, aber keine vollständige End-to-End-Abnahme aller UI-Varianten und fachlichen Randfälle.
- Der bestehende generische Kriterien-Wortlaut in `Syzeteo-Akzeptanzkriterien.json` wird in dieser **Dokumentationsphase** nicht verändert. Die fachliche Aufschlüsselung in zusätzliche registrierte Kriterien gehört zu Phase 2 und unterliegt dem CI-Gate.
- Historische, mittlerweile geklärte Entscheidungen werden nicht mehr als „offen“ geführt.

Siehe `Syzeteo-Testabdeckung-Review-DE.md` und `Syzeteo-TDD-Kriterien-Governance-DE.md`.
