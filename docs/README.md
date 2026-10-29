# Syzeteo – Dokumentation

**Requirements Engineering am realen Open-Source-System** · Stand: 29.10.2026

Syzeteo ist ein webbasiertes Teamspiel zum Wiederholen von Lehrinhalten. Diese Dokumentation ist so aufgebaut, dass man zunächst das System versteht, dann Anforderungen **modelliert** und anschließend ihre **Prüfbarkeit** nachvollzieht.

> **Einstieg für Studierende:** Mit der [Fallstudie](RE-Fallstudie-DE.md) beginnen, danach das [durchgearbeitete Methodenbeispiel](RE-Methodenbeispiel-DE.md) bearbeiten. Programmierkenntnisse sind für die RE-Fallstudie nicht erforderlich.

## 1. Leseweg für die RE-Lehre

| Schritt | Dokument | Was lerne ich? |
|---|---|---|
| 1 | [Fallstudie: System, Akteure, Spielregeln](RE-Fallstudie-DE.md) | Problem verstehen, Systemgrenze, Begriffe und fachlichen Ablauf |
| 2 | [Methodenbeispiel: US → UC → BPMN → FANF/NFANF/RANF → AC → Traceability](RE-Methodenbeispiel-DE.md) | Verschiedene Spezifikationsformen unterscheiden und aufeinander beziehen |
| 3 | [29 User Stories](Syzeteo-L-US-DE.md) | Anforderungen aus Sicht eines Anwenders |
| 4 | [Randanforderungen, nichtfunktionale Anforderungen und Geschäftsregeln](Syzeteo-RANF-etc-DE.md) | Bedingungen, die durch eine reine User Story nicht hinreichend präzisiert werden |
| 5 | [Use Cases: Spiel abbrechen und Spiel löschen](Syzeteo-Use-Cases-US26-DE.md) | Ausführliche, strukturierte Interaktionen und Alternativabläufe |
| 6 | [Traceability-Matrix](Syzeteo-Traceability-Matrix-DE.md) | Fachlich begründete Beziehungen, Querschnittsregeln und Rückwärtsverfolgung |
| 7 | [Akzeptanzkriterien und Qualitätssicherung](Syzeteo-QS-und-Abnahme-DE.md) | Wie prüfbare Nachbedingungen und Testnachweise dokumentiert werden |

**Für ein BPMN-Werkzeug:** [BPMN-2.0-Beispiel „Spiel abbrechen“](RE-Beispiel-Spiel-abbrechen.bpmn) (editierbares XML mit Diagrammkoordinaten).

## 2. Was ist verbindlich – und was ist ein Lehrbeispiel?

| Status | Artefakte |
|---|---|
| **Verbindliche fachliche Quelle** | User Stories, `Syzeteo-RANF-etc-DE.md`, die zwei freigegebenen Use Cases und die fachliche Traceability-Matrix |
| **Verbindliche technische Kriterien-/Testzuordnung** | [Akzeptanzkriterien (JSON)](Syzeteo-Akzeptanzkriterien.json) und [Story-Test-Mapping (JSON)](Syzeteo-Akzeptanztests-Mapping.json) |
| **Didaktische Ableitung / Lernbeispiel** | `RE-Methodenbeispiel-DE.md`, einschließlich der beispielhaft abgeleiteten **FANF**; sie sind **keine** zusätzlich beschlossenen Produktanforderungen |
| **Qualitäts- und Entwicklungsnachweis** | `Syzeteo-QS-und-Abnahme-DE.md`, Tests und CI-Workflow; diese Nachweise ersetzen keine vollständige fachliche Abnahme |
| **Historische Technikstände** | [Technische Dokumente und Versionsarchiv](archiv/README.md), nicht Ausgangspunkt der RE-Lehre |

Die englischsprachigen Fassungen der fachlichen Dokumente ([US](Syzeteo-L-US-EN.md), [Anforderungen und Regeln](Syzeteo-RANF-etc-EN.md), [UC](Syzeteo-Use-Cases-US26-EN.md), [Traceability](Syzeteo-Traceability-Matrix-EN.md)) dienen der ergänzenden Lektüre. Bei Abweichungen ist für diese Fallstudie der aktuelle **deutsche Fachstand** maßgeblich.

## 3. Lehrumfang und Modellierungsregeln

Im Mittelpunkt stehen **User Stories (US), Use Cases (UC), BPMN, funktionale Anforderungen (FANF), nichtfunktionale Anforderungen (NFANF), Randanforderungen (RANF)**. Traceability dient als **Ausblick und Qualitätskontrolle**, nicht als eigenständige Modellierungsübung mit einer Vielzahl künstlicher Verknüpfungen.

- **Eine User Story kann durch mehrere Use Cases konkretisiert werden.** Beispiel: US #26 → „Spiel abbrechen“ und „Spiel löschen“.
- **Use Cases beschreiben Interaktion, BPMN den Ablauf eines Geschäftsprozesses.** Das sind keine austauschbaren Darstellungen.
- **FANF, NFANF, RANF und Geschäftsregeln** dürfen nicht vermischt werden. Die Geschäftsregel `GR #11` ist nicht automatisch eine nichtfunktionale Anforderung.
- **Ein Testname ist kein Beweis.** Ein Akzeptanzkriterium braucht eine fachlich passende Assertion; ein UI-Test kann zusätzlich manuelle Sichtprüfung verlangen.
- **Keine Individualauswertung:** Studierendennamen werden nur für die Spielorganisation verwendet; Leistungsdaten werden ausschließlich nach Team/Kurs ausgewertet (NFANF #01).

## 4. Technische und historische Nachweise

- [QS, Tests, CI und dokumentierte UI-Abnahmen](Syzeteo-QS-und-Abnahme-DE.md)
- [Aktuelle technische Referenz (Stand 1.1.1)](Syzeteo-Technical-Baseline-DE.md) – ein **technischer Versionsstand**, keine Aussage über den aktuellen Entwicklungsumfang
- [Versionsarchiv](archiv/README.md) – frühere Baselines, Migrations- und i18n-Spezifikationen
- [Repository und Quellcode](../README.de.md) – Installation und Betrieb

**Pflegeprinzip:** Anforderungen stehen an genau einer fachlich verbindlichen Stelle; zusätzliche Lehrtexte erläutern und verlinken sie, schreiben sie aber nicht neu.
