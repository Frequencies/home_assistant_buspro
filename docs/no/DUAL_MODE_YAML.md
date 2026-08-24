# Dual-Mode YAML-konfigurasjon

[🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | 🇳🇴 Norsk | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

---

Buspro-komponenten støtter to komplementære YAML-konfigurasjonstilnærminger:

1. **Enhet-sentrert** (Legacy) - Individuelle enhetsdefinisjonerner
2. **Enhet-sentrert** (Modern) - Fullstendige enhetsdefinisjonerner med alle kanaler

Du kan bruke **enten én tilnærming eller begge samtidig** i Home Assistant-konfigurasjonen din.

## Enhet-sentrert format (Legacy)

Definer enheter individuelt. Nyttig for å organisere enheter etter domene (lys, brytere, sensorer).

### Karakteristikker
- Én enhet per YAML-oppføring
- Fokus på spesifikke sensortyper eller utganger
- Automatisk enhetsgruppering etter adresseprefiks
- Egnet for individuell enhetsorganisering

### Eksempel
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

### Filorganisasjon

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Enhetsentrert enhetskonfigurasjon
```

## Enhets-sentrert format (Modern)

Definer fullstendige enheter med alle deres kanaler/enheter. Nyttig for å administrere alle aspekter av en enhet på ett sted.

### Karakteristikker
- Én enhet = én YAML-fil
- Alle kanaler definert sammen
- Tydelig enhetsgruppering og struktur
- Egnet for omfattende enhetadministrasjon
- Kartlegger direkte til buspro-enhetsregisteret

### Eksempel
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

### Filorganisasjon

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Enhetsentrert
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Detaljer om enhetssentrert kanalformat

### Påkrevde felt

```yaml
address: "2.5"                    # Enhetens adresse (subnett.enhet)
name: "Device Name"               # Lesbar enhetsnavn
model: "HDL-MD0606.32"           # Enhetsmodell fra katalogen
device_type: "relay|dimmer|..."  # Enhetstype
channels:                         # Liste over kanaler/enheter
  - number: 1                     # Kanalnummer (1-N) eller mulighetsnavn
    name: "Channel Name"          # Kanals visningsnavn
    enabled: true                 # Opprett enhet (standard: true)
```

### Valgfrie felt

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Entity ID-suffiks
    unique_id: "buspro-2.5-relay-1"                     # Unik identifikator
```

## Støttede enhetstyper

**Belysning:**
- `relay` - Enkle på/av-brytere
- `dimmer` - Dimmbare lys (lysintensitetskontroll 0-255)

**Sensorer og inngang:**
- `dry_contact` - Binære sensorer (dør-/vindueskontakter)
- `multisensor` - Sammensatte miljøsensorer
- `universal_switch` - Universelle bryter-inngang med dag/natt-logikk

**Klima og HVAC:**
- `floor_heating` - Gulvvarmings-/temperaturkontrollmoduler
- `ac` - Klimaanleggskontrollere

**Motorisert:**
- `cover` - Rullegardiner-/persiennemotorer med posisjonsregulering
- `fan` - Viftehastighetsregulatorer

## Blande begge tilnærminger

Du kan bruke begge formater samtidig, så lenge de ikke er i konflikt:

```yaml
buspro:
  devices:
    # Enhetsentrert: multi-sensor
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Enhetsentrert: relé med kanaler
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Viktig:** Hver adresse kan bare defineres én gang. Ikke bruk den samme adressen i begge formater.

## Enhetsregistergruppering

Begge formater grupperer automatisk enheter under deres overordnede enhet i Home Assistants enhetsregister:

- Enheter identifiseres av **basisadresse** (for eksempel `2.5`)
- Alle enheter med adresser `2.5.1`, `2.5.2`, ... er gruppert under enhet `2.5`
- Enhetegenskaper (navn, modell, produsent) gjelder for alle enheter

### Eksempel på enhetsregisterhierarki

```
Enhet: Guestroom Relay (2.5)
├── Enhet: Bra Okno (2.5.1) [dimmer/switch]
└── Enhet: Bra Dver (2.5.2) [dimmer/switch]

Enhet: Bathroom Relay (2.4)
├── Enhet: Main Light (2.4.1) [relay/switch]
└── Enhet: Exhaust Fan (2.4.2) [relay/switch]
```

## Beste praksis

### For enhet-sentrert (Legacy):
- Organiser filer etter domene (`entities/sensors/`, `entities/lights/`)
- Én enhet per fil
- Bruk beskrivende filnavn
- Egnet for sensorintensive konfigurasjoner

### For enhet-sentrert (Modern):
- Organiser filer etter rom eller enhetsgruppe
- Alle kanaler i én fil
- Bruk konsistent navngiving på tvers av kanaler
- Egnet for organisert enhetsadministrasjon

### For begge:
- Dupliker ikke adresser mellom formater
- Bruk formatet som passer til arbeidsflytene
- Vurder teamets preferanser
- Dokumenter valget i CLAUDE.md eller README
