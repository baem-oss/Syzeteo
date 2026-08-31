# Syzeteo – Traceability Matrix

Stand: 31.08.2026

Quellenbasis: `Syzeteo-L-US-DE.md`, `Syzeteo-RANF-etc-DE.md` und `Syzeteo-Use-Cases-US26-DE.md`

## 1. Prüfgrundsatz

Die Matrix enthält nur fachlich oder normativ belastbare Beziehungen. Reine technische oder lediglich mittelbare Abhängigkeiten werden nicht als Trace-Link ausgewiesen.

Querschnittsanforderungen werden dort gesondert ausgewiesen, wo eine Wiederholung in nahezu jeder Tabellenzeile die Aussagekraft der Matrix vermindern würde.

Insbesondere gilt:

- RANF #01 ist eine globale Migrationsrandbedingung für alle persistenten fachlichen Daten.
- NFANF #04 gilt für sämtliche Spiel- und Verwaltungsfunktionen. US #05 stellt den Authentifizierungseinstieg bereit.
- NFANF #02 schützt bestehende Spiel- und Protokolldaten vor unbeabsichtigten rückwirkenden Änderungen. Die vollständige Kurslöschung gemäß GR #10, das fachlich definierte Undo gemäß US #20 sowie die Löschung eines zuvor abgebrochenen Spiels gemäß US #26 und GR #11 sind ausdrücklich davon abgegrenzt.
- US #26 wird durch die Use Cases „Spiel abbrechen“ und „Spiel löschen“ konkretisiert.

## 2. Traceability Matrix: User Stories → Anforderungen

| **US** | User Story | Geschäfts-/Spielregeln | Nichtfunktionale Anforderungen | Erläuterung |
|---|---|---|---|---|
| **US #01** | Startspieler ändern | GR #04, GR #05 | NFANF #01 | Der tatsächlich eingesetzte Startspieler unterliegt anschließend dem strikten Teamwechsel und der Sperre für erneute reguläre Einsätze. Die Nutzung des Namens zur Startspielerauswahl ist nach NFANF #01 zulässig. |
| **US #02** | Spielerwahlmodus festlegen | GR #04, GR #05, GR #08 | NFANF #01 | GR #08 regelt Zeitpunkt, Standardwert und Unveränderlichkeit des Modus. Teamwechsel und reguläre Einsatzsperre gelten unabhängig vom Auswahlmodus. |
| **US #03** | Nachzügler aufnehmen | GR #05, GR #06 | NFANF #01, NFANF #02 | Nachzügler werden in den weiteren Personenbestand aufgenommen. Bereits abgeschlossene Spielzüge dürfen dadurch nicht rückwirkend verändert werden. |
| **US #04** | Zentrale Instructor Settings | GR #08 | – | Der Spielerwahlmodus ist eine spielrelevante Einstellung. Zugriffsschutz ergibt sich querschnittlich aus NFANF #04. |
| **US #05** | Am System anmelden | – | NFANF #04 | Die Anmeldung ist der unmittelbare Mechanismus zur Durchsetzung des Zugriffsschutzes. |
| **US #06** | Eigenen Account verwalten | – | – | Zugriffsschutz ergibt sich querschnittlich aus NFANF #04. |
| **US #07** | Kurse verwalten | GR #10 | NFANF #02 | GR #10 definiert die vollständige Löschung aller kursbezogenen Daten. NFANF #02 grenzt diese bewusste Löschoperation von unzulässigen rückwirkenden Stammdatenänderungen ab. |
| **US #08** | Studierende verwalten | – | NFANF #01, NFANF #02 | Studierendennamen dürfen nur organisatorisch genutzt werden. Änderungen am Studierendenbestand dürfen historische Spieldaten nicht rückwirkend verändern. |
| **US #09** | Studierende importieren | – | NFANF #01, NFANF #02 | Der Import erzeugt organisatorische Personendaten, aber keine individuellen Leistungsdaten. Ein Import darf historische Spieldaten nicht rückwirkend verändern. |
| **US #10** | Studierende Teams zuordnen | – | NFANF #01, NFANF #02 | Teamzuordnung ist ein ausdrücklich zulässiger organisatorischer Zweck. Spätere Teamänderungen dürfen historische Spieldaten nicht rückwirkend verändern. |
| **US #11** | Anwesenheit festlegen | GR #05, GR #06 | NFANF #01 | Anwesenheit bestimmt den zulässigen Personenbestand. Für reguläre Einsätze gilt GR #05; beim Team Assist gilt die Ausnahme nach GR #06. |
| **US #12** | Lerneinheiten verwalten | – | NFANF #02 | Änderungen an fachlichen Stammdaten dürfen bereits dokumentierte Spielverläufe nicht rückwirkend verändern. |
| **US #13** | Fragenpool verwalten | GR #02 | NFANF #02 | Änderungen im globalen Fragenpool dürfen bereits gestartete oder gespielte Runden nicht rückwirkend verändern. |
| **US #14** | Lerninhalte importieren und exportieren | – | NFANF #02 | Importierte Änderungen an Lerninhalten dürfen historische Spiel- und Protokolldaten nicht rückwirkend verändern. |
| **US #15** | Runden konfigurieren | GR #01, GR #02, GR #03 | – | Die Rundenkonfiguration verwendet acht Fachfragen, kursübergreifend denselben Fragensatz und wird nach dem ersten erfolgreichen Start unveränderlich. |
| **US #16** | Spiel starten | GR #01, GR #02, GR #03, GR #08, GR #09 | NFANF #01 | Beim Start werden Fragensatz, Rundenstruktur, Spielerwahlmodus und Einmaligkeit der Runde je Kurs wirksam. Personenbezogene Daten dürfen nur organisatorisch verarbeitet werden. |
| **US #17** | Fachfragen durchführen und werten | GR #03, GR #04, GR #05, GR #07 | NFANF #01, NFANF #03 | Kern des regulären Spielablaufs: Kartenstruktur, Teamwechsel, einmaliger regulärer Einsatz und Sonderbehandlung der letzten Karte. Punkte bleiben teambezogen. |
| **US #18** | Team Assist einsetzen | GR #05, GR #06 | NFANF #01 | Einsätze über den Team Assist unterliegen der Ausnahme von der regulären Einsatzsperre und erzeugen ihrerseits keine Sperre für einen späteren regulären Spielerzug. |
| **US #19** | Challenge Card werten | GR #03, GR #07 | NFANF #01 | Die Challenge Card ist die neunte Karte und wird nach ihrer speziellen Wertungslogik gewertet, sofern sie nicht die letzte verbleibende Karte ist. Als letzte Karte wird sie gemäß GR #07 durch den Instructor beantwortet und nicht gewertet. |
| **US #20** | Spielschritt rückgängig machen | GR #04, GR #05, GR #06 | – | Undo muss den vorherigen fachlich konsistenten Spielzustand wiederherstellen. NFANF #02 stellt ausdrücklich klar, dass diese definierte Spieloperation keine unzulässige rückwirkende Änderung ist. |
| **US #21** | Laufendes Spiel fortsetzen | GR #04, GR #05, GR #06, GR #07, GR #08, GR #09, GR #11 | NFANF #02 | Nur laufende Spiele können fortgesetzt werden. Ein gemäß GR #11 abgebrochenes Spiel kann nicht fortgesetzt werden. |
| **US #22** | Beamer-Modus verwenden | – | NFANF #03 | Der Beamer-Modus unterstützt unmittelbar die kompakte und gut lesbare Spielansicht. |
| **US #23** | Ergebnisse überblicken | GR #09, GR #11 | NFANF #01, NFANF #02 | Das Dashboard darf ausschließlich Team- und Kursauswertungen zeigen und muss auf konsistenten historischen Spieldaten beruhen. Abgebrochene Spiele gelten gemäß GR #11 nicht als regulär abgeschlossen und dürfen daher nicht als reguläre Ergebnisse behandelt werden. |
| **US #24** | Gespielte Fragen protokollieren | GR #01, GR #02, GR #09, GR #11 | NFANF #02 | Das Protokoll muss den tatsächlich gespielten Fragensatz je Runde und Kurs nachvollziehbar halten. Wird ein abgebrochenes Spiel gemäß GR #11 gelöscht, werden auch seine ausschließlich spielbezogenen Daten entfernt. |
| **US #25** | Rundenabdeckung prüfen | GR #09, GR #11 | NFANF #02 | Die Rundenabdeckung unterscheidet offene, laufende, abgebrochene und regulär gespielte Runden. Erst nach Löschung eines abgebrochenen Spiels gilt die Runde für den betreffenden Kurs wieder als offen. |
| **US #26** | Spiel abbrechen und löschen | GR #09, GR #11 | NFANF #02 | US #26 wird durch die Use Cases „Spiel abbrechen“ und „Spiel löschen“ konkretisiert. Der Abbruch beendet das laufende Spiel ohne regulären Abschluss; die anschließende Löschung macht die Runde für den betreffenden Kurs wieder offen. |

## 3. Querschnittsanforderungen

### 3.1 RANF #01 – Erhalt des Datenbestands

RANF #01 gilt bei Aktualisierungen von Syzeteo für sämtliche persistenten fachlichen Daten. Dazu gehören insbesondere:

- Kurse,
- Studierende,
- Teamzuordnungen,
- Lerneinheiten,
- Fragen,
- Runden,
- laufende, abgebrochene und abgeschlossene Spiele,
- Spielstände,
- Ergebnisdaten,
- Fragenprotokolle.

Die ausdrücklich ausgelöste Kurslöschung gemäß GR #10 und die Löschung eines zuvor abgebrochenen Spiels gemäß GR #11 sind keine Systemaktualisierung und stellen daher keinen Widerspruch zu RANF #01 dar.

### 3.2 NFANF #04 – Zugriffsschutz

NFANF #04 gilt querschnittlich:

- US #05 stellt den Authentifizierungsmechanismus bereit.
- US #01 bis US #04 und US #06 bis US #26 beschreiben Spiel- oder Verwaltungsfunktionen und dürfen nur nach erfolgreicher Authentifizierung zugänglich sein.

## 4. Rückwärts-Traceability: Anforderungen → User Stories

### 4.1 Geschäfts- und Spielregeln

| **Anforderung** | Abgedeckt durch User Stories |
|---|---|
| **GR #01 – Einheitlicher Fragensatz** | US #15, US #16, US #24 |
| **GR #02 – Fragensatz unveränderlich** | US #13, US #15, US #16, US #24 |
| **GR #03 – Rundenumfang festgelegt** | US #15, US #16, US #17, US #19 |
| **GR #04 – Strikter Teamwechsel** | US #01, US #02, US #17, US #20, US #21 |
| **GR #05 – Einmaliger regulärer Einsatz** | US #01, US #02, US #03, US #11, US #17, US #18, US #20, US #21 |
| **GR #06 – Team-Assist-Ausnahme** | US #03, US #11, US #18, US #20, US #21 |
| **GR #07 – Letzte Karte durch Instructor** | US #17, US #19, US #21 |
| **GR #08 – Spielerwahlmodus vor Spielbeginn** | US #02, US #04, US #16, US #21 |
| **GR #09 – Runde je Kurs einmal verwenden** | US #16, US #21, US #23, US #24, US #25, US #26 |
| **GR #10 – Vollständige Kurslöschung** | US #07 |
| **GR #11 – Spiel abbrechen und löschen** | US #21, US #23, US #24, US #25, US #26 |

### 4.2 Nichtfunktionale Anforderungen

| **Anforderung** | Abgedeckt durch User Stories |
|---|---|
| **NFANF #01 – Keine Individualauswertung** | US #01, US #02, US #03, US #08, US #09, US #10, US #11, US #16, US #17, US #18, US #19, US #23 |
| **NFANF #02 – Rundenbezogene Datenintegrität** | US #03, US #07, US #08, US #09, US #10, US #12, US #13, US #14, US #21, US #23, US #24, US #25, US #26 |
| **NFANF #03 – Kompakte Spielansicht** | US #17, US #22 |
| **NFANF #04 – Zugriffsschutz** | US #05 als Authentifizierungsmechanismus; US #01–US #04 und US #06–US #26 als geschützte Spiel- und Verwaltungsfunktionen |

### 4.3 Randanforderung

| **Anforderung** | Geltungsbereich |
|---|---|
| **RANF #01 – Erhalt des Datenbestands** | Globale Migrationsrandbedingung für alle bei einer Systemaktualisierung vorhandenen persistenten fachlichen Daten |

## 5. Vollständigkeits- und Konsistenzprüfung

Die konsolidierte Anforderungsbasis enthält:

- 26 User Stories
- 11 Geschäfts- und Spielregeln
- 4 nichtfunktionale Anforderungen
- 1 Randanforderung
- 2 Use Cases zur Konkretisierung von US #26

Alle 26 User Stories sind in der Matrix enthalten.

Alle 11 Geschäfts- und Spielregeln besitzen mindestens einen nachvollziehbaren Trace-Link.

Alle 4 nichtfunktionalen Anforderungen sind berücksichtigt.

RANF #01 ist als globale Querschnittsanforderung berücksichtigt.

Die Präzisierungen sind wie folgt konsolidiert:

1. Kurslöschung: vollständige Löschung aller kursbezogenen Daten gemäß US #07 und GR #10; globale Lerninhalte bleiben erhalten.
2. Änderungen an Fragen: bereits gestartete oder gespielte Runden bleiben einschließlich Frage- und Musterantworttext unverändert gemäß GR #02.
3. Undo: ausdrücklich zulässige Spieloperation gemäß US #20 und NFANF #02.
4. Team Assist: Ein ausschließlicher Einsatz über den Team Assist sperrt nicht für einen späteren regulären Spielerzug gemäß GR #05 und GR #06.
5. Letzte Karte: Die letzte verbleibende Karte wird unabhängig von ihrem Kartentyp durch den Instructor beantwortet und nicht gewertet; es werden keine Punkte vergeben gemäß GR #07.
6. Spielabbruch und Löschung: Ein laufendes Spiel kann gemäß US #26 und GR #11 abgebrochen werden. Das abgebrochene Spiel kann nicht fortgesetzt werden, wird auf der Instructor-Seite zur Löschung angeboten und macht die Runde erst nach der Löschung wieder offen. Regulär abgeschlossene Spiele können über diese Funktion nicht gelöscht werden.

Ergebnis: Bezogen auf die konsolidierten Dokumente bestehen keine erkennbaren fachlichen Widersprüche oder verwaisten Anforderungen.
