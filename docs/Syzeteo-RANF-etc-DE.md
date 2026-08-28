# Syzeteo – Randanforderungen, nichtfunktionale Anforderungen und Geschäftsregeln

Stand: 27.08.2026

## 1. Randanforderungen (RANF)

- [x] **RANF #01 – Erhalt des Datenbestands**  
  **Art:** Technische Randanforderung / Migrationsrandbedingung  
  **Anforderung:**  
  Bei Aktualisierungen von Syzeteo müssen sämtliche bereits vorhandenen fachlichen Daten vollständig und konsistent erhalten bleiben. Änderungen am Datenbankschema dürfen nur so durchgeführt werden, dass bestehende Daten verlustfrei übernommen und weiterhin korrekt verwendet werden können.  
  **Begründung:**  
  Versionswechsel dürfen nicht zum Verlust oder zur unbeabsichtigten Veränderung bereits erfasster Kurs-, Studierenden-, Fragen-, Runden- oder Spieldaten führen. Die ausdrücklich durch den Instructor ausgelöste Löschung eines Kurses gemäß GR #10 ist keine Aktualisierung von Syzeteo und fällt daher nicht unter diese Migrationsrandbedingung.

## 2. Nichtfunktionale Anforderungen (NFANF)

- [x] **NFANF #01 – Keine Individualauswertung**  
  **Art:** Datenschutz / Privacy  
  **Anforderung:**  
  Syzeteo darf keine individuellen Leistungsdaten einzelner Studierender erfassen, speichern oder auswerten. Studierendennamen dürfen ausschließlich für organisatorische Zwecke des Spielbetriebs verwendet werden, insbesondere für:
  - Teamzuordnung,
  - Anwesenheit,
  - Auswahl des Startspielers,
  - reguläre Spielerwahl,
  - Gegenspielerauswahl,
  - Auswahl beim Team Assist.

  Punkte, Statistiken, Spielstände und Auswertungen dürfen ausschließlich auf Team- bzw. Kursebene erfolgen.  
  **Begründung:**  
  Syzeteo dient der spielerischen Wiederholung von Lerninhalten und nicht der individuellen Leistungsbewertung oder der Erstellung personenbezogener Leistungsprofile.

- [x] **NFANF #02 – Rundenbezogene Datenintegrität**  
  **Art:** Integrität / Konsistenz  
  **Anforderung:**  
  Bereits abgeschlossene Spielzüge, Punktestände und protokollierte Fragen dürfen durch spätere Änderungen an Stammdaten oder durch die Aufnahme von Nachzüglern nicht rückwirkend verändert werden. Davon ausgenommen ist die ausdrücklich durch den Instructor ausgelöste vollständige Löschung eines Kurses gemäß GR #10; in diesem Fall werden sämtliche mit diesem Kurs zusammenhängenden Daten gelöscht. Das in US #20 vorgesehene Rückgängigmachen des zuletzt ausgeführten Spielschritts ist eine definierte Spieloperation und gilt nicht als unzulässige rückwirkende Änderung im Sinne dieser Anforderung.  
  **Begründung:**  
  Der dokumentierte Spielverlauf muss während des Bestehens des zugehörigen Kurses nachvollziehbar und konsistent bleiben. Eine bewusste vollständige Kurslöschung stellt dagegen eine ausdrücklich vorgesehene Löschoperation dar.

- [x] **NFANF #03 – Kompakte Spielansicht**  
  **Art:** Usability  
  **Anforderung:**  
  Die Spielansicht soll kompakte querformatige Karten mit gut lesbarem Fragetext verwenden und im normalen Spielbetrieb möglichst ohne vertikales Scrollen bedienbar sein.  
  **Begründung:**  
  Die Anwendung wird im Lehrbetrieb und insbesondere in einer Beamer-Situation eingesetzt. Die wesentlichen Spielinformationen sollen daher ohne unnötige Navigation unmittelbar erfassbar sein.

- [x] **NFANF #04 – Zugriffsschutz**  
  **Art:** Sicherheit / Zugriffskontrolle  
  **Anforderung:**  
  Spiel- und Verwaltungsfunktionen von Syzeteo dürfen nur nach erfolgreicher Authentifizierung zugänglich sein.  
  **Begründung:**  
  Unberechtigte Personen dürfen keine spielrelevanten oder administrativen Daten einsehen oder verändern können.

## 3. Geschäfts- und Spielregeln (GR)

- [x] **GR #01 – Einheitlicher Fragensatz**  
  **Art:** Fachliche Geschäftsregel  
  **Regel:**  
  Für eine Runde muss in allen Kursen derselbe Satz von acht Fachfragen verwendet werden. Die Kartenpositionen dürfen zwischen den Kursen variieren.  
  **Begründung:**  
  Damit spielen alle Kurse innerhalb derselben Runde auf derselben fachlichen Grundlage.

- [x] **GR #02 – Fragensatz unveränderlich**  
  **Art:** Fachliche Integritätsregel  
  **Regel:**  
  Sobald eine Runde erstmals erfolgreich gestartet wurde, darf der dieser Runde zugeordnete Fragensatz nicht mehr verändert werden. Dies umfasst sowohl die Zuordnung der acht Fachfragen als auch den in der Runde verwendeten Frage- und Musterantworttext. Spätere Änderungen einer Frage im globalen Fragenpool dürfen bereits gestartete oder gespielte Runden nicht rückwirkend verändern.  
  **Begründung:**  
  Dadurch bleiben Vergleichbarkeit, Nachvollziehbarkeit und Fragenprotokoll über alle Kurse hinweg erhalten. Die technische Umsetzung kann hierzu insbesondere unveränderliche Rundenkopien der verwendeten Fragen und Musterantworten verwenden.

- [x] **GR #03 – Rundenumfang festgelegt**  
  **Art:** Fachliche Spielregel  
  **Regel:**  
  Jede Runde besteht aus genau acht Fachfragen und einer automatisch ergänzten **Challenge Card** als neunter Karte.  
  **Begründung:**  
  Der feste Umfang definiert die verbindliche Struktur einer Runde.

- [x] **GR #04 – Strikter Teamwechsel**  
  **Art:** Fachliche Spielregel  
  **Regel:**  
  Nach jedem regulären Spielerzug muss das jeweils andere Team an der Reihe sein. Der Teamwechsel darf durch die Art der Spielerwahl nicht aufgehoben werden.  
  **Begründung:**  
  Der strikte Wechsel stellt eine gleichmäßige Beteiligung beider Teams sicher.

- [x] **GR #05 – Einmaliger regulärer Einsatz**  
  **Art:** Fachliche Spielregel  
  **Regel:**  
  Eine Person, die in einer Runde bereits regulär am Zug war, darf in derselben Runde nicht erneut für einen regulären Spielerzug ausgewählt werden. Ein Einsatz ausschließlich über den **Team Assist** gilt nicht als regulärer Spielerzug und sperrt die betreffende Person nicht für einen späteren regulären Spielerzug.  
  **Begründung:**  
  Damit sollen bei den regulären Spielerzügen möglichst viele unterschiedliche Studierende innerhalb einer Runde beteiligt werden, ohne die besondere Funktion des Team Assist einzuschränken.

- [x] **GR #06 – Team-Assist-Ausnahme**  
  **Art:** Fachliche Ausnahmeregel  
  **Regel:**  
  Bei der Auswahl einer Person über den **Team Assist** gilt die reguläre Einsatzsperre nicht. Es dürfen alle anwesenden Mitglieder des betreffenden Teams ausgewählt werden, auch wenn sie in derselben Runde bereits regulär am Zug waren oder bereits über den Team Assist eingesetzt wurden.  
  **Begründung:**  
  Der Team Assist stellt bewusst eine Ausnahme von der regulären Spielerwahl dar.

- [x] **GR #07 – Letzte Karte durch Instructor**  
  **Art:** Fachliche Spielregel  
  **Regel:**  
  Die letzte verbleibende Karte einer Runde wird immer durch den **Instructor** aufgedeckt und beantwortet. Sie wird unabhängig von ihrem Kartentyp nicht gewertet. Für die letzte Karte werden keine Punkte vergeben.  
  **Begründung:**  
  Dies entspricht dem festgelegten Abschluss einer Runde. Die letzte Karte ist unabhängig davon, ob es sich um eine Fachfrage oder die Challenge Card handelt, von der regulären Wertung ausgenommen.

- [x] **GR #08 – Spielerwahlmodus vor Spielbeginn**  
  **Art:** Fachliche Konfigurationsregel  
  **Regel:**  
  Der Modus für die reguläre Spielerwahl ab Spieler 2 wird vor Beginn eines Spiels festgelegt. Standard ist die zufällige Spielerwahl. Nach dem Start des Spiels darf der Modus für dieses laufende Spiel nicht mehr geändert werden.  
  **Begründung:**  
  Der Auswahlmodus muss während eines laufenden Spiels stabil bleiben und zugleich das festgelegte Standardverhalten von Syzeteo beibehalten.

- [x] **GR #09 – Runde je Kurs einmal verwenden**  
  **Art:** Fachliche Geschäftsregel  
  **Regel:**  
  Eine Runde darf in einem Kurs nur einmal regulär durchgeführt werden.  
  **Begründung:**  
  Dadurch wird verhindert, dass dieselbe Runde mit demselben Fragensatz innerhalb eines Kurses mehrfach in die Ergebnis- und Fragenhistorie eingeht.

- [x] **GR #10 – Vollständige Kurslöschung**  
  **Art:** Fachliche Datenregel  
  **Regel:**  
  Wird ein Kurs durch den **Instructor** gelöscht, werden sämtliche mit diesem Kurs zusammenhängenden Daten vollständig gelöscht. Dies umfasst insbesondere Studierende und Teamzuordnungen des Kurses, Anwesenheitsdaten, laufende und abgeschlossene Spiele, Spielstände, Rundenergebnisse, kursbezogene Fragenprotokolle und sonstige ausschließlich diesem Kurs zugeordnete Daten. Globaler, kursübergreifender Datenbestand, insbesondere Lerneinheiten und Fragen des globalen Fragenpools, wird dadurch nicht gelöscht.  
  **Begründung:**  
  Die Kurslöschung ist als vollständige fachliche Löschoperation definiert. Gleichzeitig bleiben globale, nicht ausschließlich dem gelöschten Kurs zugeordnete Lerninhalte erhalten.
