# Syzeteo – US #21: Laufendes Spiel fortsetzen

**Stand:** 29.10.2026 · **Status:** vier direkte automatisierte Teilnachweise; UI-Freigabe PASS (vom Nutzer gemeldet).

## Fachliche Grundlage

Ein laufendes Spiel bleibt nach Unterbrechung verfügbar und wird am gespeicherten Zustand fortgesetzt. Abgebrochene Spiele dürfen nicht als laufende Spiele angeboten werden (GR #11). Die automatisierten Tests verwenden eine temporäre SQLite-Datenbank und öffnen die Verbindung erneut.

**Verbindliche maschinenlesbare Kriterien-ID:** `AC-US21-01` (Status `legacy_provisional`). Die folgenden **S-US21-xx** sind konkretisierte Testszenarien und **noch keine gesondert registrierten AC-IDs**.

## Automatisierte Szenarien

| Szenario | Gegeben | Wenn | Dann | Direkter Test |
|---|---|---|---|---|
| S-US21-01 | Laufendes Spiel | Datenbank neu geöffnet | Spiel weiter als `running` auffindbar | `test_us21_running_game_can_be_found_after_restart` |
| S-US21-02 | Startzustand mit Spieler, Teams und neun Karten | Verbindung neu geöffnet | Karten, Kader, aktuelle Spielerwahl und Spielstand unverändert | `test_us21_game_state_cards_and_roster_survive_restart` |
| S-US21-03 | Abgebrochenes Spiel | Verbindung neu geöffnet | Nicht mehr als laufend auswählbar | `test_us21_aborted_game_cannot_be_resumed_as_running` |
| S-US21-04 | Spiel mit gewerteter Fachfrage | Verbindung neu geöffnet; nächste Karte aufgedeckt | Punkte, Karten, Spielerwahl und Zug bleiben erhalten; nächste Karte ist bedienbar | `test_us21_scored_turn_can_continue_after_restart` |

Alle vier Methoden liegen in `test_us21_resume.py` und sind im Story-Mapping referenziert.

## UI-Abnahme und Prüfanleitung

**PASS – vom Projektverantwortlichen am 29.10.2026 gemeldet.** Dies ist keine vom Assistenten durchgeführte Browser-E2E-Prüfung. Einzelbeobachtungen, Browserversion und tatsächliche Auflösung/Zoomstufe sind nicht übermittelt.

Referenz für eine künftig einzeln dokumentierte Wiederholungsprüfung: 1920×1080, Browser-Zoom 100 %. Spiel starten und eine Fachfrage werten; Sitzung beenden, erneut anmelden und „Spiel fortsetzen“ wählen; Punkte, Karten, Spieler/Teams und Team-Assist-Zustand vergleichen; nach Abbruch prüfen, dass keine Fortsetzung mehr angeboten wird.

## Grenzen

- Die automatisierten Tests beweisen persistierten Zustand und weitere Bedienbarkeit **auf Anwendungsebene**; sie ersetzen keinen automatisierten Streamlit-Browsertest.
- Der testweise Neustart ist ein erneutes Öffnen der Datenbankverbindung, kein vollständig automatisierter Browser-Login oder Prozessneustart.
- Mehrere hintereinander gewertete Züge und weitere UI-Randfälle sind nicht als vollständig abgedeckt ausgewiesen.
- Für eine revisionsfähige manuelle Einzelabnahme fehlen Browser-/Umgebungsdetails und ggf. Screenshots.

Siehe `Syzeteo-Testabdeckung-Review-DE.md` und `Syzeteo-TDD-Kriterien-Governance-DE.md`.
