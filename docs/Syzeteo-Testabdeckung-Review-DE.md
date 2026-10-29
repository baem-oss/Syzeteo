# Syzeteo – Fachliches Review der Testzuordnung
Stand: 29.10.2026

## Prüfprinzip
Die bisher nur anhand von Testnamen erzeugten Zuordnungen wurden konservativ anhand des jeweils geprüften Funktionsverhaltens und der Assertions überarbeitet. Ein grüner Unit-Test belegt **nur seinen konkret geprüften Teilaspekt**, nicht die vollständige fachliche Abnahme der User Story. Die unveränderte Bestands-Baseline ist keine Nachweismatrix.

## Ergebnis
- 29 User Stories insgesamt.
- 26 Stories besitzen wenigstens eine fachlich begründbare **Teilzuordnung**.
- Für **US #10 (Teams zuordnen), US #21 (Spiel fortsetzen), US #24 (Fragen protokollieren)** ist im bisherigen Mapping kein hinreichend direkter Test identifiziert; ihre Referenzen wurden entfernt.
- 59 Story-Test-Links verbleiben als konservative Teilnachweise; Mehrfachzuordnungen sind möglich.
- UI- und End-to-End-Abnahmen sind damit **nicht** als bestanden nachgewiesen.

## Nacharbeit nach fachlicher Priorität
| US | Bereits geprüfter Teilaspekt | Offener Abnahmebedarf |
|---|---|---|
| 01–03 | Startperson, Wahlmodus, Nachzügler | Vollständiger UI-Ablauf |
| 04–06 | Settings-Teilfunktionen, Anmeldung, Zugangsdatenänderung | Vollständiger Seiten- und Zugriffsschutz |
| 07–09 | Archivierung, Duplikate, CSV-Duplikate | Vollständige Kurslöschung, vollständige Studierendenverwaltung, CSV-Sonderfälle |
| 10 | – | Manuelle und zufällige Teamzuordnung |
| 11–14 | Mindestanwesenheit, Lerneinheiten, Löschschutz, Import-Teilpfad | Vollständige CRUD- und Roundtrip-Abläufe |
| 15–20 | Rundenumfang, Start, Punkte-/Spielerlogik, Assist, Challenge, Undo | Alle fachlichen Randfälle und UI |
| 21 | – | Laufendes Spiel nach Neuaufruf korrekt wiederherstellen |
| 22–23 | Fragetext-Rendering, Ausschluss abgebrochener Spiele | Beamer-Full-HD-Abnahme, vollständiges Dashboard |
| 24 | – | Aufgelöste vs. aufgedeckte Fragen, Snapshots, Abbruch/Löschung, Filter/CSV |
| 25–26 | Abbruchstatus, erneuter Rundenstart, Löschschutz | Gesamte Rundenabdeckung und Bestätigungsdialoge |
| 27–29 | Teamnamen/Snapshots, Aggregation, Tic-Tac-Toe | Darstellung in UI und visuelle Abnahme |

## Abnahmeregel
Die vereinbarte inkrementelle TDD-Regel bleibt: Bestandslücken werden ausgegeben und blockieren CI nicht. Für neue/geänderte User Stories ist ein neuer testbarer Nachweis Pflicht. Bei Änderungen nur an Akzeptanzkriterien gibt es derzeit noch keine vollständig automatische Erkennung; das bleibt eine offene technische Nacharbeit.

## Pilot US #24
Siehe `docs/Syzeteo-TDD-Phase2-US24-DE.md`. Die dort genannten fachlichen Entscheidungen müssen bestätigt werden, bevor neue Assertions als verbindliche Akzeptanzkriterien gelten.
