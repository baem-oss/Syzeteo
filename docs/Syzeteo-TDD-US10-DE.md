# Syzeteo – US #10: Teamzuordnung, Akzeptanznachweise

**Stand:** 29.10.2026 · **Status:** sechs direkte automatisierte Teilnachweise, fünf konkretisierte Kriterien; UI-Freigabe PASS (vom Nutzer gemeldet).

## Fachliche Grundlage

Der Instructor kann Studierende manuell oder zufällig Team 1 beziehungsweise Team 2 zuordnen. Die Implementierung verwendet `storage.py::update_student` und `storage.py::randomize_teams`.

**Verbindliche maschinenlesbare Kriterien:** `AC-US10-01` bis `AC-US10-05` in `Syzeteo-Akzeptanzkriterien.json` (Status `specified_partial`). Jede Zuordnung ist durch mindestens eine direkt referenzierte Testmethode belegt; dies ist keine vollständige Story-Abnahme.

## Automatisierte Szenarien

| Szenario | Gegeben | Wenn | Dann | Direkter Test |
|---|---|---|---|---|
| AC-US10-01 | Zwei Studierende ohne Team | Eine Person wird Team 2 zugeordnet | Nur diese Person hat Team 2 | `test_us10_manual_assignment_changes_only_selected_student` |
| AC-US10-02 | Sieben aktive Studierende | Zufällige Zuordnung | Teamgrößen 3 und 4 | `test_us10_random_assignment_balances_odd_number` |
| AC-US10-03 | Aktive, inaktive und kursfremde Studierende | Zufallszuordnung im Zielkurs | Nur aktive Mitglieder des Zielkurses werden neu verteilt | `test_us10_random_assignment_ignores_inactive_and_other_courses` |
| AC-US10-04 | Weniger als zwei aktive Studierende | Zufallszuordnung angefordert | Fachlicher Fehler; Zuordnung unverändert | `test_us10_random_assignment_rejects_less_than_two_active` |
| AC-US10-04 | Studierender mit Team 1 | Ungültige Teamkennung zugewiesen | Fehler; Team 1 bleibt bestehen | `test_us10_manual_assignment_rejects_invalid_team_without_mutation` |

| AC-US10-05 | Gestartetes Spiel mit gespeichertem Kader und Team-Snapshots | Kurs-Teamzuordnung eines Spielers wird nachträglich geändert | Ursprüngliche Team-Snapshots und aktuelle Spielerwahl im Spiel bleiben unverändert | `test_us10_reassignment_does_not_change_running_game_team_snapshots` |

Alle sechs Methoden liegen in `test_us10_team_assignment.py` und nutzen eine temporäre SQLite-Datenbank. Die sechs Referenzen sind im Story-Mapping und in den maschinenlesbaren Kriterien hinterlegt.

## Manuelle UI-Abnahme

**PASS – vom Projektverantwortlichen am 29.10.2026 im Chat erteilt.** Eine eigene Browserprüfung durch den Assistenten fand nicht statt. Browser-Version, tatsächliche Auflösung und Zoomstufe sowie Einzelbeobachtungen/Screenshots wurden nicht übermittelt. Das vereinbarte **Referenzformat** ist 1920 × 1080 bei 100 % Zoom.

## Fachliche Grenzen und nächste Arbeit

- Nachträgliche Studierenden-Teamänderungen und die Unveränderlichkeit des begonnenen Spiels werden jetzt direkt geprüft. Weitergehende Interaktionen, etwa kombinierte Neuzuordnungen im fortgeschrittenen Spiel, sind nicht vollständig automatisiert.
- Eine ausgeglichene zufällige Verteilung ist getestet, nicht statistische Zufälligkeit; letztere ist kein eigenständiges Akzeptanzkriterium.
- Die sechs Szenarien sind Teilnachweise, keine vollständige fachliche Vollabnahme von US #10.
- Die zusätzlichen Kriterien-IDs wurden in Phase 2 spezifiziert und gemäß CI-Governance mit direkten Tests hinterlegt. Die eingefrorene Baseline bleibt unverändert.

Siehe auch `Syzeteo-Testabdeckung-Review-DE.md` und `Syzeteo-TDD-Kriterien-Governance-DE.md`.
