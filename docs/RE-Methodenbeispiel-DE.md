# RE-Methoden am Beispiel von Syzeteo

**Ein durchgängiges Lehrbeispiel: „Ein laufendes Spiel abbrechen und gegebenenfalls löschen“ (US #26)**

[Zur Übersicht](README.md) · [Zur Fallstudie](RE-Fallstudie-DE.md)

> **Lesehinweis:** Die folgenden FANF sind **didaktisch abgeleitete Beispielanforderungen**, keine zusätzlich freigegebenen Syzeteo-Produktanforderungen. Verbindlich sind die verlinkten Originalartefakte. Das Beispiel zeigt die Methode, nicht eine nachträgliche Änderung der Geschäftslogik.

## 1. Die Ausgangssituation

Der Instructor hat aus Versehen die falsche Runde gestartet. Das laufende Spiel soll nicht in die reguläre Auswertung eingehen. Er bricht es ab. Später kann er das abgebrochene Spiel ausdrücklich löschen; erst dadurch darf er dieselbe Runde im selben Kurs erneut starten.

Die zentrale Unterscheidung lautet:

```text
Nicht begonnen ──Start──> Running ──regulär abschließen──> Finished
                             │
                             └──Abbrechen──> Aborted ──Löschen──> [kein Spiel mehr]
```

**Dieses Textschema ist eine Zustandsübersicht, kein BPMN-Diagramm.** Die Zustandsübergänge sollen fachlich erklärt werden; eine Zustandsmodellierung und eine Prozessmodellierung sind unterschiedliche Modelltypen.

Das Beispiel beruht auf [US #26](Syzeteo-L-US-DE.md), [GR #09/#11](Syzeteo-RANF-etc-DE.md) und den [zwei spezifizierten Use Cases](Syzeteo-Use-Cases-US26-DE.md).

## 2. Schritt 1 – User Story (US)

Die verbindliche US #26 beschreibt in der bekannten Form **Rolle → Absicht → Nutzen**:

- **Rolle:** Instructor.
- **Absicht:** Laufendes Spiel abbrechen und ein abgebrochenes Spiel auf der Instructor-Seite löschen.
- **Nutzen:** Fehlstarts blockieren nicht dauerhaft den Spielbetrieb und die Rundenabdeckung.

Die Story beantwortet das **Warum** und **Was** auf Zielebene. Sie sagt noch nicht vollständig, wann eine Löschung zulässig ist oder was bei einem Abbruch der Bestätigung geschieht.

**Merksatz:** Eine US ist kein Klickprotokoll. Sie kann mehrere Use Cases erfordern.

## 3. Schritt 2 – Use Cases (UC)

Für US #26 sind tatsächlich **zwei** Use Cases dokumentiert:

| Use Case | Vorbedingung | Erfolgsnachbedingung | Wichtige Alternative |
|---|---|---|---|
| [Spiel abbrechen](Syzeteo-Use-Cases-US26-DE.md) | Spielstatus `running` | Status `aborted`; nicht fortsetzbar und nicht regulär abgeschlossen | Instructor verwirft die Bestätigung; Spiel bleibt `running` |
| [Spiel löschen](Syzeteo-Use-Cases-US26-DE.md) | Ein abgebrochenes Spiel ist auf der Instructor-Seite ausgewählt | Spiel und ausschließlich spielbezogene Daten entfernt; Runde für den Kurs wieder offen | Instructor verwirft die Löschung; Daten bleiben erhalten |

Das **Use-Case-Template** ist verpflichtend: **Use Case** (Verb + Objekt, zwei oder drei Wörter), **Ziel**, **Vorbedingung**, **Nachbedingung Erfolg**, **Nachbedingung Fehlschlag**, **Akteure**, **Auslösendes Ereignis**, **Beschreibung** (nummerierte Schritte), **Erweiterungen** (etwa `2a`) und **Alternativen**. Die vollständigen Formulierungen und Schrittnummern stehen in der [UC-Originaldatei](Syzeteo-Use-Cases-US26-DE.md), die hier nicht dupliziert wird.

**Unterschied der Nachbedingungen:** „abgebrochen“ bedeutet **noch gespeichert**; „gelöscht“ bedeutet **nicht mehr vorhanden**. Wer beides gleichsetzt, verletzt GR #09/#11.

## 4. Schritt 3 – Geschäftsprozess mit BPMN

Die BPMN modelliert den **fachlichen Ablauf**, einschließlich Rollen und Entscheidungen. Das [editierbare BPMN-2.0-Modell „Spiel abbrechen“](RE-Beispiel-Spiel-abbrechen.bpmn) kann in einen BPMN-Editor importiert werden.

**Leseschlüssel zum Modell:**

- **Pool:** Gemeinsamer Vorgang „Spiel abbrechen“ mit zwei **Lanes** (Instructor und Syzeteo).
- **Startereignis:** Instructor löst „Spiel abbrechen“ aus.
- **Aufgaben:** Bestätigung anfordern, bestätigen/abbrechen, Status ändern und Ergebnis anzeigen.
- **Exklusives Gateway (XOR):** Bestätigt der Instructor den Abbruch? Nur ein Pfad ist möglich.
- **Endereignisse:** „Spiel abgebrochen“ bzw. „Abbruch verworfen“.

**Wichtige Grenze:** Das BPMN-Modell betrachtet den **Abbruch**, nicht den separaten Vorgang **Löschung**. Das Löschen kann später durch einen neuen Use Case ausgelöst werden. In einer BPMN sollten nicht heimlich zusätzliche Funktionen oder technische Implementierungsdetails erfunden werden.

**BPMN ist kein Flowchart mit beliebigen Symbolen.** Aufgaben, Ereignisse, Gateways, Sequenzflüsse, Pools und Lanes haben jeweils eine definierte Semantik. Ein UML-Aktivitätsdiagramm oder eine Mermaid-Skizze ist kein Ersatz für ein BPMN-2.0-Modell.

## 5. Schritt 4 – Funktionale Anforderungen (FANF)

FANF präzisieren beobachtbares **Systemverhalten**. Hier sind vier **Lehrbeispiele**, die aus US #26, UC und GR #11 abgeleitet werden. Sie sind ausdrücklich **nicht** im Produktanforderungskatalog neu beschlossen.

| Didaktische ID | Beispiel einer funktionalen Anforderung | Herkunft |
|---|---|---|
| **FANF-DEMO-01** | Syzeteo muss dem Instructor die Möglichkeit bieten, ein laufendes Spiel nach einer Bestätigung abzubrechen. | US #26; UC „Spiel abbrechen“ |
| **FANF-DEMO-02** | Syzeteo muss den Status eines erfolgreich abgebrochenen Spiels auf `aborted` setzen und seine Fortsetzung verhindern. | GR #11; UC „Spiel abbrechen“ |
| **FANF-DEMO-03** | Syzeteo muss die Löschung eines abgebrochenen Spiels nach einer gesonderten Bestätigung ermöglichen und ausschließlich spielbezogene Daten mitentfernen. | GR #11; UC „Spiel löschen“ |
| **FANF-DEMO-04** | Syzeteo muss die betreffende Runde im betreffenden Kurs nach der Löschung des abgebrochenen Spiels wieder als offen behandeln. | GR #09/#11; UC „Spiel löschen“ |

**Prüffrage:** Ist die Anforderung beobachtbar und testbar? „Syzeteo soll modern und intuitiv sein“ ist keine ausreichend präzise FANF. „Nach der bestätigten Löschung ist die Runde wieder startbar“ dagegen schon.

## 6. Schritt 5 – NFANF, RANF und Geschäftsregeln auseinanderhalten

| Kategorie | Aussage am Fallbeispiel | Warum gehört sie dorthin? |
|---|---|---|
| **FANF** | Ein abgebrochenes Spiel kann gelöscht werden. | Geforderte Funktion bzw. Systemreaktion |
| **NFANF #02** | Historische Spiel- und Protokolldaten dürfen nicht durch beliebige Stammdatenänderungen verfälscht werden; ausdrücklich vorgesehene Löschungen sind Ausnahmen. | Datenintegrität über verschiedene Funktionen hinweg |
| **RANF #01** | Ein Software-Update muss bestehende fachliche Daten konsistent erhalten. | Technische Migrationsrandbedingung; nicht auf jede reguläre Löschung anzuwenden |
| **GR #11** | Nur abgebrochene Spiele dürfen über die Löschfunktion entfernt werden. | Fachliche Zulässigkeitsregel |
| **GR #09** | Eine Runde darf pro Kurs nur einmal regulär durchgeführt werden; nach Löschung eines abgebrochenen Spiels ist sie wieder offen. | Kursübergreifend wirksame Geschäftsregel |

**Nicht verwechseln:** NFANF #01 untersagt individuelle Leistungsanalysen. Das ist eine fachübergreifende **Qualitäts-/Datenschutzanforderung**, auch wenn zu ihrer Durchsetzung funktionales Verhalten nötig sein kann. GR #11 bleibt eine **Geschäftsregel** und wird nicht durch Umbenennung zu einer NFANF.

Die vollständige verbindliche Liste steht in [Syzeteo-RANF-etc-DE.md](Syzeteo-RANF-etc-DE.md).

## 7. Schritt 6 – Akzeptanzkriterium und Nachweis

Im maschinenlesbaren [Kriterienkatalog](Syzeteo-Akzeptanzkriterien.json) steht **AC-US26-01** sinngemäß:

> Gegeben ist ein laufendes Spiel. Wenn der Instructor es abbricht und anschließend löscht, dann verschwinden das Spiel und seine Daten; dieselbe Runde kann im selben Kurs wieder gestartet werden.

Der **konkrete automatisierte Teilnachweis** liegt unter anderem in
`test_tdd_phase2_remaining.py::test_us26_aborted_game_deletion_removes_cards_and_releases_round`.

Dort werden nach Abbruch und Löschung die Nicht-Existenz des Spiels und seiner Karten sowie die Möglichkeit eines erneuten Starts geprüft. Das ist **ein überprüfbarer Teilaspekt**, nicht automatisch die vollständige Abnahme aller UC-Alternativpfade.

### Positiv- und Negativfall

| Fall | Gegeben | Wenn | Erwartetes Ergebnis |
|---|---|---|---|
| Positiv | Status `running` | Instructor bricht ab, bestätigt Löschung | Spiel und spielbezogene Daten entfernt; Runde wieder offen |
| Negativ | Status `finished` | Instructor versucht die Löschfunktion | Löschung nicht erlaubt, Historie bleibt erhalten |
| Abgebrochene Bestätigung | Spiel läuft | Instructor verwirft Abbruch | Spiel bleibt laufend und unverändert |

**Didaktischer Kern:** Ein gutes AC nennt **Ausgangslage, Handlung und beobachtbares Ergebnis**. Das bloße Vorhandensein einer Testmethode ohne passende Assertions wäre kein belastbarer Nachweis. Für den Negativfall sind weitere Tests relevant; siehe `test_game_abort.py`.

## 8. Schritt 7 – Traceability (Ausblick)

Eine kleine **Lehrmatrix** zeigt fachlich begründete Beziehungen; `FANF-DEMO-*` sind hier nur didaktische Zwischenschritte:

| US | UC | FANF-Beispiel | Regeln / Randbedingungen | Akzeptanznachweis |
|---|---|---|---|---|
| US #26 | Spiel abbrechen | FANF-DEMO-01/-02 | GR #11; NFANF #02 | Teil von AC-US26-01; `test_game_abort.py` |
| US #26 | Spiel löschen | FANF-DEMO-03/-04 | GR #09/#11; NFANF #02 | AC-US26-01 |
| US #07 | Kurse verwalten | *Nicht in dieser Fallstudie ausgearbeitet* | GR #10; NFANF #02 | AC-US07-01 |

Die [verbindliche Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md) führt US zu fachlichen Regeln und Querschnittsanforderungen. Das maschinenlesbare [Testmapping](Syzeteo-Akzeptanztests-Mapping.json) verbindet Stories mit konkreten Tests.

**Zwei wichtige Traceability-Regeln:**

1. **Keine künstlichen Links:** Eine Beziehung muss inhaltlich begründet werden, nicht allein durch ähnliche Begriffe.
2. **Keine falschen 1:1-Annahmen:** Eine US kann mehrere UC, eine GR kann viele US betreffen, und ein Test kann mehrere Kriterien berühren.

## 9. Typische Modellierungsfehler

| Häufiger Fehler | Korrektur |
|---|---|
| „Spiel abbrechen“ und „Spiel löschen“ als identischer Vorgang | Zwei getrennte UC mit unterschiedlichen Vor- und Nachbedingungen |
| GUI-Buttons als fachlichen Prozess behandeln | In BPMN zuerst Aktivitäten, Entscheidungen und Verantwortlichkeiten modellieren |
| Die technische Datenbanktransaktion als User Story formulieren | Fachliche Nutzerabsicht und beobachtbares Ergebnis zuerst |
| GR #11 als NFANF etikettieren | Geschäftsregel von Qualitätsanforderung unterscheiden |
| `PASS` einer UI-Abnahme als vollständige Fachabdeckung lesen | Prüfumfang und Evidenzgrenzen explizit dokumentieren |
| Alle US pauschal mit jeder Querschnittsregel verknüpfen | Nur fachlich begründete Links ausweisen; globale Regeln separat dokumentieren |

## 10. Übungsaufgaben

1. **US → UC:** Überführe US #03 „Nachzügler aufnehmen“ in einen UC nach dem verbindlichen Template. Berücksichtige insbesondere bereits vorhandene Spielerkader und ungültige Teamzuordnungen.
2. **BPMN:** Modelliere den zweiten UC „Spiel löschen“ mit Bestätigung, Abbruch der Löschung und Erfolgspfad. Verwende BPMN-2.0-Notation und benenne die Lanes.
3. **Anforderungsklassifikation:** Ordne NFANF #01, GR #07, GR #11 und RANF #01 korrekt ein. Begründe, weshalb keine davon allein eine User Story ist.
4. **Akzeptanztest:** Formuliere für US #24 zwei Given-When-Then-Szenarien: „nur aufgedeckte Karte“ und „letzte Instructor-Fachfrage“. Unterscheide Fragenprotokoll von Fragenstatistik.
5. **Traceability:** Vergleiche deine begründeten Links mit der [Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md), ohne die Matrix einfach zu kopieren.

**Quellen und Status:** [Original-User-Stories](Syzeteo-L-US-DE.md) · [Original-Use-Cases](Syzeteo-Use-Cases-US26-DE.md) · [Geschäftsregeln](Syzeteo-RANF-etc-DE.md) · [QS-Nachweise](Syzeteo-QS-und-Abnahme-DE.md).
