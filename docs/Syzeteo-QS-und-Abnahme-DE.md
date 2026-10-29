# Syzeteo – Akzeptanzkriterien, Tests und Qualitätssicherung

**Referenzstand: 29.10.2026 · Zweck:** Prüfbarkeit der Anforderungen nachvollziehen. Dies ist **keine Erklärung einer vollständigen fachlichen Abnahme**.

[Zur Dokumentationsübersicht](README.md) · [RE-Methodenbeispiel](RE-Methodenbeispiel-DE.md)

## 1. Welche Dokumente sind der Nachweis?

| Frage | Verbindliche Quelle |
|---|---|
| Was soll das System können? | [29 User Stories](Syzeteo-L-US-DE.md), [Regeln und Randbedingungen](Syzeteo-RANF-etc-DE.md) |
| Was ist konkret überprüfbar? | [46 maschinenlesbare Akzeptanzkriterien](Syzeteo-Akzeptanzkriterien.json) |
| Welcher Test ist welcher Story zugeordnet? | [Story-Test-Mapping](Syzeteo-Akzeptanztests-Mapping.json) |
| Welche fachlichen Zusammenhänge bestehen? | [Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md) |
| Was wird tatsächlich automatisiert ausgeführt? | `test_*.py`, `regression_pipeline.py` und [GitHub-Actions-Workflow](../.github/workflows/tests.yml) |

**Maßgeblich für den aktuellen Kriterienstand ist die JSON-Datei**, nicht ein historischer Markdown-Zwischenbericht. Die formalen Baselines dienen zum Erkennen von Änderungen und sind keine Abnahmezeugnisse.

## 2. Dokumentierter Nachweisstand

| Kennzahl | Stand |
|---|---:|
| Fachliche User Stories | **29** |
| In JSON konkretisierte Kriterien | **46** |
| Davon `specified_partial` | 46 |
| Aktive `legacy_provisional`-Kriterien | 0 |
| Story-Test-Zuordnungen (Mehrfachnennungen zählen) | **109** |
| Unterschiedliche referenzierte Testmethoden | **103** |
| Automatisch gegen Browser geprüfte End-to-End-Abläufe | **Keine eigene Browser-E2E-Suite** |

**Vorsicht beim Interpretieren:** 46 spezifizierte Kriterien sind nicht gleichbedeutend mit „46 vollständig abgenommenen Anforderungen“. Ein Kriterium `specified_partial` besitzt einen konkreten Prüfzweck und mindestens einen automatisierten Teilnachweis. Weitere fachliche Randfälle können fehlen. Die Zahl der Testmethoden ist **keine** prozentuale Anforderungsabdeckung.

## 3. Drei anschauliche Testbeispiele

| RE-Frage | Kriterium | Was prüft der Test tatsächlich? |
|---|---|---|
| Bleibt eine gestartete Runde historisch unverändert? | **AC-US10-05** | Nachträgliche Teamänderung im Kurs darf Team-Snapshots und aktuelle Spielerwahl im laufenden Spiel nicht überschreiben. Nachweis: `test_us10_team_assignment.py::test_us10_reassignment_does_not_change_running_game_team_snapshots`. |
| Kann ein Spiel nach Unterbrechung weitergehen? | **AC-US21-01** | Nach zwei gewerteten Zügen bleiben Kader, Punkte und Karten nach erneutem Datenbankzugriff erhalten; ein dritter Zug ist möglich. Nachweis: `test_us21_resume.py::test_us21_two_scored_turns_survive_restart_and_allow_third_score`. |
| Welche Fragen kommen in das Protokoll? | **AC-US24-01 / -06** | Abschließend behandelte Fachfragen erscheinen unabhängig von richtig/falsch. Eine letzte Instructor-Fachfrage erscheint im Protokoll, aber nicht als studentischer Versuch in der Statistik. Nachweise in `test_us24_question_protocol.py`. |

Weitere Beispiele: **US #07** – vollständige Kurslöschung ohne Löschung des globalen Fragenpools; **US #26** – Abbruch, Löschung und erneutes Starten der Runde. Die eigentlichen Assertions stehen im Quellcode; in diesem Dokument werden sie nur erklärt.

## 4. Automatische Qualitätsprüfung in GitHub

Der Workflow `tests` mit dem Job **`regression-and-traceability`** prüft:

1. **User-Story-Traceability:** `traceability_check.py` verifiziert existierende Story-Test-Verweise und vergleicht Änderungen mit der eingefrorenen Story-Baseline.
2. **Kriterien-Integrität:** `acceptance_criteria_check.py` verifiziert eindeutige IDs, gültige Zuordnung zu Storys, **beidseitig stimmige** Kriterien-/Story-Test-Verweise und zumindest direkte Assertions in referenzierten Testmethoden.
3. **PR-spezifischen Evidenznachweis:** `tdd_pr_evidence_check.py` verlangt bei neuen oder geänderten Kriterien gegenüber dem Zielbranch eine **neu hinzugefügte oder geänderte Assertion** im betreffenden PR. Eine bloß neu eingetragene, unveränderte Testreferenz reicht nicht.
4. **Baselines:** Gewöhnliche PRs dürfen weder die Story-Baseline noch die Kriterien-Baseline ändern. Beide Dateien dienen als historische Vergleichsstände.
5. **Regression:** `regression_pipeline.py --native --release` führt die automatisierten Tests und Release-Prüfungen aus.

Das Gate kann nur die **technische Form** einer Assertion beurteilen, nicht ihre inhaltliche Angemessenheit. Ein syntaktisch neuer Test kann immer noch fachlich falsch sein. Diese Beurteilung ist eine Review-Aufgabe.

## 5. Manuelle UI-Abnahmen – dokumentierter Umfang

Die folgenden PASS-Meldungen wurden am **29.10.2026** vom Projektverantwortlichen als manuelle UI-Freigabe mitgeteilt. Der Assistent hat **keine eigene Browserprüfung** ausgeführt; es liegen keine einzeln dokumentierten Bildschirmbeobachtungen vor.

| US / AC | Prüfgegenstand | Gemeldeter Status | Evidenzgrenze |
|---|---|---|---|
| US #10 / AC-US10-01 | Teamzuordnung | **PASS (Nutzerfreigabe)** | Browser-/Einzelprüfprotokoll nicht übermittelt |
| US #21 / AC-US21-01 | Laufendes Spiel fortsetzen | **PASS (Nutzerfreigabe)** | Browser-/Einzelprüfprotokoll nicht übermittelt |
| US #22 / AC-US22-01 | Normal- und Beameransicht | **PASS (Nutzerfreigabe)** | Scrollfreiheit und tatsächliche Testumgebung nicht einzeln belegt |
| US #24 / AC-US24-01 | Fragenprotokoll und CSV | **PASS (Nutzerfreigabe)** | Browser-/Einzelprüfprotokoll nicht übermittelt |

**Referenz für reproduzierbare Sichtprüfungen:** **1920 × 1080 Pixel**, **100 % Browser-Zoom**, normale Spielansicht und Beameransicht. Dieser Referenzwert dokumentiert **nicht**, dass die bereits gemeldeten Abnahmen nachweislich unter diesen Bedingungen stattgefunden haben. Screenshot-/Ticket-Links sind nicht übermittelt.

### Vorlage für eine künftige manuelle Abnahme

| Datum | US / AC | Browser / Version | Auflösung / Zoom | Prüfschritte | Soll | Ist | PASS/FAIL | Prüfer | Beleg |
|---|---|---|---|---|---|---|---|---|---|
| *ausfüllen* | *ID* | *konkret* | *tatsächlich* | *reproduzierbar* | *prüfbar* | *beobachtet* | *Ergebnis* | *Name/Rolle* | *URL* |

**Methodischer Unterschied:** Eine gemeldete Freigabe und ein reproduzierbarer Einzelprüfnachweis sind nicht dieselbe Evidenzstufe. Beide dürfen dokumentiert werden, müssen aber klar unterschieden bleiben.

## 6. GitHub-Branchschutz – noch eine administrative Aufgabe

Am 29.10.2026 wurde das Ruleset [„Ruleset Syzeteo“ (ID 22184406)](https://github.com/baem-oss/Syzeteo/rules/22184406) über die GitHub-API geprüft:

- `enforcement: disabled` und keine Zielbranch-Auswahl; daraus folgt **kein wirksamer Schutz von `main`**.
- Der angeschlossene GitHub-Zugang besitzt keine Rechte zur Änderung der Branchschutz-Konfiguration (Branch-Protection-API: HTTP 403).
- Der CI-Workflow kann deshalb getestet werden, **ohne** dass er bereits bei jedem Merge technisch erzwungen ist.

**Vom Repository-Administrator zu erledigen:** Unter [Settings → Rules → Rulesets](https://github.com/baem-oss/Syzeteo/settings/rules) ein auf `main` gerichtetes, aktives Ruleset konfigurieren: verpflichtender Pull Request, erforderlicher Statuscheck `regression-and-traceability`, keine unkontrollierten Bypasses, keine Löschung/Force-Push. Vor Aktivierung des vorhandenen Rulesets die dort zusätzlich eingestellten CodeQL-/Code-Quality-Regeln auf tatsächliche Verfügbarkeit prüfen. Anschließend den Schutz mit einem fehlschlagenden Test-PR und einem unzulässigen Direkt-Push **nachweislich** verifizieren.

**Bis dahin:** Branch Protection ist eine **offene administrative Aufgabe**, nicht „erledigt“.

## 7. Weitere Grenzen und gepflegter Änderungsprozess

- **Nicht implementiert:** Eine vollständige automatisierte Browser-E2E-Suite für Streamlit; bei UI-Fragen sind manuelle Prüfungen weiterhin wichtig.
- **Nicht behauptet:** Vollständige semantische Abdeckung aller fachlichen und nichtfunktionalen Randfälle.
- **Nicht erlaubt:** Nachträgliche Änderungen an historischen Spiel- und Fragen-Snapshots ohne fachliche Grundlage.
- **Bei neuen Anforderungen:** US/Regel fachlich klären → UC/BPMN prüfen → AC konkret formulieren → direkte Test-Assertions ergänzen → JSON-Mappings aktualisieren → Pipeline/Review → ggf. UI-Abnahme.
- **Baseline-Migration:** Nur als separater fachlich geprüfter Vorgang, nicht durch stillschweigendes Überschreiben historischer Dateien.

**Für Studierende:** Der Kern der Qualitätssicherung liegt darin, aus einer ungenauen Zielaussage **beobachtbare Nachbedingungen** zu gewinnen und ihre Erfüllung prüfbar zu machen. Ein grüner CI-Lauf unterstützt diese Prüfung; er ersetzt keine fachliche Modellkritik.

[Zurück zum Leseweg](README.md) · [Zum Methodenbeispiel](RE-Methodenbeispiel-DE.md)
