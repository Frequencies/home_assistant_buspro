# Configurazione YAML Dual-Mode

**Documentation:** [🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | [🇬🇧 English](../en/DUAL_MODE_YAML.md) | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | 🇮🇹 Italiano | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

Il componente personalizzato buspro supporta due approcci di configurazione YAML complementari:

1. **Basato su entità** (Legacy) - Definizioni di entità individuali
2. **Basato su dispositivo** (Modern) - Definizioni complete di dispositivo con tutti i canali

Puoi utilizzare **uno dei due approcci o entrambi simultaneamente** nella configurazione di Home Assistant.

## Formato basato su entità (Legacy)

Definisci le entità singolarmente. Utile per organizzare le entità per dominio (luci, interruttori, sensori).

### Caratteristiche
- Un'entità per voce YAML
- Focus su tipi specifici di sensori o output
- Raggruppamento automatico dei dispositivi per prefisso indirizzo
- Adatto per l'organizzazione di entità individuali

### Esempio
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

### Organizzazione dei file

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Configurazione entità basata su dispositivo
```

## Formato basato su dispositivo (Modern)

Definisci dispositivi completi con tutti i loro canali/entità. Utile per gestire tutti gli aspetti di un dispositivo in un unico posto.

### Caratteristiche
- Un dispositivo = un file YAML
- Tutti i canali definiti insieme
- Raggruppamento e struttura chiara del dispositivo
- Adatto per la gestione completa dei dispositivi
- Mappa direttamente al registro dei dispositivi buspro

### Esempio
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

### Organizzazione dei file

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Basato su dispositivo
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Dettagli del formato canale basato su dispositivo

### Campi obbligatori

```yaml
address: "2.5"                    # Indirizzo dispositivo (sottorete.dispositivo)
name: "Device Name"               # Nome dispositivo leggibile
model: "HDL-MD0606.32"           # Modello dispositivo dal catalogo
device_type: "relay|dimmer|..."  # Tipo entità
channels:                         # Elenco canali/entità
  - number: 1                     # Numero canale (1-N) o nome capacità
    name: "Channel Name"          # Nome visualizzazione canale
    enabled: true                 # Creare entità (impostazione predefinita: true)
```

### Campi facoltativi

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Suffisso ID entità
    unique_id: "buspro-2.5-relay-1"                     # Identificatore univoco
```

## Tipi di dispositivi supportati

**Illuminazione:**
- `relay` - Interruttori semplici on/off
- `dimmer` - Luci dimmerabili (controllo luminosità 0-255)

**Sensori e ingressi:**
- `dry_contact` - Sensori binari (contatti porta/finestra)
- `multisensor` - Sensori ambientali composti
- `universal_switch` - Ingressi interruttore universali con logica giorno/notte

**Clima e HVAC:**
- `floor_heating` - Moduli di riscaldamento a pavimento/controllo temperatura
- `ac` - Controllori di climatizzazione

**Motorizzati:**
- `cover` - Motori persiane/tapparelle con controllo posizione
- `fan` - Controllori velocità ventilatore

## Mescolare entrambi gli approcci

Puoi utilizzare entrambi i formati simultaneamente, purché non siano in conflitto:

```yaml
buspro:
  devices:
    # Basato su entità: multisensore
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Basato su dispositivo: relè con canali
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Importante:** Ogni indirizzo può essere definito solo una volta. Non usare lo stesso indirizzo in entrambi i formati.

## Raggruppamento registro dispositivi

Entrambi i formati raggruppano automaticamente le entità nel loro dispositivo principale nel registro dispositivi di Home Assistant:

- I dispositivi sono identificati dall'**indirizzo base** (ad esempio, `2.5`)
- Tutte le entità con indirizzi `2.5.1`, `2.5.2`, ... vengono raggruppate sotto il dispositivo `2.5`
- Le proprietà del dispositivo (nome, modello, produttore) si applicano a tutte le entità

### Esempio di gerarchia registro dispositivi

```
Dispositivo: Guestroom Relay (2.5)
├── Entità: Bra Okno (2.5.1) [dimmer/switch]
└── Entità: Bra Dver (2.5.2) [dimmer/switch]

Dispositivo: Bathroom Relay (2.4)
├── Entità: Main Light (2.4.1) [relay/switch]
└── Entità: Exhaust Fan (2.4.2) [relay/switch]
```

## Migliori pratiche

### Per basato su entità:
- Organizza i file per dominio (`entities/sensors/`, `entities/lights/`)
- Un'entità per file
- Utilizza nomi di file descrittivi
- Adatto per configurazioni incentrate su sensori

### Per basato su dispositivo:
- Organizza i file per stanza o gruppo di dispositivi
- Tutti i canali in un file
- Usa denominazione coerente su tutti i canali
- Adatto per la gestione organizzata dei dispositivi

### Per entrambi:
- Non duplicare indirizzi tra i formati
- Usa il formato che si adatta al tuo flusso di lavoro
- Considera le preferenze del tuo team
- Documenta la tua scelta in CLAUDE.md o README
