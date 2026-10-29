# Syzeteo – TDD-Testabdeckung und Phase-2-Abschlussstand

**Stand:** 29.10.2026 · **Bezugsstand:** Branch `feature/tdd-phase2-completion-remaining21` · **Art:** nachvollziehbare Teilnachweise, **keine fachliche Vollabnahme sämtlicher 29 Stories**.

## Überblick

| Kennzahl | Wert |
|---|---:|
| User Stories | 29 |
| Stories mit Testreferenzen | 29 |
| Registrierte Kriterien (gesamt) | 46 |
| Status `specified_partial` | 46 |
| Status `legacy_provisional` | 0 |
| Story-Test-Zuordnungen | 109 |
| Unterschiedliche referenzierte Testmethoden | 103 |
| Story-Mappings mit `verified_partial` | 29 |

**Definition:** Ein Kriterium `specified_partial` nennt eine konkrete fachliche, mit Assertions referenzierte Nachbedingung. Die zusätzliche Abdeckung aller denkbaren Randfälle, Sicherheits-/Datenschutzanforderungen und Browserverläufe ist **nicht** dadurch bewiesen. Die ursprünglichen 29 generischen Kriterien wurden konkretisiert; zusätzlich sind 17 weitere Kriterien registriert. Der eingefrorene Vergleichsbestand ist unverändert.

## Story-zu-Test-Übersicht

| User Story | Kriterien | Story-Test-Zuordnungen | Einordnung |
|---|---:|---:|---|
| US #01 | 1 | 4 | Teilnachweis |
| US #02 | 1 | 4 | Teilnachweis |
| US #03 | 1 | 3 | Teilnachweis |
| US #04 | 1 | 3 | Teilnachweis |
| US #05 | 2 | 2 | Teilnachweis |
| US #06 | 2 | 3 | Teilnachweis |
| US #07 | 3 | 4 | Teilnachweis |
| US #08 | 2 | 5 | Teilnachweis |
| US #09 | 2 | 3 | Teilnachweis |
| US #10 | 5 | 6 | Teilnachweis |
| US #11 | 1 | 2 | Teilnachweis |
| US #12 | 1 | 2 | Teilnachweis |
| US #13 | 1 | 2 | Teilnachweis |
| US #14 | 1 | 3 | Teilnachweis |
| US #15 | 1 | 3 | Teilnachweis |
| US #16 | 1 | 3 | Teilnachweis |
| US #17 | 1 | 4 | Teilnachweis |
| US #18 | 1 | 2 | Teilnachweis |
| US #19 | 1 | 2 | Teilnachweis |
| US #20 | 1 | 4 | Teilnachweis |
| US #21 | 3 | 5 | Teilnachweis |
| US #22 | 1 | 3 | Teilnachweis |
| US #23 | 1 | 2 | Teilnachweis |
| US #24 | 6 | 10 | Teilnachweis |
| US #25 | 1 | 2 | Teilnachweis |
| US #26 | 1 | 5 | Teilnachweis |
| US #27 | 1 | 5 | Teilnachweis |
| US #28 | 1 | 7 | Teilnachweis |
| US #29 | 1 | 6 | Teilnachweis |

## Phase-2-Arbeitspakete

- **PR #11:** US #10, #21, #24 – Integrität der Team-Snapshots, Fortsetzung nach Spielzügen, Fragenprotokoll einschließlich CSV und Instructor-Karte; 14 Kriterien.
- **PR #12:** US #05–#09 – Anmeldung, Accountverwaltung, Kurslöschung, Studierendenverwaltung und CSV-Import; weitere elf konkretisierte Kriterien.
- **Aktuelles Paket:** US #01–#04 sowie #11–#20, #22–#23, #25–#29 – alle verbliebenen 21 vorläufigen Kriterien fachlich formuliert und mit 21 neuen konkreten Domain-Assertions verknüpft.

Die fachlichen User Stories, der Produktivcode, die Business Rules und die eingefrorenen `Syzeteo-TDD-Baseline.json` / `Syzeteo-Akzeptanzkriterien-Baseline.json` sind unverändert.

## UI-Abnahme und Grenzen

Die **vom Projektverantwortlichen gemeldete** manuelle UI-Freigabe vom 29.10.2026 zu US #10, #21, #22 und #24 ist in `Syzeteo-Akzeptanztests-TDD-DE.md` dokumentiert. Sie ist keine unabhängige Browser-E2E-Prüfung. Browser-/Zoom-/Auflösungsdaten und Einzelbelege fehlen. Weitere Stories sind damit nicht pauschal freigegeben.

Die CI prüft Testreferenzen sowie die Python-Regression. Die semantische Angemessenheit jeder Assertion, das Verhalten realer Browser und die vollständige Berücksichtigung aller fachlichen Neben- und Fehlerszenarien bleiben Gegenstand von Review/ggf. Phase 3.

## Nächste Stufe (Phase 3)

1. Branch Protection / verbindliche Checks für `main` verifizieren und aktivieren.
2. Test-Gate gegen nur umbenannte oder thematisch unpassende Testreferenzen härten; kontrolliertes Kriterien-Rebaselining definieren.
3. Optional Browser-E2E-Automation und revisionsfähige manuelle Prüfnachweise ergänzen.
4. Zusätzliche fachliche Kriterien gezielt dort anlegen, wo während der weitergehenden Review noch ungetestete Randfälle identifiziert werden.

**Phase-2-Abschlusskriterium:** Alle ursprünglich als `legacy_provisional` markierten Kriterien besitzen einen konkret benannten fachlichen Prüfzweck und mindestens eine neu zugeordnete direkte Testmethode; fachliche Vollabdeckung der Stories wird nicht behauptet.
