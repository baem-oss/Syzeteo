# Syzeteo – Dokumentation

**Stand:** 29.10.2026

Diese Dokumentation beschreibt das reale Open-Source-Projekt Syzeteo. Sie dient als **Referenz** für das Verständnis eines Anwendungssystems sowie seiner Anforderungen, Modelle und Prüfungen. Sie ist weder ein Lehrskript noch eine Aufgaben- oder Musterlösungssammlung.

## Projekt und fachliche Spezifikation

| Dokument | Gegenstand |
|---|---|
| [Projektüberblick](Syzeteo-Projektueberblick-DE.md) | Ziel, Systemgrenze, Rollen, Fachbegriffe und Spielablauf |
| [User Stories (DE)](Syzeteo-L-US-DE.md) | 29 Anforderungen aus Anwendersicht |
| [Nichtfunktionale Anforderungen, Randanforderungen und Geschäftsregeln (DE)](Syzeteo-RANF-etc-DE.md) | Übergreifende Eigenschaften, Bedingungen und Spielregeln |
| [Use Cases (DE)](Syzeteo-Use-Cases-US26-DE.md) | Die beiden dokumentierten Interaktionen „Spiel abbrechen“ und „Spiel löschen“ |
| [Traceability-Matrix (DE)](Syzeteo-Traceability-Matrix-DE.md) | Fachlich begründete Anforderungsbeziehungen |
| [Akzeptanzkriterien (JSON)](Syzeteo-Akzeptanzkriterien.json) | 46 konkretisierte Kriterien, IDs und direkte Testreferenzen |
| [Story-Test-Zuordnung (JSON)](Syzeteo-Akzeptanztests-Mapping.json) | Zuordnung zwischen User Stories und automatisierten Tests |
| [Qualitätssicherung und Abnahmestand](Syzeteo-QS-und-Abnahme-DE.md) | Umfang und Grenzen von Testnachweisen, CI und manuellen Prüfungen |

Die Anforderungen sind in den oben aufgeführten Originaldokumenten maßgeblich. Der Projektüberblick erläutert den Zusammenhang, ersetzt aber keine Spezifikation. Die Akzeptanzkriterien dokumentieren **Teilnachweise**, keine vollständige fachliche Abnahme jeder User Story.

**Umfang des Bestands:** Die beiden Use Cases zu US #26 sind ausgearbeitet; eine vollständige UC- oder BPMN-Spezifikation sämtlicher Funktionen gehört derzeit nicht zur Projektdokumentation. Es werden keine zusätzlichen, nur für die Lehre erfundenen Anforderungen oder Prozessmodelle als verbindlich ausgegeben.

## Weitere Referenzen

| Dokument | Gegenstand |
|---|---|
| [User Stories (EN)](Syzeteo-L-US-EN.md) | Englische Fassung |
| [Anforderungen und Geschäftsregeln (EN)](Syzeteo-RANF-etc-EN.md) | Englische Fassung |
| [Use Cases (EN)](Syzeteo-Use-Cases-US26-EN.md) | Englische Fassung |
| [Traceability-Matrix (EN)](Syzeteo-Traceability-Matrix-EN.md) | Englische Fassung |
| [Technische Baseline (DE)](Syzeteo-Technical-Baseline-DE.md) | Dokumentierter technischer Versionsstand |
| [Technische Baseline (EN)](Syzeteo-Technical-Baseline-EN.md) | Englische Fassung |
| [Versionsarchiv](archiv/README.md) | Frühere technische Baselines, Migrations- und i18n-Dokumente |
| [README.de.md](../README.de.md) | Installation und Betrieb |

Die beiden Dateien `Syzeteo-TDD-Baseline.json` und `Syzeteo-Akzeptanzkriterien-Baseline.json` sind historische technische Vergleichsstände für die Qualitätssicherung. Sie bleiben am bisherigen Ort, weil die CI auf diese Pfade zugreift.
