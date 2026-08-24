# Dual-Mode YAML-configuratie

[🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | 🇳🇱 Nederlands | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

---

Het buspro aangepaste component ondersteunt twee complementaire YAML-configuratiebenaderingen:

1. **Op entiteit gebaseerd** (Legacy) - Individuele entiteitsdefinities
2. **Op apparaat gebaseerd** (Modern) - Volledige apparaatdefinities met alle kanalen

Je kunt **beide benaderingen of beide tegelijk gebruiken** in je Home Assistant-configuratie.

## Op entiteit gebaseerd formaat (Legacy)

Definieer entiteiten afzonderlijk. Handig voor het organiseren van entiteiten op domein (lampen, schakelaars, sensoren).

### Kenmerken
- Één entiteit per YAML-invoer
- Focus op specifieke sensortypen of uitgangen
- Automatische groepering van apparaten op adresprefixen
- Geschikt voor individuele entiteitsorganisatie

### Voorbeeld
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

### Bestandsorganisatie

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Op entiteit gebaseerde apparaatconfiguratie
```

## Op apparaat gebaseerd formaat (Modern)

Definieer volledige apparaten met alle bijbehorende kanalen/entiteiten. Handig voor het beheren van alle aspecten van een apparaat op één plek.

### Kenmerken
- Eén apparaat = één YAML-bestand
- Alle kanalen samen gedefinieerd
- Duidelijke apparaatgroepering en structuur
- Geschikt voor uitgebreid apparaatbeheer
- Heeft rechtstreeks betrekking op het buspro-apparaatregister

### Voorbeeld
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

### Bestandsorganisatie

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Op apparaat gebaseerd
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Details van op apparaat gebaseerde kanaalindeling

### Verplichte velden

```yaml
address: "2.5"                    # Apparaatadres (subnet.apparaat)
name: "Device Name"               # Leesbare apparaatnaam
model: "HDL-MD0606.32"           # Apparaatmodel uit catalogus
device_type: "relay|dimmer|..."  # Entiteittype
channels:                         # Lijst met kanalen/entiteiten
  - number: 1                     # Kanalnummer (1-N) of mogelijkheidsnaam
    name: "Channel Name"          # Kanaalachtergrondnaam
    enabled: true                 # Entiteit maken (standaard: true)
```

### Optionele velden

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Entity-ID-achtervoegsel
    unique_id: "buspro-2.5-relay-1"                     # Unieke identificatie
```

## Ondersteunde apparaattypen

**Verlichting:**
- `relay` - Eenvoudige aan/uit-schakelaars
- `dimmer` - Dimbare lampen (helderheidsregeling 0-255)

**Sensoren en ingangen:**
- `dry_contact` - Binaire sensoren (deur-/raamsensoren)
- `multisensor` - Samengestelde omgevingssensoren
- `universal_switch` - Universele schakelaaringangen met dag-/nachtlogica

**Klimaat en HVAC:**
- `floor_heating` - Vloerverwarmings-/temperatuurregelingsmodules
- `ac` - Airconditioningcontrollers

**Gemotoriseerd:**
- `cover` - Blinds-/luikmotoren met positieregeling
- `fan` - Ventilatorsnelheidsregelaars

## Beide benaderingen combineren

Je kunt beide formaten tegelijk gebruiken, zolang ze niet met elkaar conflicteren:

```yaml
buspro:
  devices:
    # Op entiteit gebaseerd: multisensor
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Op apparaat gebaseerd: relais met kanalen
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Belangrijk:** Elk adres kan slechts eenmaal worden gedefinieerd. Gebruik niet hetzelfde adres in beide formaten.

## Apparaatregistergroepering

Beide formaten groeperen entiteiten automatisch onder hun bovenliggende apparaat in het apparaatregister van Home Assistant:

- Apparaten worden geïdentificeerd door **basisadres** (bijvoorbeeld `2.5`)
- Alle entiteiten met adressen `2.5.1`, `2.5.2`, ... worden gegroepeerd onder apparaat `2.5`
- Apparaateigenschappen (naam, model, fabrikant) gelden voor alle entiteiten

### Voorbeeld apparaatregisterhiërarchie

```
Apparaat: Guestroom Relay (2.5)
├── Entiteit: Bra Okno (2.5.1) [dimmer/switch]
└── Entiteit: Bra Dver (2.5.2) [dimmer/switch]

Apparaat: Bathroom Relay (2.4)
├── Entiteit: Main Light (2.4.1) [relay/switch]
└── Entiteit: Exhaust Fan (2.4.2) [relay/switch]
```

## Best practices

### Voor op entiteit gebaseerd:
- Organiseer bestanden op domein (`entities/sensors/`, `entities/lights/`)
- Eén entiteit per bestand
- Gebruik beschrijvende bestandsnamen
- Geschikt voor sensorgerichte configuraties

### Voor op apparaat gebaseerd:
- Organiseer bestanden per kamer of apparaatgroep
- Alle kanalen in één bestand
- Gebruik consistente naamgeving over alle kanalen
- Geschikt voor georganiseerd apparaatbeheer

### Voor beide:
- Dupliceer adressen niet tussen formaten
- Gebruik het formaat dat bij je workflow past
- Overweeg de voorkeuren van je team
- Documenteer je keuze in CLAUDE.md of README
