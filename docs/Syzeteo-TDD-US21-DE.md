# Syzeteo – US #21: Laufendes Spiel fortsetzen

**Stand:** 29.10.2026 · **Status:** fünf direkte automatisierte Teilnachweise, drei konkretisierte Kriterien; UI-Freigabe PASS (vom Nutzer gemeldet).

## Fachliche Grundlage

Ein laufendes Spiel bleibt nach Unterbrechung verfügbar und wird am gespeicherten Zustand fortgesetzt. Abgebrochene Spiele dürfen nicht als laufende Spiele angeboten werden (GR #11). Die automatisierten Tests verwenden eine temporäre SQLite-Datenbank und öffnen die Verbindung erneut.

**Verbindliche maschinenlesbare Kriterien:** `AC-US21-01` bis `AC-US21-03` (Status `specified_partial`). Die folgenden Szenarien sind konkreten Kriterien zugeordnet; pro Kriterium sind direkte Testmethoden hinterlegt.

## Automatisierte Szenarien

| Szenario | Gegeben | Wenn | Dann | Direkter Test |
|---|---|---|---|---|
| AC-US21-02 | Laufendes Spiel | Datenbank neu geöffnet | Spiel weiter als `running` auffindbar | `test_us21_running_game_can_be_found_after_restart` |
| AC-US21-02 | Startzustand mit Spieler, Teams und neun Karten | Verbindung neu geöffnet | Karten, Kader, aktuelle Spielerwahl und Spielstand unverändert | `test_us21_game_state_cards_and_roster_survive_restart` |
| AC-US21-03 | Abgebrochenes Spiel | Verbindung neu geöffnet | Nicht mehr als laufend auswählbar | `test_us21_aborted_game_cannot_be_resumed_as_running` |
| AC-US21-01 | Spiel mit gewerteter Fachfrage | Verbindung neu geöffnet; nächste Karte aufgedeckt | Punkte, Karten, Spielerwahl und Zug bleiben erhalten; nächste Karte ist bedienbar | `test_us21_scored_turn_can_continue_after_restart` |

| AC-US21-01 | Zwei regulär gewertete Spielzüge sind abgeschlossen | Datenbankverbindung erneut geöffnet und ein weiterer Zug gewertet | Zwei abgeschlossene Züge bleiben unverändert; der dritte lässt sich korrekt werten | `test_us21_two_scored_turns_survive_restart_and_allow_third_score` |

Alle fünf Methoden liegen in `test_us21_resume.py` und sind im Story-Mapping referenziert.

## UI-Abnahme und Prüfanleitung

**PASS – vom Projektverantwortlichen am 29.10.2026 gemeldet.** Dies ist keine vom Assistenten durchgeführte Browser-E2E-Prüfung. Einzelbeobachtungen, Browserversion und tatsächliche Auflösung/Zoomstufe sind nicht übermittelt.

Referenz für eine künftig einzeln dokumentierte Wiederholungsprüfung: 1920×1080, Browser-Zoom 100 %. Spiel starten und eine Fachfrage werten; Sitzung beenden, erneut anmelden und „Spiel fortsetzen“ wählen; Punkte, Karten, Spieler/Teams und Team-Assist-Zustand vergleichen; nach Abbruch prüfen, dass keine Fortsetzung mehr angeboten wird.

## Grenzen

- Die automatisierten Tests beweisen persistierten Zustand und weitere Bedienbarkeit **auf Anwendungsebene**; sie ersetzen keinen automatisierten Streamlit-Browsertest.
- Der testweise Neustart ist ein erneutes Öffnen der Datenbankverbindung, kein vollständig automatisierter Browser-Login oder Prozessneustart.
- Zwei hintereinander gewertete Züge und ein weiterer Zug nach Verbindungswechsel sind jetzt geprüft; eine vollständige Browser-E2E-Suite und darüber hinausgehende Randfälle bleiben offen.
- Für eine revisionsfähige manuelle Einzelabnahme fehlen Browser-/Umgebungsdetails und ggf. Screenshots.

Siehe `Syzeteo-Testabdeckung-Review-DE.md` und `Syzeteo-TDD-Kriterien-Governance-DE.md`.
