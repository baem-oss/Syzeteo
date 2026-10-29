# Syzeteo – Internationalisierungsspezifikation 1.1.1

Stand: 10.09.2026

## 1. Ziel

Syzeteo 1.1.1 behält Englisch und Deutsch als die beiden offiziellen UI-Sprachen bei und stärkt die Katalogarchitektur so, dass optionale lokale Präsentationsprofile installiert werden können, ohne Domänenlogik, Datenmodell oder Spielregeln zu verändern.

## 2. Offizielle Kataloge

```text
locales/
  en.json
  de.json
  README.md
```

- `en` ist Referenz- und Fallback-Sprache.
- `de` ist die deutsche Syzeteo-Oberfläche.
- Beide offiziellen Kataloge besitzen denselben Schlüsselbestand und kompatible Platzhalterverträge.

Der öffentliche Release enthält keine personalisierten Präsentationsprofile.

## 3. Optionale lokale Profile

Administratoren können einen vollständigen lokalen Katalog wie `de_custom.json` ergänzen. Ein solches Profil verändert ausschließlich Präsentationstexte. Interne Kartentypen, Statuscodes, Team-IDs, Wertungsregeln, Datenbankstrukturen und Question-Pool-Formate bleiben sprachneutral.

## 4. Locale-Auflösung

Locale-IDs mit einem explizit installierten Katalog werden vollständig erhalten. Ein installiertes `de_custom` wird daher als `de_custom` aufgelöst und nicht auf `de` verkürzt. Übliche regionale Angaben wie `de-DE` fallen weiterhin auf `de` zurück, sofern kein exakter Katalog vorhanden ist.

## 5. Persistenz

Jedes installierte Locale kann auf der Login-Seite gewählt und in den Instructor Settings als `ui_locale` gespeichert werden. Die Auswahl bleibt über Neustarts erhalten, solange der zugehörige Katalog installiert bleibt.

## 6. Sprachneutrale Grenzen

Eine Locale-Auswahl verändert nicht:

- SQLite-Schema oder Schemaversion;
- Datenbankdatei oder Datenpfad;
- interne Teamkennungen;
- Karten- oder Statuscodes;
- Spiel- und Wertungsregeln;
- Kurs-, Team-, Studierenden-, Runden-, Fragen- oder Antwortinhalte;
- das technische Question-Pool-JSON-Format `Syzeteo question pool`.

## 7. Rendering der Challenge Card

Die aufgedeckte Challenge Card bezieht sowohl Titel als auch Unterzeile aus dem aktiven Katalog. Harte UI-Literale sind auf diesem Renderingpfad unzulässig.

## 8. Abnahmetests

Die automatisierte Testsuite prüft, dass:

- `en` und `de` exakt denselben Schlüsselbestand besitzen;
- Platzhalter kompatibel sind;
- explizit installierte zusammengesetzte Locale-IDs erhalten bleiben;
- regionale Tags bei Bedarf weiterhin auf ihre Basissprache zurückfallen;
- optionale Profile Präsentationswerte überschreiben und als `ui_locale` persistent gespeichert werden können;
- die aufgedeckte Challenge Card Übersetzungsschlüssel statt harter englischer Literale verwendet.
