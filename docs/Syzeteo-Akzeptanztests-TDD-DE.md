# Syzeteo – TDD-Akzeptanztestkatalog (Arbeitsstand 29.10.2026)

## Geltung und Methodik

Diese Spezifikation dient der schrittweisen Synchronisation von User Stories und Regressionstests. **Die derzeitige Zuordnung ist ein Kandidatennachweis auf Grundlage der Testmethodennamen, kein Beleg für die vollständige Erfüllung eines Akzeptanzkriteriums.** Die fachliche Referenz bilden `Syzeteo-L-US-DE.md`, `Syzeteo-RANF-etc-DE.md` und `Syzeteo-Traceability-Matrix-DE.md`.

Vor der nächsten fachlichen Änderung sind die Akzeptanzkriterien der betroffenen Story konkret in mehrere überprüfbare Given/When/Then-Szenarien aufzuschlüsseln. Die hier notierte generische Mindestform ersetzt diese Szenarien nicht.

## TDD-Regel (beschlossen)

1. Vorhandene Testlücken werden sichtbar berichtet und blockieren die Pipeline zunächst nicht.
2. Neue oder geänderte User Stories benötigen mindestens einen neuen, ausführbaren und in der Manifestdatei referenzierten automatisierten Akzeptanztest, bevor die Änderung freigegeben wird.
3. Änderungen an Akzeptanzkriterien ohne Story-Textänderung müssen den gleichen Prozess durchlaufen; hierfür ist die Baseline nur nach Review zu aktualisieren. Die CI-Prüfung einer solchen rein semantischen Änderung ist mit dem derzeitigen Mechanismus **nicht automatisch erzwingbar**.
4. Visuelle Kriterien werden hybrid geprüft: technische Tests plus dokumentierte manuelle Abnahme. Die Referenz ist **1920 × 1080 Pixel bei 100 % Browser-Zoom**, jeweils normale Spielansicht und Beamer-Modus.
5. Baseline-Änderungen werden nicht automatisch vorgenommen und gehören in ein gesondert überprüftes Review.

## Übersicht und vorläufige Akzeptanzkriterien

### US #01 – Startspieler ändern

**Fachliche Anforderung:** Als **Instructor** möchte ich den automatisch zufällig bestimmten Startspieler vor der ersten Frage durch eine andere anwesende Person ersetzen können, damit ich den tatsächlichen Startspieler bei Bedarf an die konkrete Spielsituation anpassen kann.

**AC-US01-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #01 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Startspieler ändern“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_first_player_can_be_selected_manually_before_start`, `test_storage.py::test_manual_first_player_must_be_present_and_selected`, `test_storage.py::test_start_player_cannot_be_changed_after_game_creation`, `test_storage.py::test_manual_first_player_is_followed_by_automatic_random_player_two`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #02 – Spielerwahlmodus festlegen

**Fachliche Anforderung:** Als **Instructor** möchte ich vor Beginn eines Spiels in den **Instructor Settings** festlegen können, ob die reguläre Auswahl der Spieler ab Spieler 2 zufällig oder manuell erfolgt, damit ich die Spielerbestimmung an die jeweilige Unterrichts- und Spielsituation anpassen kann.

**AC-US02-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #02 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Spielerwahlmodus festlegen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_manual_first_player_must_be_present_and_selected`, `test_storage.py::test_random_mode_selects_next_player_and_undo_restores_pre_score_state`, `test_storage.py::test_manual_first_player_is_followed_by_automatic_random_player_two`, `test_storage.py::test_manual_next_player_selection_is_rejected_in_random_mode`, `test_storage.py::test_manual_regular_mode_waits_for_instructor_and_accepts_only_next_team`, `test_storage.py::test_manual_regular_mode_player_choice_shares_scoring_undo`, `test_storage.py::test_random_mode_can_complete_all_student_turns_without_repetition`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #03 – Nachzügler aufnehmen

**Fachliche Anforderung:** Als **Instructor** möchte ich während eines laufenden Spiels verspätet eingetroffene Studierende nachträglich in die Runde aufnehmen können, damit diese trotz ihrer Abwesenheit zu Spielbeginn noch am weiteren Spiel teilnehmen können.

**AC-US03-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #03 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Nachzügler aufnehmen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_late_player_is_added_to_running_roster_and_undoable`, `test_storage.py::test_late_player_can_unblock_random_selection`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #04 – Zentrale Instructor Settings

**Fachliche Anforderung:** Als **Instructor** möchte ich systemweite und spielelevante Einstellungen und Statusinformationen auf einer zentralen Seite **„Instructor Settings“** einsehen und, soweit sinnvoll, direkt verwalten können, damit ich jederzeit einen vollständigen Überblick über die aktuelle Konfiguration habe und notwendige Änderungen gezielt vornehmen kann.

**AC-US04-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #04 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Zentrale Instructor Settings“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_i18n.py::test_i18n_language_selection_is_only_login_and_instructor_settings`, `test_storage.py::test_dashboard_configuration_issues_are_language_neutral`.

**Visueller Abnahmenachweis:** Instruktor-Einstellungen prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #05 – Am System anmelden

**Fachliche Anforderung:** Als **Instructor** möchte ich mich an Syzeteo anmelden können, damit ich auf die für mich vorgesehenen Spiel- und Verwaltungsfunktionen zugreifen kann.

**AC-US05-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #05 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Am System anmelden“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_auth.py::test_admin_login_and_changes`, `test_auth.py::test_auth_returns_language_neutral_message_keys`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #06 – Eigenen Account verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich meinen Benutzernamen und mein Passwort ändern können, damit ich meine Zugangsdaten selbst verwalten kann.

**AC-US06-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #06 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Eigenen Account verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_auth.py::test_admin_login_and_changes`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #07 – Kurse verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Kurse anlegen, archivieren, reaktivieren und bei Bedarf vollständig löschen können, damit ich die in Syzeteo verwendeten Lehrveranstaltungen aktuell halten kann. Bei der Löschung eines Kurses werden sämtliche mit diesem Kurs zusammenhängenden Daten gelöscht.

**AC-US07-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #07 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Kurse verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_course_errors_use_language_neutral_codes`, `test_storage.py::test_course_archive_preserves_data_hides_course_and_can_be_reactivated`, `test_storage.py::test_course_with_running_game_cannot_be_archived`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #08 – Studierende verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierende eines Kurses anlegen, bearbeiten sowie aktiv oder inaktiv setzen können, damit der für den Spielbetrieb relevante Teilnehmerbestand aktuell gehalten werden kann.

**AC-US08-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #08 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Studierende verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_student_duplicates.py::test_manual_duplicate_raises_localizable_storage_error`, `test_student_duplicates.py::test_duplicate_name_is_allowed_in_different_course`, `test_student_duplicates.py::test_rename_to_existing_name_raises_same_storage_error`, `test_student_duplicates.py::test_csv_import_still_skips_duplicate_names`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #09 – Studierende importieren

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierendenlisten aus einer CSV-Datei in einen Kurs importieren können, damit ich größere Teilnehmergruppen nicht einzeln erfassen muss.

**AC-US09-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #09 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Studierende importieren“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_student_duplicates.py::test_csv_import_still_skips_duplicate_names`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #10 – Studierende Teams zuordnen

**Fachliche Anforderung:** Als **Instructor** möchte ich Studierende manuell oder zufällig Team 1 oder Team 2 zuordnen können, damit für jeden Kurs eine geeignete Teamstruktur für den Spielbetrieb besteht.

**AC-US10-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #10 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Studierende Teams zuordnen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_team_names.py::test_team_names_can_be_changed_without_changing_internal_team_assignment`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #11 – Anwesenheit festlegen

**Fachliche Anforderung:** Als **Instructor** möchte ich vor Spielbeginn festlegen können, welche Studierenden der beiden Teams anwesend sind, damit während des Spiels nur tatsächlich anwesende Personen für die vorgesehenen Spielerrollen berücksichtigt werden.

**AC-US11-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #11 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Anwesenheit festlegen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_start_requires_four_present_per_team`.

**Visueller Abnahmenachweis:** Anwesenheitsansicht bedienen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #12 – Lerneinheiten verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Lerneinheiten anlegen, bearbeiten und sortieren können, damit der Fragenpool fachlich strukturiert verwaltet werden kann.

**AC-US12-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #12 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Lerneinheiten verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_learning_unit_can_be_reordered_edited_and_only_deleted_without_questions`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #13 – Fragenpool verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich Fragen mit Musterantworten im globalen, kursübergreifenden Fragenpool anlegen, bearbeiten, Lerneinheiten zuordnen und archivieren können, damit die für Syzeteo verfügbaren Fachfragen zentral gepflegt werden können.

**AC-US13-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #13 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Fragenpool verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_question_delete_requires_removal_from_unlocked_round_but_preserves_locked_history`, `test_storage.py::test_question_pool_import_only_adds_new_content_and_never_overwrites_existing`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #14 – Lerninhalte importieren und exportieren

**Fachliche Anforderung:** Als **Instructor** möchte ich Lerneinheiten und Fragen exportieren und in Syzeteo importieren können, damit der fachliche Datenbestand gesichert und zwischen Installationen übertragen werden kann.

**AC-US14-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #14 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Lerninhalte importieren und exportieren“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_release.py::test_rel_04_new_exports_use_syzeteo_format`, `test_storage.py::test_question_pool_import_only_adds_new_content_and_never_overwrites_existing`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #15 – Runden konfigurieren

**Fachliche Anforderung:** Als **Instructor** möchte ich eine Runde aus Fachfragen des globalen Fragenpools konfigurieren können, damit für die Durchführung einer Runde ein definierter Fragensatz bereitsteht.

**AC-US15-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #15 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Runden konfigurieren“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_round_selection_ui.py::test_round_multiselects_do_not_use_streamlit_max_selections_overlay`, `test_round_selection_ui.py::test_exact_eight_remains_a_domain_rule`, `test_storage.py::test_round_has_eight_questions_and_locks_on_start`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #16 – Spiel starten

**Fachliche Anforderung:** Als **Instructor** möchte ich für einen ausgewählten Kurs eine konfigurierte Runde mit den anwesenden Studierenden starten können, damit die Runde durchgeführt werden kann.

**AC-US16-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #16 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Spiel starten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_round_has_eight_questions_and_locks_on_start`, `test_storage.py::test_start_requires_four_present_per_team`, `test_storage.py::test_first_player_can_be_selected_manually_before_start`, `test_storage.py::test_manual_first_player_must_be_present_and_selected`, `test_storage.py::test_manual_first_player_is_followed_by_automatic_random_player_two`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #17 – Fachfragen durchführen und werten

**Fachliche Anforderung:** Als **Instructor** möchte ich während eines Spiels Karten aufdecken, die zugehörige Fachfrage und Musterantwort anzeigen sowie die Antwort werten können, damit der Spielverlauf und die Teampunkte regelkonform fortgeschrieben werden.

**AC-US17-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #17 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Fachfragen durchführen und werten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_release.py::test_rel_09_last_card_is_always_instructor_zero_points`, `test_storage.py::test_no_individual_answer_performance_is_stored`, `test_storage.py::test_random_mode_can_complete_all_student_turns_without_repetition`.

**Visueller Abnahmenachweis:** Kartenansicht und Wertungsanzeige prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #18 – Team Assist einsetzen

**Fachliche Anforderung:** Als **Instructor** möchte ich für das aktive Team den **Team Assist** einsetzen und eine anwesende Person dieses Teams zur Beantwortung der aktuellen Fachfrage auswählen können, damit der vorgesehene Team Assist im Spiel genutzt werden kann.

**AC-US18-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #18 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Team Assist einsetzen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_question_analysis.py::test_analysis_contains_no_individual_student_fields_and_counts_team_assist_normally`, `test_release.py::test_rel_07_schema_uses_native_team_assist_fields`, `test_release.py::test_rel_08_team_assist_does_not_block_later_regular_turn`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #19 – Challenge Card werten

**Fachliche Anforderung:** Als **Instructor** möchte ich die **Challenge Card** entsprechend dem Ergebnis der Challenge-Frage werten können, damit die daraus resultierenden Teampunkte korrekt vergeben werden.

**AC-US19-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #19 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Challenge Card werten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_i18n.py::test_i18n_challenge_card_face_uses_translation_keys`, `test_question_analysis.py::test_analysis_excludes_final_instructor_card_and_challenge_card`, `test_release.py::test_rel_06_challenge_card_uses_native_value`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #20 – Spielschritt rückgängig machen

**Fachliche Anforderung:** Als **Instructor** möchte ich den zuletzt ausgeführten Spielschritt rückgängig machen können, damit eine versehentliche Wertung oder Spielerwahl korrigiert werden kann, ohne das gesamte Spiel neu starten zu müssen.

**AC-US20-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #20 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Spielschritt rückgängig machen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_storage.py::test_random_mode_selects_next_player_and_undo_restores_pre_score_state`, `test_storage.py::test_late_player_is_added_to_running_roster_and_undoable`, `test_storage.py::test_manual_regular_mode_player_choice_shares_scoring_undo`, `test_storage.py::test_undo_info_uses_language_neutral_action_descriptor`, `test_storage.py::test_undo_restores_last_scoring_step`, `test_tic_tac_toe.py::test_no_line_without_three_scored_cards_of_one_team`, `test_tic_tac_toe.py::test_every_line_is_detected_with_its_direction`, `test_tic_tac_toe.py::test_first_completed_line_wins`, `test_tic_tac_toe.py::test_scored_game_cards_form_line_and_undo_removes_it`, `test_tic_tac_toe.py::test_card_markers_have_matching_css`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #21 – Laufendes Spiel fortsetzen

**Fachliche Anforderung:** Als **Instructor** möchte ich ein laufendes Spiel später wieder öffnen und am gespeicherten Spielstand fortsetzen können, damit ein Spiel bei Unterbrechungen nicht verloren geht.

**AC-US21-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #21 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Laufendes Spiel fortsetzen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_game_abort.py::test_running_game_can_be_aborted_and_is_not_running_afterwards`, `test_game_abort.py::test_only_running_games_can_be_aborted`, `test_startup.py::test_startup_preflight_migrates_schema_v2_before_ui_start`, `test_startup.py::test_startup_preflight_rejects_unsupported_future_schema`, `test_startup.py::test_startup_preflight_rejects_foreign_key_violations`, `test_storage.py::test_course_with_running_game_cannot_be_archived`, `test_team_names.py::test_running_game_locks_team_names_and_game_keeps_snapshots`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #22 – Beamer-Modus verwenden

**Fachliche Anforderung:** Als **Instructor** möchte ich die Spielansicht in einen Beamer-Modus umschalten können, damit Karten, Fragen und Spielstand für die Studierenden groß und ohne störende Navigation dargestellt werden.

**AC-US22-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #22 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Beamer-Modus verwenden“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_rendering.py::test_numbered_lines_are_escaped_for_markdown_capable_card_labels`, `test_rendering.py::test_markdown_syntax_in_question_content_is_neutralized`, `test_rendering.py::test_plain_multiline_html_escapes_markup_and_preserves_literal_content`, `test_rendering.py::test_opened_question_renderer_bypasses_streamlit_markdown`, `test_rendering.py::test_round_overview_keeps_outer_position_and_inner_numbered_lines_literal`, `test_rendering.py::test_round_overview_does_not_use_markdown_capable_write_for_question_text`.

**Visueller Abnahmenachweis:** Normalansicht und Beamer-Modus bei 1920×1080, 100 % Zoom abnehmen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #23 – Ergebnisse überblicken

**Fachliche Anforderung:** Als **Instructor** möchte ich nach dem Login Teamstände, Rundenergebnisse, kumulierte Ergebnisse und die Spielhistorie eines Kurses im Ergebnis-Dashboard sehen können, damit ich den bisherigen Spielverlauf und den Gesamtstand jederzeit überblicken kann.

**AC-US23-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #23 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Ergebnisse überblicken“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_game_abort.py::test_aborted_game_is_excluded_from_results`, `test_question_analysis.py::test_analysis_counts_correct_and_incorrect_regular_questions`, `test_question_analysis.py::test_analysis_excludes_final_instructor_card_and_challenge_card`, `test_question_analysis.py::test_analysis_excludes_running_and_aborted_games`, `test_question_analysis.py::test_analysis_can_be_scoped_to_one_course_or_all_courses`, `test_question_analysis.py::test_analysis_separates_changed_question_versions`, `test_question_analysis.py::test_analysis_contains_no_individual_student_fields_and_counts_team_assist_normally`.

**Visueller Abnahmenachweis:** Ergebnis-Dashboard visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #24 – Gespielte Fragen protokollieren

**Fachliche Anforderung:** Als **Instructor** möchte ich nachvollziehen können, welche Fachfragen in welcher Runde und in welchem Kurs tatsächlich gespielt wurden, und dieses Protokoll exportieren können, damit die Verwendung der Fragen für die weitere Lehr- und Klausurplanung dokumentiert ist.

**AC-US24-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #24 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Gespielte Fragen protokollieren“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_release.py::test_rel_03_non_syzeteo_question_pool_format_is_rejected`, `test_storage.py::test_round_has_eight_questions_and_locks_on_start`, `test_storage.py::test_question_pool_import_only_adds_new_content_and_never_overwrites_existing`.

**Visueller Abnahmenachweis:** Export- und Protokollansicht prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #25 – Rundenabdeckung prüfen

**Fachliche Anforderung:** Als **Instructor** möchte ich sehen können, welche Runden in welchen aktiven Kursen bereits gespielt wurden, noch laufen, abgebrochen oder noch offen sind, damit ich die kursübergreifende Durchführung der vorgesehenen Runden überblicken kann.

**AC-US25-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #25 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Rundenabdeckung prüfen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_game_abort.py::test_aborted_game_is_excluded_from_results`, `test_game_abort.py::test_only_aborted_games_can_be_deleted`, `test_game_abort.py::test_delete_aborted_game_cascades_and_round_can_be_started_again`, `test_question_analysis.py::test_analysis_excludes_running_and_aborted_games`.

**Visueller Abnahmenachweis:** Rundenabdeckung visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #26 – Spiel abbrechen und löschen

**Fachliche Anforderung:** Als **Instructor** möchte ich ein laufendes Spiel abbrechen und ein abgebrochenes Spiel auf der **Instructor-Seite** löschen können, damit irrtümlich gestartete oder nicht fortzuführende Spiele den weiteren Spielbetrieb und die Rundenabdeckung nicht blockieren.

**AC-US26-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #26 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Spiel abbrechen und löschen“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_game_abort.py::test_running_game_can_be_aborted_and_is_not_running_afterwards`, `test_game_abort.py::test_aborted_game_is_excluded_from_results`, `test_game_abort.py::test_only_running_games_can_be_aborted`, `test_game_abort.py::test_only_aborted_games_can_be_deleted`, `test_game_abort.py::test_delete_aborted_game_cascades_and_round_can_be_started_again`, `test_question_analysis.py::test_analysis_excludes_running_and_aborted_games`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #27 – Teamnamen verwalten

**Fachliche Anforderung:** Als **Instructor** möchte ich für die beiden Teams eines Kurses frei wählbare Namen vergeben und diese später ändern können, damit die Teams im Spiel unter passenden Bezeichnungen angezeigt werden.

**AC-US27-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #27 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Teamnamen verwalten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_team_names.py::test_custom_team_names_can_be_set_on_course_creation`, `test_team_names.py::test_default_team_names_preserve_previous_behavior`, `test_team_names.py::test_team_names_must_be_nonempty_and_distinct`, `test_team_names.py::test_team_names_can_be_changed_without_changing_internal_team_assignment`, `test_team_names.py::test_running_game_locks_team_names_and_game_keeps_snapshots`, `test_team_names.py::test_ui_uses_course_and_game_specific_team_names`, `test_team_names.py::test_schema_v2_migrates_in_place_to_v3_without_data_loss`.

**Visueller Abnahmenachweis:** Teamnamen im Spiel und Dashboard prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #28 – Fragen auswerten

**Fachliche Anforderung:** Als **Instructor** möchte ich die Ergebnisse gespielter Fachfragen für einen einzelnen Kurs sowie kursübergreifend auswerten können, damit ich erkenne, welche Fragen wie häufig und wie erfolgreich beantwortet wurden.

**AC-US28-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #28 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Fragen auswerten“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_question_analysis.py::test_analysis_counts_correct_and_incorrect_regular_questions`, `test_question_analysis.py::test_analysis_excludes_final_instructor_card_and_challenge_card`, `test_question_analysis.py::test_analysis_excludes_running_and_aborted_games`, `test_question_analysis.py::test_analysis_can_be_scoped_to_one_course_or_all_courses`, `test_question_analysis.py::test_analysis_separates_changed_question_versions`, `test_question_analysis.py::test_analysis_contains_no_individual_student_fields_and_counts_team_assist_normally`.

**Visueller Abnahmenachweis:** Nicht gesondert festgelegt; UI-Anteile im Story-Review prüfen.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

### US #29 – Tic-Tac-Toe auf dem Board

**Fachliche Anforderung:** Als **Instructor** möchte ich, dass gewertete Karten auf dem Board einen Rand in der Farbe des punktenden Teams erhalten und eine vollständige Reihe markiert wird, damit nebenbei ein Tic-Tac-Toe als zusätzlicher spielerischer Anreiz mitläuft, ohne die Spielansicht zu vergrößern oder die reguläre Wertung zu verändern.

**AC-US29-01 (vorläufiges Prüfszenario, zu verfeinern):** Gegeben sind die in US #29 beschriebenen Vorbedingungen und die einschlägigen Geschäftsregeln; wenn der Instructor die Funktion „Tic-Tac-Toe auf dem Board“ bestimmungsgemäß ausführt, dann erfüllt das System die in der Story formulierte Nachbedingung ohne Verletzung der zugeordneten Rand- und Integritätsregeln.

**Zugeordnete automatisierte Tests (Kandidaten, nicht verifiziert):** `test_rendering.py::test_plain_multiline_html_escapes_markup_and_preserves_literal_content`, `test_tic_tac_toe.py::test_no_line_without_three_scored_cards_of_one_team`, `test_tic_tac_toe.py::test_every_line_is_detected_with_its_direction`, `test_tic_tac_toe.py::test_first_completed_line_wins`, `test_tic_tac_toe.py::test_scored_game_cards_form_line_and_undo_removes_it`, `test_tic_tac_toe.py::test_card_markers_have_matching_css`.

**Visueller Abnahmenachweis:** Boardmarkierung, Linie und Einblendung visuell prüfen; Datum, Browser, Prüfer, erwartetes/tatsächliches Ergebnis und Screenshotreferenz dokumentieren.

**Abdeckungsstatus:** teilweise nachgewiesen (Prüfung des Testinhalts erforderlich).

## Dokumentation manueller Prüfungen

| Datum | US / AC | Browser / Version | Auflösung / Zoom | Schritte | Erwartetes Ergebnis | Tatsächliches Ergebnis | Bestanden? | Prüfer | Screenshot-/Ticketlink |
|---|---|---|---|---|---|---|---|---|---|
| – | US22 / AC-US22-01 | – | 1920×1080 / 100 % | Normal- und Beameransicht öffnen, Inhalte/Navigation/Scrollen prüfen | Lesbare Darstellung ohne störende Navigation, gemäß NFANF #03 möglichst ohne vertikales Scrollen | Nicht geprüft | offen | – | – |

## Grenzen des aktuellen Bestands

- Die bisherige CI prüft vorhandene Python-Tests, aber keine Ende-zu-Ende-Browserabläufe.
- Eine Testmethodenzuordnung beweist nicht, dass sämtliche fachlichen Randfälle abgedeckt sind.
- Die Baseline-Prüfung erkennt Story-Textänderungen und neue Stories. Eine Änderung der Akzeptanzkriterien ohne Änderung der User Story kann nur durch verbindliche Review-Konvention sichergestellt werden.
- Die bereits vorhandenen Tests wurden in diesem Schritt nicht ausgeführt; der CI-Lauf liefert dafür den Laufzeitnachweis.
