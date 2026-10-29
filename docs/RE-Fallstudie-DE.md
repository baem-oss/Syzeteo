# Fallstudie Syzeteo – Das System verstehen

**Lehrmaterial Requirements Engineering · Stand: 29.10.2026**

[Zur Dokumentationsübersicht](README.md) · [Zum durchgearbeiteten Methodenbeispiel](RE-Methodenbeispiel-DE.md)

## 1. Ausgangssituation

Eine Lehrperson will bereits vermittelte Lerninhalte am Ende einer Vorlesung wiederholen. Statt einer klassischen Fragerunde treten zwei Teams gegeneinander an. Die Lehrperson („**Instructor**“) organisiert den Spielbetrieb; die Studierenden beantworten Fragen, steuern das System aber nicht selbst.

In der Realität treten Probleme auf: Studierende kommen zu spät, eine Runde wird irrtümlich gestartet, eine Frage wird später im Fragenpool verändert, oder ein Spiel muss unterbrochen werden. **Requirements Engineering** hilft dabei, solche Situationen vor der Implementierung präzise und widerspruchsfrei zu beschreiben.

### Systemgrenze

| Innerhalb von Syzeteo | Außerhalb von Syzeteo |
|---|---|
| Kurse und Studierende verwalten | Unterrichtsinhalte fachlich erstellen |
| Fragenpool und Spielrunden verwalten | Fachfragen mündlich beantworten |
| Karten zeigen, Züge und Punkte verwalten | Richtigkeit einer Antwort pädagogisch beurteilen |
| Protokoll und Team-/Kursauswertungen bereitstellen | Studierende individuell benoten |
| Spiel abbrechen, löschen oder fortsetzen | Menschliche Entscheidung über einen Spielabbruch |

**Wichtig:** Die Lehrperson vergibt die Punkte. Das Anwendungssystem erkennt nicht eigenständig, ob eine Antwort fachlich richtig ist.

## 2. Fachliches Vokabular

| Begriff | Bedeutung in Syzeteo |
|---|---|
| **Instructor** | Die authentifizierte Lehrperson; primärer menschlicher Akteur |
| **Kurs** | Lehrveranstaltung mit eigenem Teilnehmerbestand und zwei Teams |
| **Lerneinheit** | Gliederung des globalen Fragenpools |
| **Fragenpool** | Kursübergreifende Sammlung aus Fachfragen und Musterantworten |
| **Runde** | Festgelegter Satz aus **acht Fachfragen**; beim Spiel kommt eine Challenge Card hinzu |
| **Spiel** | Durchführung einer bestimmten Runde in einem bestimmten Kurs |
| **Fachfragekarte** | Karte mit Frage/Musterantwort, normalerweise 0 oder 1 Punkt |
| **Challenge Card** | Sonderkarte mit eigener Wertungslogik (bis zu 2 Punkte) |
| **Team Assist** | Unterstützung bei einer Fachfrage durch eine anwesende Person des aktiven Teams |
| **Snapshot** | Beim Spielstart gespeicherter historischer Stand, z. B. Teamname oder Fragetext |
| **Abbruch** | Das Spiel erhält Status `aborted`; es gilt nicht als regulär beendet |
| **Löschung eines abgebrochenen Spiels** | Das Spiel und die zugehörigen Daten werden entfernt; die Runde wird für den Kurs wieder frei |

### Vom Fragenpool zum Spiel

```text
Lerneinheit ── enthält ──> Fachfragen im globalen Pool
                                  │
                             8 auswählen
                                  ▼
                         Runde (Fragensatz)
                                  │
             Kurs + anwesende Studierende + Spielerwahlmodus
                                  ▼
                   Spiel: 8 Fragen + 1 Challenge Card
                                  │
                     Wertung und Statusänderungen
                                  ▼
               Teamstand / Historie / Fragenprotokoll
```

*Dieses Schema zeigt fachliche Objekte und Beziehungen; es ist ausdrücklich **kein UML-Klassendiagramm**.*

## 3. Ein typischer Spielablauf

1. Der Instructor legt einen Kurs an, importiert Studierende und ordnet ihnen zwei Teams zu.
2. Er verwaltet Lerneinheiten und Fachfragen im globalen Fragenpool.
3. Er konfiguriert eine Runde mit genau acht Fachfragen.
4. Vor Spielbeginn bestimmt er die anwesenden Studierenden und den regulären Spielerwahlmodus (zufällig oder manuell ab Spieler 2).
5. Beim Start erzeugt Syzeteo das Spiel mit neun Karten und speichert relevante historische Daten.
6. Eine Karte wird aufgedeckt; der Instructor zeigt die Frage und ggf. die Musterantwort und wertet den Zug.
7. Nach jedem regulären Zug ist das **andere Team** an der Reihe. Ein regulär eingesetzter Studierender wird in derselben Runde nicht erneut regulär ausgewählt.
8. Die **letzte verbleibende Karte** wird unabhängig vom Kartentyp durch den Instructor beantwortet und **nicht** gewertet.
9. Das Spiel endet regulär; die Ergebnisse können später auf Team- und Kursebene betrachtet werden.

Es gibt außerdem definierte Alternativsituationen: Nachzügler aufnehmen, Team Assist einsetzen, letzten Zug rückgängig machen, ein Spiel unterbrechen/fortsetzen oder ein laufendes Spiel abbrechen.

## 4. Zentrale Spiel- und Integritätsregeln

| Regel | Konsequenz für die Spezifikation |
|---|---|
| **GR #03:** Acht Fachfragen + eine Challenge Card | Die Anzahl der Karten ist kein frei wählbarer UI-Parameter |
| **GR #04:** Strikter Teamwechsel | Zufällige und manuelle Spielerwahl dürfen die Regel nicht umgehen |
| **GR #05 / #06:** Regulärer Einsatz einmal; Team Assist als Ausnahme | Zwei unterschiedliche Auswahlregeln müssen modelliert und getestet werden |
| **GR #07:** Letzte Karte durch Instructor, null Punkte | Auch bei einer Challenge Card gilt die Ausnahme |
| **GR #09 / #11:** Runde je Kurs einmal; Abbruch/Löschung | Ein abgebrochenes Spiel wird erst durch seine Löschung wieder für die Runde freigegeben |
| **GR #10:** Kurslöschung vollständig | Kursbezogene Daten müssen weg; globale Fragen und Lerneinheiten bleiben |
| **GR #12:** Individuelle Teamnamen mit Spiel-Snapshot | Spätere Umbenennungen verändern historische Spielstände nicht |
| **GR #13:** Fragenstatistik ohne Instructor-Abschluss und Sonderkarte | Fragenprotokoll und statistische Fragenauswertung besitzen **verschiedene** Einschlusskriterien |
| **NFANF #01:** Keine Individualauswertung | Studierendennamen nur zur Organisation; keine Speicherung/Auswertung individueller Antwortleistungen |
| **NFANF #02:** Rundenbezogene Datenintegrität | Nachträgliche Stammdatenänderungen dürfen frühere Spiele nicht verfälschen |

Die verbindlichen vollständigen Wortlaute stehen in [Randanforderungen, NFANF und Geschäftsregeln](Syzeteo-RANF-etc-DE.md). Diese Tabelle ist eine Orientierung, keine zweite Spezifikation.

## 5. Vier Situationen, in denen RE besonders wichtig ist

### A. Ein Student kommt zu spät

Der Instructor hat das Spiel bereits gestartet. Eine Person soll nachträglich in den Spielerkader aufgenommen werden, aber bereits beantwortete Fragen und Teamstände dürfen nicht verändert werden.

**RE-Fragen:** Welcher Zustand ist vor dem Vorgang erforderlich? Darf eine Person zweimal aufgenommen werden? Welche Rolle spielen Teamzuordnung und Anwesenheit?

**Quellen:** US #03, GR #04–#06, NFANF #02.

### B. Eine Frage wird später überarbeitet

Eine Frage wurde in einer älteren Runde bereits verwendet; ihr Text wird im globalen Pool aktualisiert. Die alte Spielhistorie muss dennoch den damals geltenden Wortlaut bewahren.

**RE-Fragen:** Welche Daten sind global, welche historisch eingefroren? Wie ist „unveränderlich“ prüfbar?

**Quellen:** US #13, #24; GR #02; NFANF #02.

### C. Die Runde wird versehentlich gestartet

Ein laufendes Spiel soll abgebrochen werden; eine Runde darf danach erneut gespielt werden, **aber erst nach der ausdrücklich veranlassten Löschung des abgebrochenen Spiels**.

**RE-Fragen:** Sind „Abbrechen“ und „Löschen“ derselbe Use Case? Was unterscheidet Erfolg und Fehlschlag? Wer bestätigt die Löschung? Welche Daten müssen entfernt werden?

**Quellen:** US #26, GR #09/#11, NFANF #02. Dies ist das [durchgearbeitete RE-Beispiel](RE-Methodenbeispiel-DE.md).

### D. Welche Fragen waren schwierig?

Der Instructor betrachtet eine Statistik der regulär gespielten Fachfragen. Weder Challenge Cards noch Instructor-Abschlusskarten werden als studentischer Versuch gezählt. Im **Fragenprotokoll** kann eine abschließend behandelte letzte Fachfrage dennoch erscheinen.

**RE-Fragen:** Warum genügt „Gespielte Fragen anzeigen“ als Anforderung nicht? Welche Definitionen von *gespielt*, *gewertet* und *auswertbar* sind erforderlich?

**Quellen:** US #24/#28, GR #07/#13, NFANF #01.

## 6. So lesen wir das Requirements-Set

Die fachlichen Artefakte haben unterschiedliche Aufgaben:

| Artefakt | Typische Frage |
|---|---|
| **User Story** | Welches Ziel verfolgt ein Akteur und welchen Nutzen erwartet er? |
| **Use Case** | Wie interagieren Akteur und System im Erfolgs- und Fehlerfall? |
| **BPMN** | In welcher Reihenfolge laufen fachliche Aktivitäten und Entscheidungen ab? |
| **FANF** | Welche konkrete Funktion oder Systemreaktion wird gefordert? |
| **NFANF** | Welche Qualitätseigenschaft oder Einschränkung muss das System erfüllen? |
| **RANF** | Welche vorgegebenen Randbedingungen gelten für die Lösung? |
| **Geschäftsregel (GR)** | Welche fachliche Regel gilt unabhängig von einer konkreten Bildschirmmaske? |
| **Akzeptanzkriterium (AC)** | Woran ist eine bestimmte Nachbedingung objektiv prüfbar? |
| **Traceability** | Wie sind Anforderung, Modell, Regel und Nachweis begründet miteinander verknüpft? |

**Achtung:** Ein BPMN-Diagramm allein ersetzt keine vollständige Anforderungenliste. Und eine User Story enthält im Allgemeinen nicht alle Fehler- und Ausnahmefälle.

## 7. Lernziele und Aufgaben

Nach der Bearbeitung sollte man fachliche Aussagen **richtig klassifizieren**, Interaktionen strukturiert spezifizieren, BPMN-Abläufe erklären und nachvollziehbare Akzeptanzkriterien formulieren können.

**Arbeitsauftrag:** Untersuche [US #26](Syzeteo-L-US-DE.md) und die [beiden Use Cases](Syzeteo-Use-Cases-US26-DE.md). Vergleiche den Abbruch eines laufenden Spiels mit der vollständigen Kurslöschung (US #07). Stelle begründet dar, weshalb sich die Datenfolgen unterscheiden. Zeichne anschließend eine BPMN für „Spiel abbrechen“ und prüfe sie anhand des [bereitgestellten BPMN-Beispiels](RE-Beispiel-Spiel-abbrechen.bpmn).

Weiterführend: [Methodenbeispiel](RE-Methodenbeispiel-DE.md) · [Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md) · [QS-Nachweise](Syzeteo-QS-und-Abnahme-DE.md).
