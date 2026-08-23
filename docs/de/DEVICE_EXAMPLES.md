# HDL Buspro Gerätekonfigurationsbeispiele
[🇧🇾 Беларуская](../be/DEVICE_EXAMPLES.md) | 🇩🇪 Deutsch | [🇬🇧 English](../en/DEVICE_EXAMPLES.md) | [🇪🇸 Español](../es/DEVICE_EXAMPLES.md) | [🇫🇷 Français](../fr/DEVICE_EXAMPLES.md) | [🇮🇹 Italiano](../it/DEVICE_EXAMPLES.md) | [🇳🇱 Nederlands](../nl/DEVICE_EXAMPLES.md) | [🇳🇴 Norsk](../no/DEVICE_EXAMPLES.md) | [🇷🇺 Русский](../ru/DEVICE_EXAMPLES.md) | [🇺🇦 Українська](../uk/DEVICE_EXAMPLES.md)

---

Dieses Handbuch bietet praktische UI- und YAML-Konfigurationsbeispiele für alle unterstützten Gerätetypen in der HDL Buspro-Integration.

**Inhaltsverzeichnis:**
- [Befehlsbestätigung (NEU!)](#befehlsbestätigung-neu)
- [Relaisgeräte](#relaisgeräte)
- [Dimmgeräte](#dimmgeräte)
- [Abdeckungsgeräte (Jalousien/Rollläden)](#abdeckungsgeräte)
- [Lüftergeräte](#lüftergeräte)
- [Klimageräte](#klimageräte)
- [Sensorgeräte](#sensorgeräte)
- [Binäre Sensorgeräte](#binäre-sensorgeräte)

---

## Befehlsbestätigung (NEU!)

### Was ist Befehlsbestätigung?

Befehlsbestätigung stellt sicher, dass Gerätzustandsänderungen in Home Assistant erst nach der physikalischen Bestätigung des Geräts widergespiegelt werden. Dies verhindert eine Desynchronisierung der Benutzeroberfläche, wenn Befehle aufgrund von Netzwerkstörungen verloren gehen.

**Ohne Bestätigung:**
- Benutzer klickt „Einschalten"
- Benutzeroberfläche aktualisiert sich sofort (~5ms)
- Gerät empfängt Befehl nach ~100ms
- Wenn Gerät nicht empfängt → Benutzeroberfläche zeigt falschen Zustand

**Mit Bestätigung:**
- Benutzer klickt „Einschalten"
- System wartet auf Gerätebestätigung (~100-500ms)
- Gerät bestätigt Empfang und Ausführung
- Benutzeroberfläche aktualisiert sich nur nach Bestätigung
- Wenn Gerät nicht antwortet → expliziter Timeout-Fehler

### Warum Sie das brauchen

Aktivieren Sie die Bestätigung für:
- **Kritische Geräte** - Notfall-Relais, Hauptschalter
- **Unzuverlässige Netzwerke** - Hohe Störungen, viele Kollisionen
- **Automatisierungsabhängigkeiten** - Automatisierungen, die garantierte Zustände benötigen
- **Sicherheitskritische Geräte** - HVAC-Systeme, Fußbodenheizung

### Konfigurationsbeispiele

#### Für ein kritisches Relais

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Notfall-Stopp-Relais"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

#### Für mehrere kritische Geräte

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      # Kritisch - Empfang bestätigen
      "1.10.1":
        name: "Hauptdeckenlicht"
        enable_confirmation: true
      
      # Unkritisch - schnell halten (Standard)
      "1.10.2":
        name: "Umgebungslicht"
        # enable_confirmation ist standardmäßig false

cover:
  - platform: buspro
    devices:
      "2.10.1":
        name: "Schlafzimmervorhänge"
        enable_confirmation: true
        confirmation_timeout: 10.0  # Länger für mechanische Geräte
        confirmation_retries: 2

climate:
  - platform: buspro
    devices:
      - address: "3.1"
        name: "Wohnzimmer AC"
        enable_confirmation: true
        confirmation_timeout: 5.0
        confirmation_retries: 3
```

### Konfigurationsparameter

| Parameter | Typ | Standard | Bereich | Zweck |
|-----------|------|---------|-------|---------| 
| `enable_confirmation` | boolean | `false` | `true`/`false` | Bestätigung aktivieren/deaktivieren |
| `confirmation_timeout` | float | `5.0` | 0.1-60 Sekunden | Max. Wartezeit für Gerätereaktion |
| `confirmation_retries` | integer | `3` | 0-10 | Wiederholungsversuche bei Timeout |

### Empfehlungen nach Gerätetyp

| Gerätetyp | Timeout | Wiederholungen | Hinweise |
|------------|---------|---------|-------|
| Relais/Schalter | 5.0s | 3 | Schnelles elektronisches Gerät |
| Licht/Dimmer | 5.0s | 3 | Schnelles elektronisches Gerät |
| Lüfter | 5.0s | 3 | Schnelles elektronisches Gerät |
| Abdeckung/Vorhang | 10.0s | 2 | Mechanisches Gerät, langsamer |
| Klima AC | 5.0s | 3 | Elektronisches Gerät |
| Fußbodenheizung | 5.0s | 3 | Elektronisches Gerät |

### Auswirkungen auf die Benutzeroberfläche

Wenn die Bestätigung aktiviert ist:
- **Latenz:** 100-500ms Verzögerung (vs. 5-10ms ohne)
- **Rückmeldung:** Klare Erfolgs-/Fehlermeldung
- **Zuverlässigkeit:** Garantierte Statussynchronisation

Wenn die Bestätigung deaktiviert ist (Standard):
- **Latenz:** ~5-10ms (unverändert)
- **Verhalten:** Fire-and-Forget (aktuelles Verhalten)
- **Risiko:** Stille Befehlsfehler möglich

---

## Relaisgeräte

Relaisgeräte sind einfache Ein-/Aus-Schalter für Beleuchtung, Lüfter und andere binäre Lasten.

**Unterstützte Modelle:**
- `HDL-MR0410.431` - 4 Relaiskanäle
- `HDL-MR0810.432` - 8 Relaiskanäle
- `HDL-MR1210.433` - 12 Relaiskanäle
- `HDL-MR1610.433` - 16 Relaiskanäle
- HDL Hochleistungs-Relaisvarianten (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Relais**
4. Genaues Modell auswählen: **HDL-MR0410.431** (4 Kanäle)
5. Buspro-Adresse eingeben: `1.10`
6. Gerätenamen eingeben: "Wohnzimmerlichter"
7. Kanäle benennen:
   - Kanal 1: "Deckenleuchte"
   - Kanal 2: "Tischlampe"
   - Kanal 3: "Wandleuchte"
   - Kanal 4: "" (leer lassen zum Deaktivieren)
8. Klicken Sie auf **Speichern**

**Ergebnis:**
- `light.wohnzimmerlichter_deckenleuchte`
- `light.wohnzimmerlichter_tischlampe`
- `light.wohnzimmerlichter_wandleuchte`

### YAML-Konfigurationsbeispiel

**Entity-zentrisch (Einzelne Dateien):**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Living Room Ceiling Light"
        object_id: "ceiling_light"
      "1.10.2":
        name: "Living Room Table Lamp"
        object_id: "table_lamp"
      "1.10.3":
        name: "Living Room Wall Sconce"
        object_id: "wall_sconce"
```

**Gerätezentrisch (Vollständige Gerätedefinition):**

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    - address: "1.10"
      name: "Living Room Relays"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
          object_id: "hdl_light_ceiling"
        - number: 2
          name: "Table Lamp"
          enabled: true
          object_id: "hdl_light_table"
        - number: 3
          name: "Wall Sconce"
          enabled: true
          object_id: "hdl_light_sconce"
        - number: 4
          enabled: false
```

---

## Dimmgeräte

Dimmgeräte steuern die Helligkeitsstufen (0-255) für dimmbare Leuchten.

**Unterstützte Modelle:**
- `HDL-MD0206.432` - 2 Dimmkanäle
- `HDL-MD0403.432` - 4 Dimmkanäle
- `HDL-MD0602.432` - 6 Dimmkanäle
- HDL Trailing-Edge-Dimmer (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 Dimmkanäle mit Diagnose

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Dimmer**
4. Genaues Modell auswählen: **HDL-MD0602.432** (6 Kanäle)
5. Buspro-Adresse eingeben: `1.5`
6. Gerätenamen eingeben: "Schlafzimmerdimmer"
7. Kanäle benennen:
   - Kanal 1: "Hauptleuchte"
   - Kanal 2: "Nachttisch Links"
   - Kanal 3: "Nachttisch Rechts"
   - Kanäle 4-6: leer lassen
8. Klicken Sie auf **Speichern**

**Ergebnis:**
- `light.schlafzimmerdimmer_hauptleuchte` (dimmbar 0-255)
- `light.schlafzimmerdimmer_nachttisch_links` (dimmbar 0-255)
- `light.schlafzimmerdimmer_nachttisch_rechts` (dimmbar 0-255)

### YAML-Konfigurationsbeispiel

**Entity-zentrisch:**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Bedroom Main Light"
        dimmable: true
      "1.5.2":
        name: "Bedroom Bedside Left"
        dimmable: true
      "1.5.3":
        name: "Bedroom Bedside Right"
        dimmable: true
```

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_dimmer_main"
        - number: 2
          name: "Bedside Left"
          enabled: true
          object_id: "hdl_dimmer_left"
        - number: 3
          name: "Bedside Right"
          enabled: true
          object_id: "hdl_dimmer_right"
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false
```

---

## Abdeckungsgeräte

Abdeckungsgeräte steuern motorisierte Jalousien, Rollläden und Vorhänge.

**Unterstützte Modelle:**
- `HDL-MW02.431` - 2 Vorhang-/Abdeckungskanäle
- `HDL-MWM45.431` - Vorhang-/Abdeckungsentitäten (konfigurierbare Kanäle)

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Abdeckung**
4. Genaues Modell auswählen: **HDL-MW02.431** (2 Kanäle)
5. Buspro-Adresse eingeben: `2.10`
6. Gerätenamen eingeben: "Wohnzimmerjalousien"
7. Kanäle benennen:
   - Kanal 1: "Fenster"
   - Kanal 2: "Terrassentür"
8. Klicken Sie auf **Speichern**

**Ergebnis:**
- `cover.wohnzimmerjalousien_fenster`
- `cover.wohnzimmerjalousien_terrassentür`

### YAML-Konfigurationsbeispiel

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.10"
      name: "Living Room Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Windows"
          enabled: true
          object_id: "hdl_cover_windows"
        - number: 2
          name: "Patio Door"
          enabled: true
          object_id: "hdl_cover_patio"
```

---

## Lüftergeräte

Lüftergeräte steuern Lüfter mit variabler Geschwindigkeit.

**Unterstützte Modelle:**
- Generisches Lüfterprofil (Lüfter mit variabler Geschwindigkeit)

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Lüfter**
4. Genaues Modell auswählen: **Generisch** (Kanalzahl angeben)
5. Buspro-Adresse eingeben: `3.5`
6. Gerätenamen eingeben: "Badezimmer-Abluftventilator"
7. Kanal benennen: "Hauptlüfter"
8. Klicken Sie auf **Speichern**

**Ergebnis:**
- `fan.badezimmer_abluftventilator_hauptlüfter` (0-255 Geschwindigkeitskontrolle)

### YAML-Konfigurationsbeispiel

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.5"
      name: "Bathroom Exhaust Fan"
      device_type: "fan"
      channels:
        - number: 1
          name: "Main Fan"
          enabled: true
          object_id: "hdl_fan_exhaust"
```

---

## Klimageräte

Klimageräte steuern Temperatur und HVAC-Systeme.

**Unterstützte Modelle:**
- `HDL-MFH04.432` - 4 Fußbodenheizungskanäle
- `HDL-MFH06.432` - 6 Fußbodenheizungskanäle
- `HDL-M/HVAC8.1` - AC-Klimakontrolle
- `HDL-MPED4.431` - AC-Klimakontrolle
- Generisches AC-Profil
- Generisches Fußbodenheizungsprofil

### UI-Konfigurationsbeispiel - AC-Gerät

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Klima**
4. Genaues Modell auswählen: **HDL-M/HVAC8.1** (AC)
5. Buspro-Adresse eingeben: `3.1`
6. Gerätenamen eingeben: "Wohnzimmer-Klimaanlage"
7. Klicken Sie auf **Speichern**

**Ergebnis:**
- `climate.wohnzimmer_klimaanlage` (Zieltemperatur, Modus, Stromkontrolle)

### YAML-Konfigurationsbeispiel

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.1"
      name: "Living Room AC"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"
      object_id: "hdl_climate_ac"

    - address: "4.2"
      name: "Master Bedroom Floor Heating"
      model: "HDL-MFH06.432"
      device_type: "floor_heating"
      channels:
        - number: 1
          name: "Zone 1"
          enabled: true
        - number: 2
          name: "Zone 2"
          enabled: true
        - number: 3
          enabled: false
```

---

## Sensorgeräte

Sensorgeräte liefern Temperatur-, Feuchte-, Beleuchtungs- und Bewegungsdaten.

**Unterstützte Modelle:**
- `HDL-MSP02.4C` - Temperatur, Beleuchtungsstärke, Bewegung
- `HDL-MSP07M.4C` - Temperatur, Beleuchtungsstärke, Feuchte, Bewegung, 2 Kontakte
- `HDL-MS08M.4C` - Temperatur, Beleuchtungsstärke, Bewegung
- `HDL-MS12M.4C` - Temperatur, Beleuchtungsstärke, Feuchte, Bewegung, 2 Kontakte
- `HDL-MCLog.431` - Logik-Controller (nur Lesezugriff)
- Panel-Temperatursensoren (MPTL, MP2B, MP4B, MPL8, etc.)

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Multisensor**
4. Genaues Modell auswählen: **HDL-MSP07M.4C**
5. Buspro-Adresse eingeben: `2.5`
6. Gerätenamen eingeben: "Wohnzimmersensor"
7. Klicken Sie auf **Speichern**

**Ergebnis:**
- `sensor.wohnzimmersensor_temperatur`
- `sensor.wohnzimmersensor_beleuchtungsstärke`
- `sensor.wohnzimmersensor_feuchte`
- `binary_sensor.wohnzimmersensor_bewegung`
- 2 zusätzliche Trockenkontakte

### YAML-Konfigurationsbeispiel

**Entity-zentrisch:**

```yaml
# configuration.yaml
sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: temperature
            name: "Temperature"
            object_id: "hdl_temp_living_room"
          - type: illuminance
            name: "Light Level"
            object_id: "hdl_lux_living_room"
          - type: humidity
            name: "Humidity"
            object_id: "hdl_humidity_living_room"

binary_sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: motion
            name: "Motion"
            object_id: "hdl_motion_living_room"
          - type: dry_contact
            number: 1
            name: "Door Contact"
            object_id: "hdl_door_living_room"
          - type: dry_contact
            number: 2
            name: "Window Contact"
            object_id: "hdl_window_living_room"
```

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
          object_id: "hdl_temp_living_room"
        - type: illuminance
          name: "Illuminance"
          object_id: "hdl_lux_living_room"
        - type: humidity
          name: "Humidity"
          object_id: "hdl_humidity_living_room"
        - type: motion
          name: "Motion"
          object_id: "hdl_motion_living_room"
        - type: dry_contact
          number: 1
          name: "Door Contact"
          object_id: "hdl_door_contact"
        - type: dry_contact
          number: 2
          name: "Window Contact"
          object_id: "hdl_window_contact"
```

---

## Binäre Sensorgeräte

Binäre Sensorgeräte liefern Ein-/Aus-Status von Trockenkontakten und Tür-/Fenstersensoren.

**Unterstützte Modelle:**
- `HDL-MS04.432` - 4 Trockenkontaktkanäle
- `HDL-MS24.232` - 24 Trockenkontaktkanäle
- Multisensoren mit integrierten Kontakten (MSP07M, MS12M, etc.)

### UI-Konfigurationsbeispiel

**Schritte:**
1. Gehen Sie zu **Einstellungen > Geräte & Services > HDL Buspro > Konfigurieren**
2. Klicken Sie auf **Gerät hinzufügen**
3. Gerätetyp auswählen: **Trockenkontakt**
4. Genaues Modell auswählen: **HDL-MS04.432** (4 Kanäle)
5. Buspro-Adresse eingeben: `1.20`
6. Gerätenamen eingeben: "Tür- & Fenstersensoren"
7. Kanäle benennen:
   - Kanal 1: "Haustür"
   - Kanal 2: "Garagentür"
   - Kanal 3: "Wohnzimmerfenster"
   - Kanal 4: leer lassen
8. Klicken Sie auf **Speichern**

**Ergebnis:**
- `binary_sensor.tür_fenstersensoren_haustür`
- `binary_sensor.tür_fenstersensoren_garagentür`
- `binary_sensor.tür_fenstersensoren_wohnzimmerfenster`

### YAML-Konfigurationsbeispiel

**Gerätezentrisch:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.20"
      name: "Door & Window Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
          object_id: "hdl_door_front"
        - number: 2
          name: "Garage Door"
          enabled: true
          object_id: "hdl_door_garage"
        - number: 3
          name: "Living Room Window"
          enabled: true
          object_id: "hdl_window_living_room"
        - number: 4
          enabled: false
```

---

## Komplexes Multi-Gerät-Beispiel

Hier ist eine vollständige Konfigurationsdatei, die mehrere Gerätetypen zeigt, die zusammenarbeiten:

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    # Relay devices
    - address: "1.10"
      name: "Living Room Lights"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
        - number: 2
          name: "Table Lamp"
          enabled: true
        - number: 3
          name: "Wall Sconce"
          enabled: true
        - number: 4
          enabled: false

    # Dimmer devices
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
        - number: 2
          name: "Bedside Left"
          enabled: true
        - number: 3
          name: "Bedside Right"
          enabled: true
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false

    # Cover devices (blinds)
    - address: "2.10"
      name: "Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Living Room"
          enabled: true
        - number: 2
          name: "Patio"
          enabled: true

    # Climate
    - address: "3.1"
      name: "AC Unit"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"

    # Sensors
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
        - type: illuminance
          name: "Illuminance"
        - type: humidity
          name: "Humidity"
        - type: motion
          name: "Motion"
        - type: dry_contact
          number: 1
          name: "Door"
        - type: dry_contact
          number: 2
          name: "Window"

    # Dry contacts
    - address: "1.20"
      name: "Door Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
        - number: 2
          name: "Garage Door"
          enabled: true
        - number: 3
          enabled: false
        - number: 4
          enabled: false
```

---

## Tipps & Best Practices

1. **UI für einfache Setups verwenden** - Die UI bietet eine intuitive Möglichkeit, Geräte hinzuzufügen und zu verwalten, ohne YAML schreiben zu müssen.

2. **YAML für komplexe oder programmatische Konfigurationen verwenden** - YAML ist besser für große Installationen oder wenn Sie eine Versionskontrolle benötigen.

3. **Adressenennung** - Verwenden Sie immer das Format `subnet.device` für Adressen (z.B. `1.5`, `2.10`). Die `subnet`- und `device`-Werte müssen gültige Buspro-Adressen in Ihrem Netzwerk sein.

4. **Kanalnummerierung** - Kanäle werden ab 1 nummeriert. Lassen Sie den Namen eines Kanals in der UI leer, um ihn zu deaktivieren, was verhindert, dass Entitäten für nicht verwendete Kanäle erstellt werden.

5. **Gerätenamen** - Verwenden Sie aussagekräftige, standortbasierte Namen (z.B. "Wohnzimmerlichter" statt "Relais"). Dies macht Automationen und Szenen leichter verständlich.

6. **Object IDs** - In YAML ist `object_id` optional, aber empfohlen. Es steuert den Entity-ID-Slug. Wenn weggelassen, generiert Home Assistant einen basierend auf dem Kanalnamen.

7. **Unique IDs** - Für fortgeschrittene Fälle, in denen Sie Entity-Registry-Einträge manuell steuern müssen, verwenden Sie `unique_id` in der YAML-Konfiguration. Dies ermöglicht es Home Assistant, die Entität zuverlässig zu verfolgen, auch wenn sich der Gerätename ändert.

Weitere Informationen zu YAML-Konfigurationsformaten finden Sie in [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
