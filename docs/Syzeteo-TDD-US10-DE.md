# Syzeteo – US #10: Akzeptanztests zur Teamzuordnung

Stand: 29.10.2026

## Fachliche Grundlage

US #10: Der Instructor kann Studierende manuell oder zufällig Team 1 beziehungsweise Team 2 zuordnen. Die aktuellen Funktionen sind `update_student` und `randomize_teams` in `storage.py`.

## Direkte automatisierte Akzeptanztests

| ID | Gegeben | Wenn | Dann |
|---|---|---|---|
| AC-US10-01 | Zwei Studierende ohne Team | Eine Person wird manuell Team 2 zugewiesen | Nur diese Person gehört Team 2 an |
| AC-US10-02 | Sieben aktive Studierende | Zufällige Teamzuordnung | Alle sieben sind zugeordnet; Teamgrößen 3 und 4 |
| AC-US10-03 | Aktive und inaktive Studierende sowie ein anderer Kurs | Teams werden zufällig verteilt | Nur aktive Studierende des Zielkurses werden neu zugeteilt |
| AC-US10-04 | Weniger als zwei aktive Studierende | Zufällige Zuordnung wird angefordert | Fachlicher Fehler, keine Teamänderung |
| AC-US10-05 | Studierender mit gültiger Teamzuordnung | Ungültige Teamkennung wird zugewiesen | Fachlicher Fehler; ursprüngliche Zuordnung bleibt erhalten |

Implementiert in `test_us10_team_assignment.py` (isolierte temporäre Datenbank).

## Offene Abnahmepunkte

- Der tatsächliche Instructor-UI-Ablauf ist noch nicht manuell abgenommen.
- Die Unveränderlichkeit der gespeicherten Team-Snapshots bereits gestarteter Spiele wird in anderen bestehenden Tests für Teamnamen behandelt; **eine direkte Prüfung gegen nachträgliche Studierenden-Teamänderungen** fehlt noch.
- Die zufällige Verteilung ist auf eine ausgeglichene Anzahl geprüft, nicht auf statistische Zufälligkeit. Letzteres ist keine fachliche Voraussetzung von US #10.

## Vorgehen

Dieser Commit ändert keine Produktivlogik. Nach grünem CI wird der PR nach Review gemergt; anschließend sollen Akzeptanzkriteriumsänderungen zusätzlich im Traceability-Gate abgesichert werden.
