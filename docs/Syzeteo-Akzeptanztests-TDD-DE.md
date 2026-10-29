# Syzeteo – TDD-Akzeptanztestkatalog (Arbeitsstand 29.10.2026)

## Geltung und Methodik

Diese Spezifikation dient der schrittweisen Synchronisation von User Stories und Regressionstests. **Die Mappings dokumentieren fachlich begründete Teilnachweise (Review-Status `verified_partial`), keine vollständige Abnahme der User Stories.** Die fachliche Referenz bilden `Syzeteo-L-US-DE.md`, `Syzeteo-RANF-etc-DE.md` und `Syzeteo-Traceability-Matrix-DE.md`.

Alle 29 User Stories besitzen jetzt mindestens ein konkretisiertes, maschinenlesbares und durch eine direkte Testmethode referenziertes Kriterium. Zusätzliche fachliche Randfälle können weitere Szenarien und Tests erfordern; die Vervollständigung der ursprünglichen generischen Kriterien ist keine vollständige Story-Abnahme.

## TDD-Regel (beschlossen)

1. Vorhandene Testlücken werden sichtbar berichtet und blockieren die Pipeline zunächst nicht.
2. Neue oder geänderte User Stories benötigen mindestens einen neuen, ausführbaren und in der Manifestdatei referenzierten automatisierten Akzeptanztest, bevor die Änderung freigegeben wird.
3. Für neue oder textlich geänderte Akzeptanzkriterien erzwingt `acceptance_criteria_check.py` eine zusätzliche ausführbare Testreferenz. Diese technische Zuordnung beweist noch keine semantische Testgüte; Assertion-Review bleibt erforderlich. Die Kriterien-Baseline wird im normalen Feature-PR nicht geändert.
4. Visuelle Kriterien werden hybrid geprüft: technische Tests plus dokumentierte manuelle Abnahme. Die Referenz ist **1920 × 1080 Pixel bei 100 % Browser-Zoom**, jeweils normale Spielansicht und Beamer-Modus.
5. Baseline-Änderungen werden nicht automatisch vorgenommen und gehören in ein gesondert überprüftes Review.

**Abschlussstand der initialen Kriterienkonkretisierung:** 29 User Stories, 109 Story-Test-Zuordnungen (103 verschiedene referenzierte Testmethoden), kein ungemappter Story-Eintrag. Alle 46 registrierten Kriterien sind `specified_partial`, keines bleibt `legacy_provisional`. Die Teilnachweis-Kennzeichnung ist kein Beweis vollständiger fachlicher Abdeckung. Autoritativer Detailbericht: `Syzeteo-Testabdeckung-Review-DE.md`.

## Übersicht der Akzeptanzkriterien und Teilnachweise

### US #01 – Startspieler ändern

**Fachliche Anforderung:** Als **Instructor** möchte ich den automatisch zufällig bestimmten Startspieler vor der ersten Frage durch eine andere anwesende Person ersetzen können, damit ich den tatsächlichen Startspieler bei Bedarf an die konkrete Spielsituation anpassen kann.

**AC-US01-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben sind vor Spielbeginn anwesende Studierende beider Teams; wenn der Instructor einen bestimmten anwesenden Startspieler festlegt und das Spiel startet, dann ist diese Person der einzige regulär als eingesetzt markierte Startspieler und ihr Team beginnt; nach Spielstart ist ein erneuter Startspielerwechsel gesperrt.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us01_manual_starter_selection_replaces_random_choice_before_first_card (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #02 – Spielerwahlmodus festlegen

**Fachliche Anforderung:** Als **Instructor** möchte ich vor Beginn eines Spiels in den **Instructor Settings** festlegen können, ob die reguläre Auswahl der Spieler ab Spieler 2 zufällig oder manuell erfolgt, damit ich die Spielerbestimmung an die jeweilige Unterrichts- und Spielsituation anpassen kann.

**AC-US02-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein noch nicht gestartetes Spiel; wenn der Instructor den regulären Spielerwahlmodus 'manuell' festlegt und das Spiel startet, dann bleibt dieser Modus während des laufenden Spiels gespeichert und die nächste Spielerwahl erfolgt nicht automatisch beim Werten der ersten Fachfrage.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us02_selection_mode_is_frozen_in_running_game (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #03 – Nachzügler aufnehmen

**Fachliche Anforderung:** Als **Instructor** möchte ich während eines laufenden Spiels verspätet eingetroffene Studierende nachträglich in die Runde aufnehmen können, damit diese trotz ihrer Abwesenheit zu Spielbeginn noch am weiteren Spiel teilnehmen können.

**AC-US03-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein laufendes Spiel mit einem zum Spielstart abwesenden aktiven Studierenden; wenn der Instructor diesen als Nachzügler aufnimmt, dann wird er in den Spielerkader aufgenommen, während eine doppelte Aufnahme abgewiesen wird.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us03_late_arrival_is_added_only_to_running_roster (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #04 – Zentrale Instructor Settings

**Fachliche Anforderung:** Als **Instructor** möchte ich systemweite und spielelevante Einstellungen und Statusinformationen auf einer zentralen Seite **„Instructor Settings“** einsehen und, soweit sinnvoll, direkt verwalten können, damit ich jederzeit einen vollständigen Überblick über die aktuelle Konfiguration habe und notwendige Änderungen gezielt vornehmen kann.

**AC-US04-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Kurs ohne Studierende; wenn die Instructor-Settings-Konfigurationsprüfung ausgeführt wird, dann meldet sie den leeren Kurs als sprachneutral beschriebenes Warnproblem mit einer Aktion zur Studierendenverwaltung.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us04_instructor_settings_reports_empty_course_with_action (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Instruktor-Einstellungen prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #05 – Am System anmelden

**Fachliche Anforderung:** Als **Instructor** möchte ich mich an Syzeteo anmelden können, damit ich auf die für mich vorgesehenen Spiel- und Verwaltungsfunktionen zugreifen kann.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US05-01:** Gegeben ist ein eingerichtetes Instructor-Konto mit gültigem Passwort; wenn sich der Instructor mit dem richtigen Benutzernamen unabhängig von dessen Groß-/Kleinschreibung und dem Passwort anmeldet, dann wird die Anmeldung akzeptiert und das Konto korrekt erkannt.
- **AC-US05-02:** Gegeben ist ein eingerichtetes Instructor-Konto; wenn ein falsches Passwort zur Anmeldung verwendet wird, dann wird der Zugriff verweigert.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** 2 referenzierte Testmethoden, darunter neue Assertions in `test_tdd_admin_acceptance.py`. Vollständige Methodenzuordnung: `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 2 konkretisierte Kriterien mit 2 direkten Story-Test-Zuordnungen; Teilabdeckung, keine vollständige Story-Abnahme.

### US #06 – Eigenen Account verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich meinen Benutzernamen und mein Passwort ändern können, damit ich meine Zugangsdaten selbst verwalten kann.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US06-01:** Gegeben ist ein authentifiziertes Instructor-Konto; wenn Benutzername und Passwort unter Angabe der bisherigen gültigen Zugangsdaten geändert werden, dann funktioniert die Anmeldung mit den neuen Daten und die früheren Zugangsdaten sind ungültig.
- **AC-US06-02:** Gegeben ist ein Instructor-Konto mit gültigem Passwort; wenn bei der Passwortänderung ein falsches bisheriges Passwort angegeben wird, dann wird die Änderung abgewiesen und das bisherige Passwort bleibt gültig.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** 3 referenzierte Testmethoden, darunter neue Assertions in `test_tdd_admin_acceptance.py`. Vollständige Methodenzuordnung: `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 2 konkretisierte Kriterien mit 3 direkten Story-Test-Zuordnungen; Teilabdeckung, keine vollständige Story-Abnahme.

### US #07 – Kurse verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Kurse anlegen, archivieren, reaktivieren und bei Bedarf vollständig löschen können, damit ich die in Syzeteo verwendeten Lehrveranstaltungen aktuell halten kann. Bei der Löschung eines Kurses werden sämtliche mit diesem Kurs zusammenhängenden Daten gelöscht.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US07-01:** Gegeben ist ein Kurs mit Studierenden, Spielkarten, Spiel und kursbezogener Historie sowie ein weiterer Kurs und ein globaler Fragenpool; wenn der Instructor den Kurs vollständig löscht, dann werden ausschließlich dessen Kurs-, Studierenden-, Spiel- und Historiendaten gelöscht, während der andere Kurs, seine Studierenden sowie globale Fragen und Runden erhalten bleiben (GR #10).
- **AC-US07-02:** Gegeben ist ein Kurs mit Studierenden ohne laufendes Spiel; wenn der Instructor ihn archiviert und anschließend reaktiviert, dann wechselt der Sichtbarkeitsstatus, ohne dass die gespeicherten Studierenden verloren gehen.
- **AC-US07-03:** Gegeben ist ein Kurs mit laufendem Spiel; wenn der Instructor versucht, ihn zu archivieren, dann wird die Archivierung fachlich zurückgewiesen und der Kurs bleibt aktiv.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** 4 referenzierte Testmethoden, darunter neue Assertions in `test_tdd_admin_acceptance.py`. Vollständige Methodenzuordnung: `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 3 konkretisierte Kriterien mit 4 direkten Story-Test-Zuordnungen; Teilabdeckung, keine vollständige Story-Abnahme.

### US #08 – Studierende verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierende eines Kurses anlegen, bearbeiten sowie aktiv oder inaktiv setzen können, damit der für den Spielbetrieb relevante Teilnehmerbestand aktuell gehalten werden kann.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US08-01:** Gegeben sind Studierende in mehreren Kursen; wenn der Instructor einen Studierenden umbenennt, dessen Team ändert und ihn deaktiviert, dann werden nur dessen Stammdaten geändert und ausschließlich aktive Studierende erscheinen in der aktiven Kursliste.
- **AC-US08-02:** Gegeben ist ein Kurs mit bereits vorhandenem Studierendennamen; wenn derselbe Name erneut angelegt oder ein anderer Studierender darauf umbenannt werden soll, dann wird die doppelte Verwendung im Kurs abgewiesen, während gleichlautende Namen in verschiedenen Kursen zulässig bleiben.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** 5 referenzierte Testmethoden, darunter neue Assertions in `test_tdd_admin_acceptance.py`. Vollständige Methodenzuordnung: `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 2 konkretisierte Kriterien mit 5 direkten Story-Test-Zuordnungen; Teilabdeckung, keine vollständige Story-Abnahme.

### US #09 – Studierende importieren

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierendenlisten aus einer CSV-Datei in einen Kurs importieren können, damit ich größere Teilnehmergruppen nicht einzeln erfassen muss.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US09-01:** Gegeben ist eine UTF-8-CSV-Datei mit BOM, Semikolon-Trennung und Vorname-/Nachname-Spalten, in der ein Name bereits im Zielkurs existiert; wenn der Instructor sie importiert, dann werden neue Studierende angelegt, doppelte Einträge übersprungen und die Import-/Überspringungszahlen zurückgegeben.
- **AC-US09-02:** Gegeben ist eine CSV-Datei ohne unterstützte Namensspalten; wenn der Instructor sie importiert, dann wird der Import mit einem fachlichen Fehler abgewiesen und im Kurs kein Studierender angelegt.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** 3 referenzierte Testmethoden, darunter neue Assertions in `test_tdd_admin_acceptance.py`. Vollständige Methodenzuordnung: `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 2 konkretisierte Kriterien mit 3 direkten Story-Test-Zuordnungen; Teilabdeckung, keine vollständige Story-Abnahme.

### US #10 – Studierende Teams zuordnen

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierende manuell oder zufällig Team 1 oder Team 2 zuordnen können, damit für jeden Kurs eine geeignete Teamstruktur für den Spielbetrieb besteht.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US10-01:** Gegeben sind aktive Studierende eines Kurses mit Teamzuordnungen; wenn der Instructor eine Person manuell Team 1 oder 2 zuweist, dann wird nur deren aktuelle Teamzuordnung geändert und die Zuordnungen anderer Studierender bleiben unverändert.
- **AC-US10-02:** Gegeben sind sieben aktive Studierende eines Kurses; wenn der Instructor die zufällige Teamzuordnung ausführt, dann sind alle sieben einem der zwei Teams zugeordnet und deren Größen unterscheiden sich um höchstens eins.
- **AC-US10-03:** Gegeben sind aktive und inaktive Studierende sowie ein weiterer Kurs; wenn für einen Kurs Teams zufällig zugeordnet werden, dann werden nur die aktiven Studierenden dieses Kurses neu verteilt; inaktive Studierende und andere Kurse bleiben unverändert.
- **AC-US10-04:** Gegeben sind weniger als zwei aktive Studierende oder eine ungültige manuelle Teamkennung; wenn die jeweilige Teamzuordnung ausgelöst wird, dann wird sie mit fachlichem Fehler abgewiesen und der vorhandene Zuordnungsstand nicht verändert.
- **AC-US10-05:** Gegeben ist ein laufendes Spiel mit gespeichertem Spielerkader und Team-Snapshots; wenn danach eine Studierenden-Teamzuordnung im Kurs geändert wird, dann bleiben die im gestarteten Spiel gespeicherten Teamzuordnungen und die aktuelle Spielerwahl unverändert (NFANF #02).

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** `test_us10_team_assignment.py` (sechs Tests). Die Einzelreferenzen stehen in `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 5 konkrete Kriterien mit 6 direkten Testmethoden im Story-Mapping; weiterhin keine vollständige Story-Abnahme.

### US #11 – Anwesenheit festlegen

**Fachliche Anforderung:** Als **Instructor** möchte ich vor Spielbeginn festlegen können, welche Studierenden der beiden Teams anwesend sind, damit während des Spiels nur tatsächlich anwesende Personen für die vorgesehenen Spielerrollen berücksichtigt werden.

**AC-US11-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben sind mehr als acht aktive Studierende aus zwei Teams, von denen genau vier je Team anwesend ausgewählt wurden; wenn ein Spiel gestartet wird, dann umfasst sein gespeicherter Kader ausschließlich diese acht anwesenden Personen, mit unveränderten Teamzuordnungen.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us11_only_present_students_enter_initial_game_roster (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Anwesenheitsansicht bedienen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #12 – Lerneinheiten verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Lerneinheiten anlegen, bearbeiten und sortieren können, damit der Fragenpool fachlich strukturiert verwaltet werden kann.

**AC-US12-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine bereits angelegte Lerneinheit; wenn der Instructor Code, Titel und Position bearbeitet, dann werden alle drei geänderten Werte gespeichert und in der Lerneinheitenliste angezeigt.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us12_learning_unit_can_be_renamed_and_reordered (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #13 – Fragenpool verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Fragen mit Musterantworten im globalen, kursübergreifenden Fragenpool anlegen, bearbeiten, Lerneinheiten zuordnen und archivieren können, damit die für Syzeteo verfügbaren Fachfragen zentral gepflegt werden können.

**AC-US13-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine Frage mit Musterantwort im globalen Fragenpool; wenn der Instructor Text und Musterantwort ändert und die Frage archiviert, dann bleiben der geänderte Datensatz erhalten und die Frage wird aus der Liste aktiver Fragen ausgeschlossen.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us13_question_edit_and_archive_preserve_global_pool_entry (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #14 – Lerninhalte importieren und exportieren

**Fachliche Anforderung:** Als **Instructor** möchte ich Lerneinheiten und Fragen exportieren und in Syzeteo importieren können, damit der fachliche Datenbestand gesichert und zwischen Installationen übertragen werden kann.

**AC-US14-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Fragenpool mit acht Fachfragen in einer Lerneinheit; wenn die Lerninhalte als JSON exportiert und in eine neue leere Installation importiert werden, dann entstehen dort dieselbe Lerneinheit und acht Fachfragen einschließlich ihrer Musterantworten.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us14_question_pool_export_import_preserves_unit_and_question (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #15 – Runden konfigurieren

**Fachliche Anforderung:** Als **Instructor** möchte ich eine Runde aus Fachfragen des globalen Fragenpools konfigurieren können, damit für die Durchführung einer Runde ein definierter Fragensatz bereitsteht.

**AC-US15-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben sind acht voneinander verschiedene vorhandene Fachfragen; wenn der Instructor daraus eine Runde anlegt, dann enthält diese genau acht Fragen in definierter Positionsreihenfolge; ein Versuch mit sieben Fragen wird abgewiesen.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us15_round_has_exactly_eight_distinct_questions_in_order (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #16 – Spiel starten

**Fachliche Anforderung:** Als **Instructor** möchte ich für einen ausgewählten Kurs eine konfigurierte Runde mit den anwesenden Studierenden starten können, damit die Runde durchgeführt werden kann.

**AC-US16-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine konfigurierte Runde mit acht Fachfragen und acht anwesenden Studierenden aus zwei Teams; wenn das Spiel gestartet wird, dann werden acht Fachfragekarten und eine Challenge Card angelegt, das Spiel ist laufend und dieselbe Runde kann in diesem Kurs nicht erneut gestartet werden.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us16_start_creates_nine_cards_and_disallows_second_start_for_same_course (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #17 – Fachfragen durchführen und werten

**Fachliche Anforderung:** Als **Instructor** möchte ich während eines Spiels Karten aufdecken, die zugehörige Fachfrage und Musterantwort anzeigen sowie die Antwort werten können, damit der Spielverlauf und die Teampunkte regelkonform fortgeschrieben werden.

**AC-US17-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein laufendes Spiel mit aktuellem Team; wenn der Instructor eine Fachfrage aufdeckt und diese mit einem Punkt wertet, dann ist die Karte abgeschlossen, genau ein Punkt wird dem aktuellen Team gutgeschrieben und der Punktestand des anderen Teams bleibt unverändert.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us17_scoring_question_updates_only_current_team_points (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Kartenansicht und Wertungsanzeige prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #18 – Team Assist einsetzen

**Fachliche Anforderung:** Als **Instructor** möchte ich für das aktive Team den **Team Assist** einsetzen und eine anwesende Person dieses Teams zur Beantwortung der aktuellen Fachfrage auswählen können, damit der vorgesehene Team Assist im Spiel genutzt werden kann.

**AC-US18-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein laufendes Spiel mit einer aufgedeckten Fachfrage; wenn der Instructor für das aktive Team einen anwesenden Teamkollegen über Team Assist auswählt und die Fachfrage wertet, dann wird der Assist als verbraucht markiert und keine individuelle Leistungszuordnung gespeichert.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us18_team_assist_is_consumed_once_and_does_not_store_person_performance (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #19 – Challenge Card werten

**Fachliche Anforderung:** Als **Instructor** möchte ich die **Challenge Card** entsprechend dem Ergebnis der Challenge-Frage werten können, damit die daraus resultierenden Teampunkte korrekt vergeben werden.

**AC-US19-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein laufendes Spiel mit verfügbarer Challenge Card; wenn diese aufgedeckt und für das aktive Team mit zwei Punkten gewertet wird, dann erhöht sich der Punktestand dieses Teams um zwei Punkte.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us19_challenge_card_can_award_two_points_to_active_team (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #20 – Spielschritt rückgängig machen

**Fachliche Anforderung:** Als **Instructor** möchte ich den zuletzt ausgeführten Spielschritt rückgängig machen können, damit eine versehentliche Wertung oder Spielerwahl korrigiert werden kann, ohne das gesamte Spiel neu starten zu müssen.

**AC-US20-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine aufgedeckte, anschließend mit einem Punkt gewertete Fachfrage; wenn der Instructor die letzte Wertung rückgängig macht, dann wird der vorherige Teampunktestand wiederhergestellt und die Karte bleibt aufgedeckt, aber noch nicht abgeschlossen.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us20_undo_restores_points_and_unresolved_card (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #21 – Laufendes Spiel fortsetzen

**Fachliche Anforderung:** Als **Instructor** möchte ich ein laufendes Spiel später wieder öffnen und am gespeicherten Spielstand fortsetzen können, damit ein Spiel bei Unterbrechungen nicht verloren geht.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US21-01:** Gegeben ist ein laufendes Spiel mit zwei abgeschlossenen und gewerteten regulären Spielzügen; wenn die persistierte Sitzung neu geöffnet wird, dann bleiben Punkte, aktueller Spieler, Zugnummer, Karten und Spielerkader erhalten und ein weiterer Spielzug lässt sich abschließen.
- **AC-US21-02:** Gegeben ist ein laufendes Spiel; wenn die Datenbankverbindung neu geöffnet wird, dann bleibt es mit Status running auffindbar und sein gespeicherter Anfangszustand mit Kader und Karten ist unverändert.
- **AC-US21-03:** Gegeben ist ein abgebrochenes Spiel; wenn die Datenbankverbindung neu geöffnet wird, dann wird das Spiel nicht als laufendes Spiel zur Fortsetzung angeboten (GR #11).

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** `test_us21_resume.py` (fünf Tests). Die Einzelreferenzen stehen in `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** 3 konkrete Kriterien mit 5 direkten Testmethoden im Story-Mapping; weiterhin keine vollständige Story-Abnahme.

### US #22 – Beamer-Modus verwenden

**Fachliche Anforderung:** Als **Instructor** möchte ich die Spielansicht in einen Beamer-Modus umschalten können, damit Karten, Fragen und Spielstand für die Studierenden groß und ohne störende Navigation dargestellt werden.

**AC-US22-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Fragetext mit HTML-Sonderzeichen und Zeilenumbruch für die Spiel-/Beameranzeige; wenn er über die sichere Textdarstellung ausgegeben wird, dann erscheint HTML-Markup als sichtbarer Text und wird nicht als ausführbarer HTML-Code übernommen.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us22_question_text_escapes_html_in_projection_rendering (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Normalansicht und Beamer-Modus bei 1920×1080, 100 % Zoom abnehmen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #23 – Ergebnisse überblicken

**Fachliche Anforderung:** Als **Instructor** möchte ich nach dem Login Teamstände, Rundenergebnisse, kumulierte Ergebnisse und die Spielhistorie eines Kurses im Ergebnis-Dashboard sehen können, damit ich den bisherigen Spielverlauf und den Gesamtstand jederzeit überblicken kann.

**AC-US23-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Kurs mit regulär abgeschlossenem Spiel und ein anderer ohne Abschluss; wenn der Instructor den Ergebnisstand aufruft, dann enthält das Dashboard ausschließlich die abgeschlossenen Teampunkte im jeweiligen Kurs und die abgeschlossene Runde ist in dessen Spielhistorie enthalten.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us23_finished_results_are_included_but_running_games_not_scored (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Ergebnis-Dashboard visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #24 – Gespielte Fragen protokollieren

**Fachliche Anforderung:** Als **Instructor** möchte ich nachvollziehen können, welche Fachfragen in welcher Runde und in welchem Kurs tatsächlich gespielt wurden, und dieses Protokoll exportieren können, damit die Verwendung der Fragen für die weitere Lehr- und Klausurplanung dokumentiert ist.

**Konkretisierte maschinenlesbare Kriterien (Status `specified_partial`):**

- **AC-US24-01:** Gegeben sind richtig und falsch beantwortete, abschließend behandelte Fachfragen sowie eine nur aufgedeckte Fachfrage; wenn das Fragenprotokoll angezeigt wird, dann werden beide abgeschlossenen Fachfragen unabhängig von der Wertung protokolliert, die bloß aufgedeckte dagegen nicht.
- **AC-US24-02:** Gegeben sind abgeschlossene Fachfragen in verschiedenen Kursen und Runden; wenn das Protokoll gelesen wird, dann enthält jede Fachfrage ihre Kurs-, Runden- und Kartenpositionszuordnung.
- **AC-US24-03:** Gegeben ist eine bereits gespielte Frage, deren Wortlaut im globalen Fragenpool später geändert wurde; wenn das Protokoll gelesen wird, dann erscheint weiterhin der gespeicherte historische Fragetext und Lerneinheitencode.
- **AC-US24-04:** Gegeben ist ein abgebrochenes Spiel mit abschließend behandelten Fachfragen; wenn das Protokoll gelesen wird, dann werden diese samt Abbruchstatus und Zeitstempel angezeigt; nach ausdrücklicher Löschung des Spiels sind dessen Protokolleinträge entfernt.
- **AC-US24-05:** Gegeben ist ein Fragenprotokoll über mehrere Kurse und Runden; wenn nach Kurs und Runde gefiltert und als CSV exportiert wird, dann enthält die CSV ausschließlich die gefilterte Ansicht, einschließlich Sonderzeichen, UTF-8-BOM und Spaltenköpfen auch bei leerer Treffermenge.
- **AC-US24-06:** Gegeben ist eine abschließend behandelte letzte Instructor-Fachfrage; wenn Protokoll und statistische Fragenauswertung gelesen werden, dann erscheint die Fachfrage nur im Protokoll, nicht aber als studentischer Versuch in der Fragenauswertung (GR #07 und #13).

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** `test_us24_question_protocol.py` (sieben Tests) und `test_us24_csv.py` (drei Tests). Die Einzelreferenzen stehen in `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Export- und Protokollansicht prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** 6 konkrete Kriterien mit 10 direkten Testmethoden im Story-Mapping; weiterhin keine vollständige Story-Abnahme.

**Beschlossene Sonderregel:** Die letzte Instructor-Fachfrage wird protokolliert, aber aus der statistischen Fragenauswertung ausgeschlossen. Nachweis: `test_us24_question_protocol.py::test_us24_final_instructor_question_is_logged_but_not_analyzed`.

### US #25 – Rundenabdeckung prüfen

**Fachliche Anforderung:** Als **Instructor** möchte ich sehen können, welche Runden in welchen aktiven Kursen bereits gespielt wurden, noch laufen, abgebrochen oder noch offen sind, damit ich die kursübergreifende Durchführung der vorgesehenen Runden überblicken kann.

**AC-US25-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine konfigurierte Runde für zwei aktive Kurse; wenn in einem Kurs ein Spiel läuft und im anderen noch kein Spiel existiert, dann zeigt die Rundenabdeckung 'running' bzw. 'open'; nach regulärem Abschluss wird der erste Eintrag zu 'played'.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us25_round_coverage_distinguishes_running_played_and_open_courses (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Rundenabdeckung visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #26 – Spiel abbrechen und löschen

**Fachliche Anforderung:** Als **Instructor** möchte ich ein laufendes Spiel abbrechen und ein abgebrochenes Spiel auf der **Instructor-Seite** löschen können, damit irrtümlich gestartete oder nicht fortzuführende Spiele den weiteren Spielbetrieb und die Rundenabdeckung nicht blockieren.

**AC-US26-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein laufendes Spiel; wenn der Instructor es abbricht und anschließend löscht, dann verschwinden dessen Spiel, Karten und zugehörige Daten; für denselben Kurs kann die betroffene Runde erneut gestartet werden.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us26_aborted_game_deletion_removes_cards_and_releases_round (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #27 – Teamnamen verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich für die beiden Teams eines Kurses frei wählbare Namen vergeben und diese später ändern können, damit die Teams im Spiel unter passenden Bezeichnungen angezeigt werden.

**AC-US27-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Kurs mit benannten Teams; wenn das Spiel gestartet wurde, dann enthalten die Spiel-Snapshots diese beiden Namen und eine nachträgliche Umbenennung während des laufenden Spiels wird abgewiesen, ohne die historischen Namen zu verändern.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us27_team_name_changes_preserve_running_game_snapshots (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Teamnamen im Spiel und Dashboard prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #28 – Fragen auswerten

**Fachliche Anforderung:** Als **Instructor** möchte ich die Ergebnisse gespielter Fachfragen für einen einzelnen Kurs sowie kursübergreifend auswerten können, damit ich erkenne, welche Fragen wie häufig und wie erfolgreich beantwortet wurden.

**AC-US28-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist eine gewertete Fachfrage aus einem noch laufenden Spiel; wenn die Fragenauswertung erfolgt, dann erscheint dieses Spiel nicht in der Statistik; personenbezogene Leistungsfelder werden nicht ausgegeben.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us28_analysis_excludes_unfinished_games_and_student_identity (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

### US #29 – Tic-Tac-Toe auf dem Board

**Fachliche Anforderung:** Als **Instructor** möchte ich, dass gewertete Karten auf dem Board einen Rand in der Farbe des punktenden Teams erhalten und eine vollständige Reihe markiert wird, damit nebenbei ein Tic-Tac-Toe als zusätzlicher spielerischer Anreiz mitläuft, ohne die Spielansicht zu vergrößern oder die reguläre Wertung zu verändern.

**AC-US29-01 (konkretisiertes Akzeptanzkriterium, Status `specified_partial`):** Gegeben ist ein Board, auf dem die drei Karten einer waagerechten Reihe Punkte für Team 1 tragen; wenn die Tic-Tac-Toe-Auswertung durchgeführt wird, dann erkennt sie diese Reihe und Team 1 als Gewinner der Markierung, ohne Punktewerte zu verändern.

**Fachlich zugeordnete Teilnachweise (Quellcode/Assertions geprüft, keine Vollabnahme):** test_tdd_phase2_remaining.py::test_us29_tic_tac_toe_recognizes_scored_team_row_without_changing_points (direkter neuer Assertions-Test); weitere frühere Teilnachweise siehe `Syzeteo-Akzeptanzkriterien.json`.

**Visueller Abnahmenachweis:** Boardmarkierung, Linie und Einblendung visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** mindestens ein konkretisiertes, direkt getestetes Kriterium; `specified_partial` bedeutet Teilnachweis, keine Vollabnahme der Story.

## Dokumentation manueller Prüfungen

Die folgenden **PASS**-Einträge sind Freigaben des Projektverantwortlichen im Chat vom 29.10.2026, keine unabhängigen Browsermessungen. Für US #10, #21 und #24 sind die entsprechenden Einzelvermerke zusätzlich in den fachlichen Detaildokumenten enthalten.

| Datum | US / AC | Browser / Version | Auflösung / Zoom | Schritte (vorgesehen; Einzelausführung nicht belegt) | Erwartetes Ergebnis | Tatsächliches Ergebnis | Bestanden? | Prüfer | Screenshot-/Ticketlink |
|---|---|---|---|---|---|---|---|---|---|
| 29.10.2026 (Freigabe) | US10 / AC-US10-01 | nicht angegeben | Referenz 1920×1080 / 100 %; tatsächliche Umgebung nicht dokumentiert | Manuelle und zufällige Teamzuordnung öffnen und verändern | Korrekte Zuordnung, Kursisolation und gültige Teamgrößen | UI-Freigabe des Projektverantwortlichen, keine Einzelbeobachtungen übermittelt | PASS (Nutzerfreigabe) | Projektverantwortlicher | nicht vorgelegt |
| 29.10.2026 (Freigabe) | US21 / AC-US21-01 | nicht angegeben | Referenz 1920×1080 / 100 %; tatsächliche Umgebung nicht dokumentiert | Laufendes Spiel nach Unterbrechung wieder öffnen | Gespeicherter Spielstand erhalten; abgebrochenes Spiel nicht fortsetzbar | UI-Freigabe des Projektverantwortlichen, keine Einzelbeobachtungen übermittelt | PASS (Nutzerfreigabe) | Projektverantwortlicher | nicht vorgelegt |
| 29.10.2026 (Freigabe) | US22 / AC-US22-01 | nicht angegeben | Referenz 1920×1080 / 100 %; tatsächliche Umgebung nicht dokumentiert | Normal- und Beameransicht öffnen, Navigation und Scrollen prüfen | Lesbare Darstellung ohne störende Navigation, gemäß NFANF #03 möglichst ohne vertikales Scrollen | UI-Freigabe des Projektverantwortlichen, keine Einzelbeobachtungen übermittelt | PASS (Nutzerfreigabe) | Projektverantwortlicher | nicht vorgelegt |
| 29.10.2026 (Freigabe) | US24 / AC-US24-01 | nicht angegeben | Referenz 1920×1080 / 100 %; tatsächliche Umgebung nicht dokumentiert | Fragenprotokoll anzeigen, Kurs-/Rundenfilter und CSV prüfen | Gefilterte Fragen und CSV entsprechen dem gewählten Kurs und der Runde | UI-Freigabe des Projektverantwortlichen, keine Einzelbeobachtungen übermittelt | PASS (Nutzerfreigabe) | Projektverantwortlicher | nicht vorgelegt |

**Grenze des Nachweises:** Browser-Version, verwendete Auflösung, Zoomstufe, einzelne Prüfschritte, Screenshots und Einzelbeobachtungen liegen nicht vor. Der Referenzwert 1920×1080/100 % ist **kein Beleg**, dass diese Testumgebung tatsächlich verwendet wurde. Weitere US sind durch diese Tabelle nicht automatisch freigegeben.

## Grenzen des aktuellen Bestands

- Die GitHub-CI führt Python-Regressionstests aus, jedoch keine automatisierten Browser-End-to-End-Tests.
- Eine Testmethodenzuordnung beweist weder vollständige Randfallabdeckung noch die semantische Angemessenheit ihrer Assertions.
- `traceability_check.py` prüft Änderungen an User Stories. `acceptance_criteria_check.py` prüft zusätzlich neue oder geänderte Akzeptanzkriterien gegen die eingefrorene Kriterien-Baseline; fachliche Aussagekraft bleibt Review-Aufgabe.
- Alle 46 registrierten Kriterien sind `specified_partial` und mit Testreferenzen hinterlegt. Es gibt keine unveränderten generischen Baseline-Kriterien mehr im aktiven Katalog; die eingefrorene historische Baseline bleibt unverändert. Weitere fachliche Einzelkriterien und vollständige Story-Abnahmen können erforderlich bleiben.
- Für aktuelle Zählwerte und verbleibende Aufgaben gilt `Syzeteo-Testabdeckung-Review-DE.md`; die Detaildokumente von US #10, #21 und #24 enthalten fachliche Testszenarien und gemeldete UI-Freigaben.
