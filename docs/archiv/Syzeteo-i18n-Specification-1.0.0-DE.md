# Syzeteo – Internationalisierungsspezifikation 1.0.0

Datum: 2026-08-27

## 1. Ziel

Syzeteo 1.0.0 wird mit einer sauberen und erweiterbaren Internationalisierung der vollständigen Anwendungsoberfläche ausgeliefert. Englisch und Deutsch sind initial enthalten. Weitere Sprachen müssen über Sprachkataloge ergänzt werden können, ohne die Domänenlogik zu verändern.

## 2. Architektur

### 2.1 Dateien

```text
locales/
  en.json
  de.json
  README.md
i18n.py
```

Englisch (`en`) ist Referenz- und Fallback-Sprache.

### 2.2 Übersetzungsfunktion

Der Anwendungscode referenziert stabile Übersetzungsschlüssel über die zentrale Übersetzungsschicht. Die Ablaufsteuerung der UI darf niemals von übersetzten Beschriftungen abhängen.

### 2.3 Platzhalter

Platzhalter sind benannt und müssen in allen Sprachkatalogen kompatibel bleiben, zum Beispiel:

```json
"course.label": "Course {code}"
```

Die Übersetzung desselben Schlüssels muss dieselben Platzhalternamen bereitstellen.

## 3. Verbindliche Anforderungen

### I18N #01 – Englische Referenzsprache

Englisch (`en`) ist Referenz- und Fallback-Sprache.

### I18N #02 – Vollständiger deutscher Katalog

Der deutsche Sprachkatalog (`de`) enthält denselben Schlüsselbestand wie der englische Katalog.

### I18N #03 – Externe Sprachkataloge

UI-Texte liegen als UTF-8-JSON-Kataloge außerhalb der Anwendungslogik.

### I18N #04 – Fallback

Fehlt ein Schlüssel in einem Nicht-Referenzkatalog, wird der englische Wert verwendet. Unbekannte Sprachen fallen auf Englisch zurück.

### I18N #05 – Persistente Sprachauswahl

Die gewählte Standard-UI-Sprache kann als sprachneutrale Anwendungseinstellung `ui_locale` gespeichert werden.

### I18N #06 – Sprachauswahl vor Login

Auf der Login-/Ersteinrichtungsseite kann bereits vor der Authentifizierung eine Sprache gewählt werden. Diese Auswahl gilt für die aktuelle Sitzung.

### I18N #07 – Begrenzte Positionen des Sprachwählers

Der Sprachwähler ist ausschließlich auf Login/Ersteinrichtung und in den Instructor Settings verfügbar. Er erscheint weder in der Sidebar noch auf der Account-Seite.

### I18N #08 – Stabile Navigations-IDs

Die Navigation verwendet sprachneutrale Seiten-IDs wie `dashboard`, `courses`, `students`, `game` und `instructor_settings`.

### I18N #09 – Sprachneutrale Domänen-/Statuscodes

Persistierte Werte, Statuscodes, Konfigurationshinweise und Domänenfehlercodes sind sprachneutral.

### I18N #10 – Keine lokalisierten Storage-Meldungen

`storage.py` liefert sprachneutrale `StorageError`-Codes anstelle fertiger lokalisierter Benutzermeldungen.

### I18N #11 – Sprachneutrale Authentifizierungslogik

Die Authentifizierungslogik ist unabhängig von sprachabhängigen UI-Texten.

### I18N #12 – Strukturierte Konfigurationshinweise

Konfigurationswarnungen verwenden stabile Codes und Parameter; der sichtbare Text wird durch die Übersetzungsschicht der UI erzeugt.

### I18N #13 – Nutzerdaten werden nicht übersetzt

Question-Pool-Inhalte, Kursnamen, Studierendennamen, Rundennamen und sonstige Nutzerdaten werden niemals automatisch übersetzt.

### I18N #14 – Sprachneutrale technische Schnittstellen

Datenbankschema-Bezeichner, Seiten-IDs, Einstellungsschlüssel und interne Domänenwerte ändern sich nicht mit der UI-Sprache.

### I18N #15 – Stabile Austauschformate

Das Syzeteo-Question-Pool-JSON-Format ist sprachneutral. Beim Studierenden-CSV-Import werden die englischen Spalten `first_name` / `last_name` und die deutschen Spalten `vorname` / `nachname` unterstützt.

### I18N #16 – Community-Übersetzungen

Weitere Sprachkataloge können ergänzt werden, wenn sie Schlüsselbestand und Platzhaltervertrag des Referenzkatalogs einhalten.

## 4. Sprachauswahl und Persistenz

- Neuinstallationen starten standardmäßig mit Englisch;
- die Auswahl auf Login/Ersteinrichtung gilt für die aktuelle Sitzung;
- in den Instructor Settings kann die Standardsprache persistent gespeichert werden;
- eine gültige gespeicherte Sprache wird bei späteren Logins wiederverwendet;
- nicht verfügbare oder ungültige Sprachen fallen auf Englisch zurück.

## 5. Abnahmetests

Die automatisierte Testsuite muss mindestens prüfen:

- offizielle Sprachkataloge sind gültiges UTF-8-JSON;
- Englisch und Deutsch besitzen identische Schlüsselbestände;
- Platzhalter stimmen überein;
- fehlende Übersetzungen fallen auf Englisch zurück;
- unbekannte Sprachen fallen auf Englisch zurück;
- die Navigation verwendet stabile Seiten-IDs;
- Konfigurationsaktionen verwenden sprachneutrale IDs;
- der Sprachwähler existiert nur auf Login/Ersteinrichtung und in den Instructor Settings;
- `ui_locale` wird korrekt persistiert;
- bekannte deutsche UI-Literale steuern nicht mehr den Anwendungsablauf;
- Storage-Fehler- und Konfigurationshinweisschlüssel sind in beiden offiziellen Katalogen vorhanden;
- jeder in `app.py` literal referenzierte Übersetzungsschlüssel existiert im englischen Katalog;
- jeder in `storage.py` literal referenzierte `StorageError`-Schlüssel existiert im englischen Katalog.

## 6. Aktuelle Katalogbasis

Syzeteo 1.0.0 enthält **473 Übersetzungsschlüssel** in jedem offiziellen Sprachkatalog. Die Schlüsselbestände sind identisch.

## 7. Definition of Done

Die Internationalisierung von Syzeteo 1.0.0 ist abgeschlossen, wenn:

1. jede Anwendungsseite vollständig auf Englisch und Deutsch nutzbar ist;
2. Englisch Referenz- und Fallback-Sprache ist;
3. beide offiziellen Kataloge identische Schlüssel und kompatible Platzhalter besitzen;
4. die Sprachauswahl ausschließlich an den definierten Stellen angeboten wird;
5. die gespeicherte Standardsprache korrekt erhalten bleibt;
6. Question-Pool-Nutzerdaten niemals automatisch übersetzt werden;
7. Domänen- und Persistenzlogik sprachneutral bleiben; und
8. die vollständige automatisierte Testsuite erfolgreich durchläuft.
