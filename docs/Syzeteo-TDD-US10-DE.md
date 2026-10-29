# Syzeteo – US #10: Teamzuordnung, Akzeptanznachweise

**Stand:** 29.10.2026 · **Status:** fünf direkte automatisierte Teilnachweise; UI-Freigabe PASS (vom Nutzer gemeldet).

## Fachliche Grundlage

Der Instructor kann Studierende manuell oder zufällig Team 1 beziehungsweise Team 2 zuordnen. Die Implementierung verwendet `storage.py::update_student` und `storage.py::randomize_teams`.

**Verbindliche maschinenlesbare Kriterien-ID:** `AC-US10-01` in `Syzeteo-Akzeptanzkriterien.json` (Status `legacy_provisional`). Die **S-US10-xx**-Kennungen unten bezeichnen konkrete Testszenarien und **sind keine zusätzlichen, bereits registrierten Akzeptanzkriterien**.

## Automatisierte Szenarien

| Szenario | Gegeben | Wenn | Dann | Direkter Test |
|---|---|---|---|---|
| S-US10-01 | Zwei Studierende ohne Team | Eine Person wird Team 2 zugeordnet | Nur diese Person hat Team 2 | `test_us10_manual_assignment_changes_only_selected_student` |
| S-US10-02 | Sieben aktive Studierende | Zufällige Zuordnung | Teamgrößen 3 und 4 | `test_us10_random_assignment_balances_odd_number` |
| S-US10-03 | Aktive, inaktive und kursfremde Studierende | Zufallszuordnung im Zielkurs | Nur aktive Mitglieder des Zielkurses werden neu verteilt | `test_us10_random_assignment_ignores_inactive_and_other_courses` |
| S-US10-04 | Weniger als zwei aktive Studierende | Zufallszuordnung angefordert | Fachlicher Fehler; Zuordnung unverändert | `test_us10_random_assignment_rejects_less_than_two_active` |
| S-US10-05 | Studierender mit Team 1 | Ungültige Teamkennung zugewiesen | Fehler; Team 1 bleibt bestehen | `test_us10_manual_assignment_rejects_invalid_team_without_mutation` |

Alle Methoden liegen in `test_us10_team_assignment.py` und nutzen eine temporäre SQLite-Datenbank. Die fünf Referenzen sind im Story-Mapping hinterlegt.

## Manuelle UI-Abnahme

**PASS – vom Projektverantwortlichen am 29.10.2026 im Chat erteilt.** Eine eigene Browserprüfung durch den Assistenten fand nicht statt. Browser-Version, tatsächliche Auflösung und Zoomstufe sowie Einzelbeobachtungen/Screenshots wurden nicht übermittelt. Das vereinbarte **Referenzformat** ist 1920 × 1080 bei 100 % Zoom.

## Fachliche Grenzen und nächste Arbeit

- Ein direkter Nachweis, dass nachträgliche Studierenden-Teamänderungen die gespeicherten Team-Snapshots **bereits gestarteter** Spiele nicht verändern, fehlt noch; hierfür ist ein gesonderter Randfalltest sinnvoll.
- Eine ausgeglichene zufällige Verteilung ist getestet, nicht statistische Zufälligkeit; letztere ist kein eigenständiges Akzeptanzkriterium.
- Die fünf Szenarien sind Teilnachweise, keine vollständige fachliche Vollabnahme von US #10.
- Weitere Kriterien-IDs werden erst in Phase 2 bewusst spezifiziert und gemäß CI-Governance mit Tests hinterlegt. Keine Baseline wird dadurch stillschweigend verändert.

Siehe auch `Syzeteo-Testabdeckung-Review-DE.md` und `Syzeteo-TDD-Kriterien-Governance-DE.md`.
