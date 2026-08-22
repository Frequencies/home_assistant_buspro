# Dual-Mode YAML-Konfiguration

**Documentation:** [🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | 🇩🇪 Deutsch | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

Die buspro-Benutzerdefinierte Komponente unterstützt zwei komplementäre YAML-Konfigurationsansätze:

1. **Entity-zentriert** (Legacy) - Individuelle Entitätsdefinitionen
2. **Device-zentriert** (Modern) - Vollständige Gerätedefinitionen mit allen Kanälen

Sie können **entweder einen Ansatz oder beide gleichzeitig** in Ihrer Home Assistant-Konfiguration verwenden.

## Entity-zentriertes Format (Legacy)

Definieren Sie Entitäten einzeln. Nützlich zur Organisation von Entitäten nach Domänen (Leuchten, Schalter, Sensoren).

### Eigenschaften
- Eine Entität pro YAML-Eintrag
- Fokus auf spezifische Sensortypen oder Ausgaben
- Automatische Gerätegruppe nach Adresspräfix
- Geeignet für die Organisation einzelner Entitäten

### Beispiel
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"
        - type: illuminance
          name: "Kitchen Illuminance"
          object_id: "hdl_sensor_illuminance_kitchen_ceiling"
```

### Dateiorganisation

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Entity-zentrierte Gerätekonfiguration
```

## Device-zentriertes Format (Modern)

Definieren Sie vollständige Geräte mit allen ihren Kanälen/Entitäten. Nützlich zur Verwaltung aller Aspekte eines Geräts an einer Stelle.

### Eigenschaften
- Ein Gerät = eine YAML-Datei
- Alle Kanäle zusammen definiert
- Klare Gerätegruppe und Struktur
- Geeignet für umfassende Geräteverwaltung
- Entspricht direkt der buspro-Geräteregistrierung

### Beispiel
```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_switch_light_bathroom_main"
        - number: 2
          name: "Exhaust Fan"
          enabled: true
          object_id: "hdl_switch_fan_bathroom_exhaust"

    - address: "2.5"
      name: "Guestroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Bra Okno"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_window"
        - number: 2
          name: "Bra Dver"
          enabled: true
          object_id: "hdl_switch_light_guestroom_bra_door"
```

### Dateiorganisation

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Device-zentriert
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Details zum Device-zentrierten Kanalformat

### Erforderliche Felder

```yaml
address: "2.5"                    # Geräteadresse (Subnetz.Gerät)
name: "Device Name"               # Benutzerfreundlicher Gerätename
model: "HDL-MD0606.32"           # Gerätemodell aus dem Katalog
device_type: "relay|dimmer|..."  # Entitätstyp
channels:                         # Liste der Kanäle/Entitäten
  - number: 1                     # Kanalnummer (1-N) oder Fähigkeitsname
    name: "Channel Name"          # Kanalanzeigename
    enabled: true                 # Entität erstellen (Standard: true)
```

### Optionale Felder

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Entity-ID-Suffix
    unique_id: "buspro-2.5-relay-1"                     # Eindeutige Kennung
```

## Unterstützte Gerätetypen

**Beleuchtung:**
- `relay` - Einfache An/Aus-Schalter
- `dimmer` - Dimmbare Leuchten (Helligkeitsregelung 0-255)

**Sensoren und Eingaben:**
- `dry_contact` - Binärsensoren (Tür-/Fensterkontakte)
- `multisensor` - Zusammengesetzte Umgebungssensoren
- `universal_switch` - Universelle Schaltereingänge mit Tag/Nacht-Logik

**Klima und HVAC:**
- `floor_heating` - Fußbodenheizungs-/Temperaturregelungsmodule
- `ac` - Klimaanlagenregler

**Motorisiert:**
- `cover` - Jalousien-/Rollladenmotoren mit Positionsregelung
- `fan` - Lüfterdrehzahlregler

## Mischen beider Ansätze

Sie können beide Formate gleichzeitig verwenden, solange sie nicht in Konflikt geraten:

```yaml
buspro:
  devices:
    # Entity-zentriert: Multi-Sensor
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Device-zentriert: Relais mit Kanälen
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Wichtig:** Jede Adresse kann nur einmal definiert werden. Verwenden Sie nicht dieselbe Adresse in beiden Formaten.

## Geräteverzeichnis-Gruppierung

Beide Formate gruppieren Entitäten automatisch unter ihrem übergeordneten Gerät in Home Assistants Geräteregister:

- Geräte werden durch **Basisadresse** identifiziert (z. B. `2.5`)
- Alle Entitäten mit Adressen `2.5.1`, `2.5.2`, ... werden unter Gerät `2.5` gruppiert
- Geräteeigenschaften (Name, Modell, Hersteller) gelten für alle Entitäten

### Beispiel Geräteverzeichnis-Hierarchie

```
Gerät: Guestroom Relay (2.5)
├── Entität: Bra Okno (2.5.1) [dimmer/switch]
└── Entität: Bra Dver (2.5.2) [dimmer/switch]

Gerät: Bathroom Relay (2.4)
├── Entität: Main Light (2.4.1) [relay/switch]
└── Entität: Exhaust Fan (2.4.2) [relay/switch]
```

## Best Practices

### Für Entity-zentriert:
- Organisieren Sie Dateien nach Domäne (`entities/sensors/`, `entities/lights/`)
- Eine Entität pro Datei
- Verwenden Sie aussagekräftige Dateinamen
- Geeignet für sensorlastige Konfigurationen

### Für Device-zentriert:
- Organisieren Sie Dateien nach Raum oder Gerätegruppe
- Alle Kanäle in einer Datei
- Verwenden Sie konsistente Benennung über alle Kanäle
- Geeignet für organisierte Geräteverwaltung

### Für beide:
- Duplizieren Sie Adressen nicht zwischen Formaten
- Verwenden Sie das Format, das Ihrem Arbeitsablauf entspricht
- Berücksichtigen Sie die Vorlieben Ihres Teams
- Dokumentieren Sie Ihre Wahl in CLAUDE.md oder README
