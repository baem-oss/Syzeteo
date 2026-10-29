# Syzeteo – Testabdeckung und TDD-Status (konsolidiert)

**Stand:** 29.10.2026 · **Bezug:** GitHub `main` nach PR #9 · **Geltung:** Dokumentations- und Traceability-Status, **keine fachliche Vollabnahme**.

## Verbindliche Quellen

- `docs/Syzeteo-L-US-DE.md`: 29 fachliche User Stories.
- `docs/Syzeteo-Akzeptanztests-Mapping.json`: aktuelle Story-zu-Test-Zuordnung; maßgeblich für die Zahlen dieses Berichts.
- `docs/Syzeteo-Akzeptanzkriterien.json`: Kriterien mit stabilen IDs, Wortlaut, Status und Testreferenzen.
- `docs/Syzeteo-TDD-Baseline.json` und `docs/Syzeteo-Akzeptanzkriterien-Baseline.json`: eingefrorene Vergleichsstände, **nicht** Abnahmenachweise.
- `docs/Syzeteo-Akzeptanztests-TDD-DE.md`: lesbarer Akzeptanztestkatalog und manuelle Freigaben.
- `docs/Syzeteo-TDD-Kriterien-Governance-DE.md`: Regeln für Änderungen und CI-Schutz.
- `docs/Syzeteo-TDD-US10-DE.md`, `docs/Syzeteo-TDD-US21-DE.md`, `docs/Syzeteo-TDD-Phase2-US24-DE.md`: vertiefte Tests und offene Restpunkte.

## Aktueller Nachweisstand

| Kennzahl | Stand |
|---|---:|
| User Stories | 29 |
| Stories mit mindestens einer automatisierten Referenz | 29 |
| Story-Test-Zuordnungen (Mehrfachnennungen eingeschlossen) | 77 |
| Verschiedene referenzierte Testmethoden | 71 |
| Story-Mappings mit Status `verified_partial` | 29 |
| Maschinenlesbare Kriterien mit Status `legacy_provisional` | 29 |
| Story-Mappings mit `manual_review: true` (Bedarfsmarker, **kein** Abnahmestatus) | 9 |

**Einordnung:** `verified_partial` bezeichnet dokumentierte fachliche **Teilnachweise** und keine vollständige Abnahme der Story. `legacy_provisional` kennzeichnet generische, noch fachlich zu präzisierende Kriterien. Die Zahl der Testreferenzen ist keine Testabdeckungsquote. Die CI prüft die Existenz referenzierter Methoden und führt Regressionstests aus; die semantische Aussagekraft der Assertions muss im Review bestätigt werden.

### Referenzübersicht je Story

| Story | Automatische Testreferenzen | Nachweisstatus |
|---|---:|---|
| US #01 | 3 | Teilnachweis |
| US #02 | 3 | Teilnachweis |
| US #03 | 2 | Teilnachweis |
| US #04 | 2 | Teilnachweis |
| US #05 | 1 | Teilnachweis |
| US #06 | 1 | Teilnachweis |
| US #07 | 2 | Teilnachweis |
| US #08 | 4 | Teilnachweis |
| US #09 | 1 | Teilnachweis |
| US #10 | 5 | Teilnachweis |
| US #11 | 1 | Teilnachweis |
| US #12 | 1 | Teilnachweis |
| US #13 | 1 | Teilnachweis |
| US #14 | 2 | Teilnachweis |
| US #15 | 2 | Teilnachweis |
| US #16 | 2 | Teilnachweis |
| US #17 | 3 | Teilnachweis |
| US #18 | 1 | Teilnachweis |
| US #19 | 1 | Teilnachweis |
| US #20 | 3 | Teilnachweis |
| US #21 | 4 | Teilnachweis |
| US #22 | 2 | Teilnachweis |
| US #23 | 1 | Teilnachweis |
| US #24 | 9 | Teilnachweis |
| US #25 | 1 | Teilnachweis |
| US #26 | 4 | Teilnachweis |
| US #27 | 4 | Teilnachweis |
| US #28 | 6 | Teilnachweis |
| US #29 | 5 | Teilnachweis |

## Fachliche Fortschritte seit dem ursprünglichen Review

- **US #10 – Studierende Teams zuordnen:** fünf direkte Akzeptanztests zu manueller und zufälliger Verteilung, Kursisolation und ungültigen Eingaben.
- **US #21 – Laufendes Spiel fortsetzen:** vier direkte Tests, einschließlich persistiertem Zustand nach gewertetem Spielzug und erneuter Datenbankverbindung.
- **US #24 – Gespielte Fragen protokollieren:** neun direkte Tests zu abgehandelten Fragen, Historie, Abbruch/Löschung, Kurs-/Rundenfilter, CSV und letzter Instructor-Karte.
- **US #22 – Beamer-Modus:** zwei zugeordnete Rendering-Tests; diese ersetzen keine echte Browserprüfung.

Die vormals als testlos aufgeführten US #10, #21 und #24 besitzen inzwischen automatisierte Nachweise. Der frühere Stand von 59 Verknüpfungen/26 Stories ist **historisch und nicht mehr aktuell**.

## Manuelle UI-Freigaben

Am **29.10.2026** hat der Projektverantwortliche die UI-Abnahme im Chat als **PASS** erklärt. Für **US #10, #21, #22 und #24** ist diese gemeldete Freigabe dokumentiert (US #22 in der manuellen Prüftabelle, die anderen in den jeweiligen Detaildokumenten).

**Evidenzgrenze:** Es fand keine eigene Browserprüfung durch den Assistenten statt; Browser-Version, tatsächlich verwendete Auflösung und Zoomstufe sowie Screenshots wurden nicht übermittelt. Die definierte **Referenzumgebung** beträgt 1920 × 1080 Pixel bei 100 % Zoom, ist jedoch nicht als tatsächlich geprüft belegt. Eine pauschale UI-Vollabnahme sämtlicher 29 Stories folgt aus der Freigabe nicht.

## CI und Änderungs-Governance

`.github/workflows/tests.yml` startet bei Push und Pull Request:

1. `traceability_check.py`: neue oder geänderte User Stories müssen mit zusätzlicher Testreferenz hinterlegt sein.
2. `acceptance_criteria_check.py`: neue oder geänderte Akzeptanzkriterien erfordern zusätzliche Testreferenzen; entfernte/doppelte/fehlerhaft zugeordnete Kriterien werden abgewiesen.
3. PR-Schutz für die eingefrorene Kriterien-Baseline.
4. `regression_pipeline.py --native --release`: kanonische Regression inklusive Release-Prüfungen.

Die Ausgangsfassung der Baseline bleibt unangetastet. **Grenzen:** Das Gate beweist weder, dass Tests fachlich ausreichende Assertions enthalten, noch schützt es vor direkten Pushes auf `main`; hierfür sollte Branch Protection eingerichtet und überprüft werden.

## Offene Arbeiten nach dieser Dokumentationsphase

1. **Phase 2:** Vorläufige generische Kriterien nach und nach in konkrete Given-When-Then-Szenarien überführen; fachliche Randfälle und ggf. ergänzende Tests prüfen. Insbesondere die Unveränderlichkeit von Team-Snapshots bei nachträglicher Änderung der Teamzuordnung bleibt bei US #10 ein zusätzlicher Testkandidat.
2. **Phase 3:** Durchsetzung und Qualität des Traceability-Gates weiter verbessern; Branch Protection/Required Checks verifizieren; gegebenenfalls automatisierte Browser-E2E-Tests ergänzen.
3. Falls ein revisionsfähiger Einzelprüfnachweis benötigt wird: manuelle UI-Freigaben um tatsächlich beobachtete Browser-Version, Auflösung, Schritte und Belege erweitern.

**Phase-1-Abschlusskriterium:** Alle vorgenannten Angaben beruhen auf den aktuellen JSON-Mappings und den dokumentierten Freigaben; die Dokumentationsbereinigung ändert keine fachliche Anforderung, kein Testmapping, keinen Produktivcode und keine Baseline.
