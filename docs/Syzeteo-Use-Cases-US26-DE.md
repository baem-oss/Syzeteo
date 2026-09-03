# Syzeteo – Use Cases zu US #26

Stand: 03.09.2026

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
4. Syzeteo bestätigt dem Instructor den erfolgreichen Abbruch.
5. Syzeteo öffnet die Instructor-Seite.

**Erweiterungen:**  
Keine.

**Alternativen:**

**2a. Der Instructor verwirft den Abbruch.**  
2a1. Syzeteo schließt die Bestätigungsabfrage.  
2a2. Syzeteo zeigt dem Instructor wieder das laufende Spiel an.

**3a. Syzeteo kann das laufende Spiel nicht abbrechen.**  
3a1. Syzeteo informiert den Instructor über den fehlgeschlagenen Abbruch.  
3a2. Syzeteo zeigt dem Instructor wieder das laufende Spiel an.

---

## Use Case: Spiel löschen

**Ziel:**  
Ein abgebrochenes Spiel löschen, damit die zugehörige Runde für den betreffenden Kurs erneut durchgeführt werden kann.

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

1. Syzeteo zeigt dem Instructor das ausgewählte Spiel an.
2. Syzeteo fordert den Instructor auf, die Löschung zu bestätigen.
3. Der Instructor bestätigt die Löschung.
4. Syzeteo löscht das ausgewählte Spiel.
5. Syzeteo bestätigt dem Instructor die erfolgreiche Löschung.

**Erweiterungen:**  
Keine.

**Alternativen:**

**3a. Der Instructor verwirft die Löschung.**  
3a1. Syzeteo schließt die Bestätigungsabfrage.  
3a2. Syzeteo zeigt dem Instructor wieder die Instructor-Seite an.

**4a. Syzeteo kann das ausgewählte Spiel nicht löschen.**  
4a1. Syzeteo informiert den Instructor über die fehlgeschlagene Löschung.  
4a2. Syzeteo zeigt dem Instructor wieder die Instructor-Seite an.
