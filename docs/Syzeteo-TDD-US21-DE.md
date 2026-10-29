# Syzeteo – US #21: Akzeptanztests für das Fortsetzen laufender Spiele

Stand: 29.10.2026

## Fachliche Grundlage

US #21 verlangt, dass ein bereits laufendes Spiel später wieder geöffnet und am gespeicherten Zustand fortgesetzt werden kann. GR #11 untersagt die Fortsetzung abgebrochener Spiele. Die Testfälle verwenden eine isolierte temporäre SQLite-Datei und öffnen die Verbindung neu, um einen Prozess-/Sitzungswechsel auf Persistenzebene nachzubilden.

## Automatisierte Szenarien

| ID | Gegeben | Wenn | Dann | Test |
|---|---|---|---|---|
| AC-US21-01 | Ein laufendes Spiel ist gestartet | Die Datenbank wird geschlossen und erneut geöffnet | Das Spiel ist weiter als `running` auffindbar | `test_us21_running_game_can_be_found_after_restart` |
| AC-US21-02 | Ein laufendes Spiel hat Startspieler, Teams und neun Karten | Die Datenbankverbindung wird neu aufgebaut | Karten, Spielerbestand, aktueller Spieler, Modus und Spielstand sind unverändert | `test_us21_game_state_cards_and_roster_survive_restart` |
| AC-US21-03 | Ein Spiel wurde abgebrochen | Das System wird erneut gestartet | Das Spiel wird nicht als laufend angeboten | `test_us21_aborted_game_cannot_be_resumed_as_running` |

## Grenzen

Dies sind echte Assertions zum persistierten Spielzustand, aber noch kein automatisierter Streamlit-End-to-End-Test des Buttons „Spiel fortsetzen“. Der vorhandene UI-Pfad ist in `app.py` (Dashboard und Instructor Settings) implementiert und erfordert eine dokumentierte manuelle UI-Abnahme. Außerdem prüft AC-US21-02 bislang den unmittelbar nach Spielstart gespeicherten Zustand; eine zusätzliche Fortsetzung nach mehreren gewerteten Spielzügen bleibt ein sinnvoller nächster Test.

## Manuelle Abnahme

Referenzumgebung: 1920×1080 Pixel, Browser-Zoom 100 %.

1. Spiel starten, eine Fachfrage werten und den aktuellen Spielstand notieren.
2. Browser-Sitzung schließen, erneut anmelden und „Spiel fortsetzen“ öffnen.
3. Aktuelle Punkte, Karten, Start-/Folgespieler, Teamnamen und Team-Assist-Verbrauch vergleichen.
4. Spiel abbrechen und erneut anmelden; prüfen, dass dieses Spiel nicht fortgesetzt werden kann.

**Nachweisstatus:** Offen, bis Datum, Prüfer, Browser-Version und Ist-Ergebnis dokumentiert sind.
