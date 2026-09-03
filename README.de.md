# Syzeteo

**Knowledge. Teams. Rounds.**

*An open-source team-based active recall game for the classroom.*

Syzeteo ist ein Streamlit-basiertes Teamspiel zur strukturierten Wiederholung von Wissen im Unterricht und in Lehrveranstaltungen. Der Instructor verwaltet Kurse, Studierende, Fragen und Runden, führt Spiele durch und wertet Ergebnisse ausschließlich auf Team- und Kursebene aus.

## Warum Syzeteo?

Der Name geht auf das altgriechische **συζητέω (syzēteō)** zurück und bedeutet sinngemäß *gemeinsam suchen oder untersuchen* sowie – je nach Kontext – *miteinander diskutieren oder fragen*. Das beschreibt die Grundidee der Anwendung: Studierende aktivieren Wissen, beantworten Fragen und lernen gemeinsam im Team.

## Kernprinzipien

- zwei Teams mit strikt wechselnden regulären Zügen;
- acht Question Cards plus eine Challenge Card pro Runde;
- zufällige oder manuelle reguläre Spielerwahl ab Spieler 2;
- pro Person höchstens ein regulärer Einsatz je Runde;
- Team Assist als Ausnahme: ein Einsatz über Team Assist zählt nicht als regulärer Zug;
- die letzte verbleibende Karte wird immer vom Instructor beantwortet und mit 0 Punkten abgeschlossen;
- keine Individualauswertung;
- laufende Spiele können abgebrochen werden; ausschließlich abgebrochene Spiele können vom Instructor gelöscht werden;
- persistente SQLite-Datenhaltung und Docker-Betrieb;
- vollständig englische und deutsche Anwendungsoberfläche.

## Schnellstart mit Docker

```bash
docker compose up -d --build
```

Syzeteo ist standardmäßig über Host-Port `8502` erreichbar.

Beim ersten Start wird in der Anwendung der einzige Instructor-Account eingerichtet. Bei einer Neuinstallation wird automatisch `persistent/syzeteo.sqlite3` erzeugt.

## Lokaler Start

```bash
python -m pip install -r requirements.txt
streamlit run app.py
```

## Internationalisierung

Englisch und Deutsch stehen über JSON-Sprachkataloge zur Verfügung; Englisch ist Referenz- und Fallback-Sprache. Die Sprachauswahl wird bewusst nur auf der Login-/Ersteinrichtungsseite und in den Instructor Settings angeboten. Die gespeicherte Standardsprache wird bei zukünftigen Anmeldungen wiederverwendet.

Sämtliche Seiten der Anwendungsoberfläche sind internationalisiert. Navigation, Filter, Konfigurationshinweise, Undo-Aktionen und Domänenfehler verwenden intern sprachneutrale IDs bzw. Codes. Inhalte des Question Pool bleiben Nutzerdaten und werden bewusst nicht automatisch übersetzt.

## Spielmodell

Eine Runde umfasst exakt acht Question Cards und eine Challenge Card. Die Karten werden für jedes Spiel gemischt. Beide Teams wechseln sich bei regulären Zügen strikt ab.

Die Challenge Card wird im normalen Spielverlauf nach ihrer besonderen Wertungslogik behandelt. Ist eine beliebige Karte die letzte verbleibende Karte, beantwortet sie der Instructor; unabhängig vom Kartentyp werden dafür keine Punkte vergeben.

Eine Person darf pro Runde höchstens einmal regulär eingesetzt werden. Ein Team Assist gilt nicht als regulärer Einsatz. Eine helfende Person bleibt deshalb für einen späteren regulären Zug verfügbar.

## Privacy by Design

Syzeteo erfasst und bewertet keine individuellen Leistungen einzelner Studierender. Namen dienen ausschließlich organisatorischen Zwecken wie Teamzuordnung, Anwesenheit, Spielerwahl und Team Assist. Punkte, Statistiken und Ergebnisse werden ausschließlich auf Team- oder Kursebene gespeichert und dargestellt.

## Question Pool: Import und Export

Syzeteo verwendet für JSON-Import und -Export:

```json
{
  "format": "Syzeteo question pool",
  "version": 1
}
```

Question-Pool-Importe und -Exporte verwenden ausschließlich das oben dargestellte Syzeteo-Format.

## Datenverzeichnis und Datenbank

Optional kann folgende Environment-Variable gesetzt werden:

```text
SYZETEO_DATA_DIR
```

Ohne diese Variable verwendet Syzeteo `./persistent`. Die Datenbankdatei heißt immer:

```text
syzeteo.sqlite3
```

Syzeteo 1.1.0 verwendet SQLite-Schemaversion `2` (`PRAGMA user_version`). Anwendungs- und SQLite-Schemaversion sind bewusst voneinander unabhängig. Im persistenten Domänenmodell werden unter anderem `challenge`, `team_assist_used`, `team1_assist_used` und `team2_assist_used` verwendet.


## Upgrade von 1.0.0

Syzeteo 1.1.0 verwendet weiterhin SQLite-Schemaversion `2`. Eine Datenmigration ist nicht erforderlich. Bestehende 1.0.0-Daten können unverändert weiterverwendet werden. Vor einem Wechsel des Anwendungscodes wird dennoch eine konsistente Sicherung von `persistent/` empfohlen.

## Tests

```bash
python -m unittest discover -v
```

Das Release enthält Regressionstests, Release-Abnahmetests und Konsistenztests für die Internationalisierung. Die Release-Testsuite von Syzeteo 1.1.0 umfasst **62 automatisierte Tests**.

## Spezifikation

Im Verzeichnis `docs/` liegen User Stories, Anforderungen/Geschäftsregeln und Traceability Matrix jeweils in deutscher und englischer Fassung sowie technische Baseline und Internationalisierungsspezifikation für Syzeteo 1.1.0.

## Repository-Hygiene

Das öffentliche Repository darf keine produktiven Datenbanken, SQLite-WAL/SHM-Dateien, Backups, reale Studierendenlisten, Accountdaten oder Lehrinhalte mit ungeklärten Veröffentlichungsrechten enthalten. Die mitgelieferte CSV enthält ausschließlich fiktive Demonstrationsnamen.

## Lizenz

Syzeteo steht unter der **Apache License 2.0**. Siehe [`LICENSE`](LICENSE).

Die Apache License 2.0 gilt für den Syzeteo-Quellcode und die originäre Projektdokumentation. Vor der Veröffentlichung oder Weitergabe zusätzlicher Fragensätze, Lehrmaterialien oder sonstiger Inhalte Dritter muss deren Veröffentlichungsberechtigung separat geprüft werden.
