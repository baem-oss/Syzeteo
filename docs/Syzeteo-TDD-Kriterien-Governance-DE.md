# Syzeteo – Verbindliche TDD-Akzeptanzkriterien und CI-Regeln

Stand: 29.10.2026

## Datenmodell

- `Syzeteo-Akzeptanzkriterien.json`: maschinenlesbare, versionierte Kriterien mit stabilen IDs (`AC-USnn-mm`), fachlichem Wortlaut, Story-ID, Testreferenzen und Hinweis auf manuelle Abnahme.
- `Syzeteo-Akzeptanzkriterien-Baseline.json`: unveränderter eingefrorener Bestand vom 29.10.2026. Er ist **keine fachliche Freigabe**; bestehende generische Formulierungen tragen `legacy_provisional`.
- `Syzeteo-Akzeptanztests-Mapping.json`: bisherige Story-zu-Test-Traceability und fachlich überprüfte Teilnachweise; weiterhin zu pflegen.

## Konsolidierter Nachweisstand und Nummerierung

Der aktuelle Story-Test-Status und die verbleibenden fachlichen Lücken stehen in `Syzeteo-Testabdeckung-Review-DE.md`. Der lesbare Akzeptanztestkatalog ist `Syzeteo-Akzeptanztests-TDD-DE.md`. In Phase 2 wurden **alle ursprünglich 29 generischen Kriterien** zu konkreten, automatisiert referenzierten Prüfzwecken formuliert. Zusammen mit 17 ergänzenden Kriterien stehen nun **46 Kriterien** auf `specified_partial`; kein aktives Kriterium bleibt auf `legacy_provisional`. Dies ist ein Abschluss der initialen Kriterienkonkretisierung, keine Bestätigung vollständiger Story-Abdeckung. Maßgeblich registriert sind ausschließlich die IDs in `Syzeteo-Akzeptanzkriterien.json`; weitere Aufspaltungen müssen das CI-Gate durchlaufen.

Die manuelle UI-Freigabe PASS für US #10, #21, #22 und #24 wurde vom Projektverantwortlichen gemeldet. Sie darf nicht als vom CI bestätigter Browser-E2E-Test oder als vollständige Freigabe aller Kriterien ausgegeben werden.

## Durchsetzung

Der Prüfer `acceptance_criteria_check.py` vergleicht jede aktive Kriterien-ID mit ihrer eingefrorenen Fassung.

| Änderung | Pipeline |
|---|---|
| Altes Kriterium unverändert | Bestehende Lücken melden, nicht blockieren |
| Neues Kriterium | Mindestens eine referenzierte, vorhandene Testmethode verpflichtend |
| Wortlaut, Story-Zuordnung, Status oder manuelle Abnahme geändert | Mindestens eine **zusätzliche** Testreferenz gegenüber der Baseline verpflichtend |
| Kriterium gelöscht, ID doppelt oder falsch zugeordnet | Blockieren |
| Ungültige Testreferenz | Blockieren |
| Baseline im regulären PR geändert | Blockieren; gesonderte kontrollierte Migration erforderlich |

**Grenze der Automatisierung:** Der Gate kann nachweisen, dass eine Testmethode existiert und neu referenziert wird. Er kann **nicht** semantisch beweisen, dass sie das Kriterium tatsächlich testet oder dass ein neuer Testcode geschrieben wurde. Das muss der Reviewer anhand der Assertions bestätigen. Gerade bei UI-Anforderungen bleibt die manuelle Abnahme zusätzlich verbindlich.

## Ablauf bei neuen / geänderten Akzeptanzkriterien

1. Präzise Given-When-Then-Anforderung mit eindeutiger ID in `Syzeteo-Akzeptanzkriterien.json` anlegen oder ändern.
2. Automatisierten Akzeptanztest mit fachlicher Assertion hinzufügen; neue Testreferenz eintragen.
3. Bei UI-Anforderungen das manuelle Abnahmeprotokoll (Full HD 1920 × 1080, 100 % Zoom) ergänzen.
4. Traceability-Mapping und lesbare Story-Spezifikation synchronisieren.
5. Lokal `python acceptance_criteria_check.py` und `python regression_pipeline.py --native --release` ausführen.
6. PR erst nach grüner CI und fachlicher Prüfung der Assertions mergen.

**Baseline-Regel:** Eine Änderung der eingefrorenen Baseline ist nicht Teil normaler Feature-PRs. Sollte eine neue Baseline nötig werden, benötigt dies einen gesonderten, dokumentierten Review und eine explizite Anpassung der Sperrregel.

## Noch offene methodische Punkte

- Es gibt keine aktiven generischen `legacy_provisional`-Kriterien mehr. Die 46 `specified_partial`-Kriterien beschreiben jeweils einen überprüfbaren Teilaspekt, **keine** garantierte vollständige Abnahme aller Story-Randfälle.
- Die neuen Kriterien werden noch nicht automatisch aus dem Markdown-Katalog gespiegelt. Die JSON-Datei ist die verbindliche technische Referenz; menschliche Dokumentation muss im Review abgeglichen werden.
- Der CI-Schutz der Baseline ist für Pull Requests implementiert. Direkte Pushes nach `main` sollten zusätzlich über GitHub Branch Protection unterbunden werden.
