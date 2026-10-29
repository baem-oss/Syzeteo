# Syzeteo – Projektüberblick

**Stand:** 29.10.2026 · [Dokumentationsübersicht](README.md)

## Gegenstand und Ziel

Syzeteo ist eine quelloffene, webbasierte Anwendung zur Wiederholung von Lehrinhalten in Form eines Teamspiels. Eine Lehrperson (**Instructor**) verwaltet die Kurse, Studierenden, Fragen und Spielrunden, steuert den Spielablauf und dokumentiert Ergebnisse.

Die Anwendung wird in der Lehre eingesetzt. Das Repository mit seinen Anforderungen, Modellen, Tests und Implementierungsdateien kann zugleich als **reales Referenzprojekt für Requirements Engineering** betrachtet werden. Die Dokumentation enthält keine Arbeitsaufträge für Studierende.

## Systemgrenze und Akteure

Der **Instructor** ist der primäre Benutzer des Systems. Die Studierenden nehmen am Spiel teil, bedienen die Anwendung aber nicht selbst.

| Aufgabe von Syzeteo | Außerhalb der Systemgrenze |
|---|---|
| Kurse und Studierende verwalten | Lehrveranstaltungsinhalte festlegen |
| Studierende Teams zuordnen und Anwesenheit erfassen | Tatsächliche Anwesenheit feststellen |
| Globale Fachfragen und Runden verwalten | Fachliche Qualität der Fragen beurteilen |
| Spielstand, Karten und Teampunkte verwalten | Richtigkeit einer Antwort pädagogisch beurteilen |
| Gespielte Fragen protokollieren und Teamergebnisse auswerten | Individuelle Leistungen benoten |

Die fachliche Entscheidung, ob eine Antwort richtig oder falsch ist, trifft der Instructor. Syzeteo berechnet daraus die vom Instructor festgelegte Teamwertung.

## Zentrale Fachbegriffe

| Begriff | Bedeutung |
|---|---|
| **Kurs** | Lehrveranstaltung mit eigenem Studierendenbestand und zwei Teams |
| **Lerneinheit** | Fachliche Gliederung des globalen Fragenpools |
| **Fragenpool** | Kursübergreifende Fachfragen und zugehörige Musterantworten |
| **Runde** | Festgelegter Satz von genau acht Fachfragen |
| **Spiel** | Durchführung einer Runde mit anwesenden Studierenden eines Kurses |
| **Challenge Card** | Zusätzliche Sonderkarte einer Runde |
| **Team Assist** | Unterstützung durch eine anwesende Person des aktiven Teams |
| **Snapshot** | Beim Spielstart bzw. beim Festlegen einer Runde gespeicherter historischer Datenstand |
| **Spielstatus** | Beispielsweise `running`, `finished` oder `aborted` |

## Fachlicher Ablauf im Überblick

1. Der Instructor legt einen Kurs an, erfasst Studierende und ordnet sie zwei Teams zu.
2. Er verwaltet den globalen Fragenpool und stellt acht Fachfragen für eine Runde zusammen.
3. Vor Spielbeginn bestimmt er die anwesenden Personen sowie den Spielerwahlmodus.
4. Syzeteo startet ein Spiel mit acht Fachfragekarten und einer Challenge Card.
5. Karten werden aufgedeckt und durch den Instructor gewertet. Die regulären Züge wechseln zwischen den Teams.
6. Das Spiel wird regulär abgeschlossen oder bei Bedarf unterbrochen bzw. abgebrochen.
7. Ergebnisse stehen auf Team-/Kursebene zur Verfügung; abgeschlossene Fachfragen werden nach den fachlichen Regeln protokolliert.

## Ausgewählte fachliche Besonderheiten

- **Letzte Karte:** Die letzte verbleibende Karte wird immer vom Instructor beantwortet und bringt unabhängig vom Kartentyp keine Punkte (GR #07).
- **Spielerwahl:** Es gibt eine Startspielerauswahl und einen getrennt festgelegten regulären Spielerwahlmodus. Der strikte Teamwechsel bleibt bestehen.
- **Team Assist:** Eine Person kann zur Unterstützung herangezogen werden. Das ist nicht mit einem regulären Einsatz gleichzusetzen.
- **Datenintegrität:** Änderungen an globalen Fragen, Studierenden oder Teamnamen dürfen den historischen Stand bereits gestarteter Spiele nicht rückwirkend verfälschen (NFANF #02).
- **Spielabbruch:** Abbrechen und anschließendes Löschen sind unterschiedliche Vorgänge. Die Runde wird erst nach Löschung eines abgebrochenen Spiels für den Kurs wieder frei (GR #09/#11).
- **Keine Individualauswertung:** Namen dienen organisatorischen Zwecken; Punkte und Statistiken werden nicht einzelnen Studierenden als Leistungsdaten zugeordnet (NFANF #01).
- **Protokoll versus Statistik:** Eine letzte abschließend behandelte Instructor-Fachfrage kann im Fragenprotokoll erscheinen, zählt aber nicht als studentischer Versuch in der statistischen Fragenauswertung (GR #07/#13).

Die rechtsverbindliche bzw. fachlich maßgebliche Formulierung dieser Regeln steht ausschließlich im [Anforderungskatalog](Syzeteo-RANF-etc-DE.md). Die Aufzählung ist eine Zusammenfassung.

## Verfügbare RE-Artefakte

| Artefakt | Bestand |
|---|---|
| [User Stories](Syzeteo-L-US-DE.md) | 29 fachliche User Stories |
| [Geschäftsregeln, NFANF und RANF](Syzeteo-RANF-etc-DE.md) | Fachliche Regeln und übergreifende Bedingungen |
| [Use Cases](Syzeteo-Use-Cases-US26-DE.md) | Zwei ausgearbeitete Use Cases zu US #26 („Spiel abbrechen“, „Spiel löschen“) |
| [Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md) | Begründete Zuordnungen zwischen User Stories und weiteren Anforderungen |
| [Akzeptanzkriterien](Syzeteo-Akzeptanzkriterien.json) | 46 maschinenlesbare, konkretisierte Teilkriterien mit Testreferenzen |
| [Test-Mapping](Syzeteo-Akzeptanztests-Mapping.json) | Zuordnung der User Stories zu automatisierten Tests |

**Umfangsgrenze:** Das Repository enthält keine vollständige UC-Sammlung für alle User Stories und kein verbindliches BPMN-Referenzmodell aller Prozesse. Die vorhandenen Artefakte dokumentieren den tatsächlichen Projektstand und werden nicht zu Lehrzwecken künstlich ergänzt.

## Technischer Überblick

Syzeteo ist in Python mit **Streamlit** implementiert, verwendet **SQLite** zur Persistenz und kann über **Docker** betrieben werden. Tests und Qualitätsprüfungen laufen über eine GitHub-Actions-Pipeline. Einzelheiten zur Installation stehen in [README.de.md](../README.de.md); der dokumentierte technische Versionsstand und ältere Versionen sind über die [Dokumentationsübersicht](README.md) zugänglich.
