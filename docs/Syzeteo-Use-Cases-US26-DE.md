# Syzeteo – Use Cases zu US #26

Stand: 31.08.2026

## Use Case: Spiel abbrechen

**Ziel:**  
Ein laufendes Spiel beenden, ohne es als regulär abgeschlossenes Spiel zu werten.

**Vorbedingung:**  
Der Instructor befindet sich in einem laufenden Spiel.

**Nachbedingung Erfolg:**  
Das Spiel ist abgebrochen. Es gilt weder als laufendes noch als regulär abgeschlossenes Spiel, kann nicht fortgesetzt werden und kann anschließend gelöscht werden.

**Nachbedingung Fehlschlag:**  
Das Spiel bleibt unverändert als laufendes Spiel bestehen.

**Akteure:**  
Instructor

**Auslösendes Ereignis:**  
Der Instructor wählt die Funktion „Spiel abbrechen“.

**Beschreibung:**

1. Syzeteo fordert den Instructor auf, den Abbruch zu bestätigen.
2. Der Instructor bestätigt den Abbruch.
3. Syzeteo bricht das Spiel ab.
4. Syzeteo bestätigt den erfolgreichen Abbruch und öffnet die Instructor-Seite.

**Erweiterungen:**

**2a. Der Instructor bestätigt den Abbruch nicht.**  
2a1. Syzeteo schließt die Bestätigungsabfrage und zeigt dem Instructor wieder das laufende Spiel an.

**3a. Syzeteo kann den Abbruch nicht durchführen.**  
3a1. Syzeteo informiert den Instructor über den fehlgeschlagenen Abbruch.  
3a2. Syzeteo zeigt dem Instructor wieder das laufende Spiel an.

**Alternativen:**  
Keine.

---

## Use Case: Spiel löschen

**Ziel:**  
Ein abgebrochenes Spiel vollständig entfernen, damit die zugehörige Runde für den betreffenden Kurs erneut durchgeführt werden kann.

**Vorbedingung:**  
Der Instructor befindet sich auf der Instructor-Seite. Mindestens ein abgebrochenes Spiel ist vorhanden.

**Nachbedingung Erfolg:**  
Das ausgewählte Spiel und alle ausschließlich diesem Spiel zugeordneten Daten sind gelöscht. Die zugehörige Runde gilt für den betreffenden Kurs wieder als offen.

**Nachbedingung Fehlschlag:**  
Das ausgewählte Spiel und alle zugehörigen Daten bleiben unverändert erhalten.

**Akteure:**  
Instructor

**Auslösendes Ereignis:**  
Der Instructor wählt ein abgebrochenes Spiel zum Löschen aus.

**Beschreibung:**

1. Syzeteo zeigt dem Instructor das ausgewählte Spiel und fordert ihn auf, die Löschung zu bestätigen.
2. Der Instructor bestätigt die Löschung.
3. Syzeteo löscht das ausgewählte Spiel.
4. Syzeteo bestätigt dem Instructor die erfolgreiche Löschung.

**Erweiterungen:**

**2a. Der Instructor bestätigt die Löschung nicht.**  
2a1. Syzeteo schließt die Bestätigungsabfrage und zeigt dem Instructor wieder die Instructor-Seite an.

**3a. Syzeteo kann die Löschung nicht durchführen.**  
3a1. Syzeteo informiert den Instructor über die fehlgeschlagene Löschung.  
3a2. Syzeteo zeigt dem Instructor wieder die Instructor-Seite an.

**Alternativen:**  
Keine.
