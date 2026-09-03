# Syzeteo – Technische Baseline 1.0.0

Datum: 2026-08-27

## 1. Zweck

Dieses Dokument definiert die technische Baseline für Syzeteo 1.0.0. Das erste öffentliche Syzeteo-Release verwendet ein natives Syzeteo-Datenmodell und sprachneutrale persistierte Domänenkennungen.

## 2. Laufzeit und Deployment

- Anwendungsframework: Streamlit
- Implementierungssprache: Python
- Persistenz: SQLite
- vorgesehener Deployment-Weg: Docker / Docker Compose
- Standard-Host-Port: `8502`
- Anwendungsversion: `1.0.0`

## 3. Persistenz

- Datenbankdatei: `syzeteo.sqlite3`
- Standard-Datenverzeichnis: `./persistent`
- optionale Environment-Variable: `SYZETEO_DATA_DIR`
- SQLite-Schemaversion: `PRAGMA user_version = 2`

Anwendungs- und SQLite-Schemaversion sind voneinander unabhängig. Schemaversion 2 ist die erste veröffentlichte Syzeteo-Schemabasis und enthält die Tabelle `app_settings` für persistente Anwendungseinstellungen.

Syzeteo 1.0.0 verwendet zur Laufzeit keine alten Vorab-Datenbanknamen bzw. Environment-Variablen.

## 4. Persistierte Domänenterminologie

| Domänenbegriff | Persistierter Bezeichner |
|---|---|
| Question Card | `card_type = 'question'` |
| Challenge Card | `card_type = 'challenge'` |
| Team Assist auf einer Karte | `team_assist_used` |
| Team Assist Team 1 | `team1_assist_used` |
| Team Assist Team 2 | `team2_assist_used` |
| UI-Spracheinstellung | `app_settings.ui_locale` |

Domänenneutrale Tabellennamen erhalten keinen Produktpräfix.

## 5. Zentrale Tabellen

Syzeteo 1.0.0 verwendet unter anderem:

- `courses`
- `students`
- `learning_units`
- `questions`
- `rounds`
- `round_questions`
- `games`
- `game_roster`
- `game_cards`
- `game_undo`
- `app_settings`
- die durch `auth.py` angelegten Authentifizierungstabellen

## 6. Question-Pool-Austauschformat

JSON-Import und -Export verwenden:

```json
{
  "format": "Syzeteo question pool",
  "version": 1
}
```

Question-Pool-Importe akzeptieren ausschließlich das native Syzeteo-Format. Andere Formatkennungen und nicht unterstützte Formatversionen werden zurückgewiesen.

CSV steht als menschenlesbares Exportformat zur Verfügung. JSON ist das definierte Austauschformat für den Import zwischen Syzeteo-Installationen.

## 7. Internationalisierungsarchitektur

- Sprachkataloge: `locales/en.json`, `locales/de.json`
- Referenz- und Fallback-Sprache: Englisch (`en`)
- persistente Einstellung: `ui_locale`
- Stellen der Sprachauswahl: Login/Ersteinrichtung und Instructor Settings
- stabile sprachneutrale Seiten-IDs und Domänen-/Statuscodes
- Inhalte des Question Pool sind Nutzerdaten und werden von der Anwendung nicht übersetzt

Die beiden offiziellen Sprachkataloge müssen denselben Schlüsselbestand und kompatible Platzhalter besitzen.

## 8. Technisch erzwungene Domänenregeln

- Eine Runde enthält exakt acht Question Cards und eine Challenge Card.
- Bei regulären Zügen wechseln sich die beiden Teams strikt ab.
- Eine Person darf pro Runde höchstens einen regulären Zug übernehmen.
- Ein Team Assist ist kein regulärer Zug und sperrt die helfende Person nicht für einen späteren regulären Zug.
- Die letzte verbleibende Karte wird unabhängig vom Kartentyp immer vom Instructor beantwortet und mit 0 Punkten abgeschlossen.
- Individuelle Leistungsdaten einzelner Studierender werden weder gespeichert noch ausgewertet.

## 9. Release-Abnahmekriterien

| ID | Kriterium |
|---|---|
| REL-01 | Eine Neuinstallation verwendet `syzeteo.sqlite3`. |
| REL-02 | `SYZETEO_DATA_DIR` ist die unterstützte Environment-Variable für das Datenverzeichnis. |
| REL-03 | Fremde Question-Pool-Formatkennungen werden zurückgewiesen. |
| REL-04 | Neue Exporte verwenden `Syzeteo question pool`, Version 1. |
| REL-05 | Runtime-/UI-Quellcode enthält kein veraltetes Produktbranding. |
| REL-06 | Challenge Cards werden als `challenge` persistiert. |
| REL-07 | Das Schema verwendet die nativen Team-Assist-Felder. |
| REL-08 | Team Assist sperrt die helfende Person nicht für einen späteren regulären Zug. |
| REL-09 | Die letzte Karte ergibt unabhängig vom Kartentyp 0 Punkte. |
| REL-10 | Das Release enthält keine persistente SQLite-Datenbank oder Sicherungsdatei. |
| REL-11 | Das erzeugte SQLite-Schema enthält keine veralteten Produkt-/Domänenkennungen. |
| REL-12 | Runtime-Code enthält keine alten Vorab-Datenbank-/Pfadkennungen. |
| REL-13 | Die SQLite-Schemaversion ist `2` und enthält `app_settings`. |
| REL-14 | Englischer und deutscher Sprachkatalog haben identische Schlüsselbestände und kompatible Platzhalter. |
| REL-15 | Alle im Runtime-Code referenzierten literalen Übersetzungsschlüssel existieren im Referenzkatalog. |

## 10. Release-Verifikation

Für die Syzeteo-1.0.0-Baseline wurden folgende Prüfungen durchgeführt:

- vollständige automatisierte Testsuite: **56/56 Tests erfolgreich**;
- offizielle Sprachkataloge: **jeweils 473 Schlüssel**, identische Schlüsselbestände;
- SQLite-Schemaversion: `2`;
- der Release-Baum enthält keine persistente SQLite-Datenbank, WAL/SHM-Datei oder Sicherung.

## 11. Künftige Schemaänderungen

Nach Veröffentlichung ist die Datenbank Teil der Produktkompatibilität. Spätere Schemaänderungen müssen:

1. die SQLite-Schemaversion bei Bedarf erhöhen,
2. einen expliziten und getesteten Migrationspfad für veröffentlichte Syzeteo-Datenbanken bereitstellen,
3. Datenintegrität und Domänenkonsistenz erhalten und
4. durch automatisierte Regressionstests abgesichert sein.
