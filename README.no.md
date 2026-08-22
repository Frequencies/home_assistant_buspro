# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Språk

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md) |
[![Norsk](https://flagcdn.com/24x18/no.png) Norsk](README.no.md)

# Med HDL Buspro-integrasjonen kan du kontrollere ditt HDL Buspro-system fra Home Assistant.

## Installasjon

### One-click install (HACS)

[![Åpne Home Assistant-instansen din og åpne et repositorium i Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Manuell installasjon

Under HACS -> Integrasjoner, legg til eget repositorium "https://github.com/Frequencies/home_assistant_buspro" med kategori "Integration". Velg integrasjonen med navn "HDL Buspro" og last ned.

Omstart Home Assistant.

Gå til Innstillinger > Integrasjoner og legg til integrasjon "HDL Buspro". Skriv inn IP-adresse og portnummer for gateway-en.

## Konfigurasjon

#### Lyse plattform
   
For å bruke Buspro-lyset i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
light:
  - platform: buspro
    running_time: 3
    devices:
      1.89.1:
        name: Living Room Light
        running_time: 5
      1.89.2:
        name: Front Door Light
        dimmable: False
        ack_retry_enabled: True
```
+ **running_time** _(int) (Valgfritt)_: Standard kjøretid i sekunder for alle enheter. Kjøretid er 0 sekunder hvis ikke satt.
+ **ack_retry_enabled** _(boolean) (Valgfritt)_: Aktiverer engangs-kommando-retry når ingen ACK mottas innen 0,8s. Standard er `True`.
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **X.X.X** _(Påkrevd)_: Adressen til enheten på formatet `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Påkrevd)_: Enhetens navn
    + **running_time** _(int) (Valgfritt)_: Kjøretid i sekunder for enheten. Hvis utelatt, brukes standard kjøretid for alle enheter.
    + **ack_retry_enabled** _(boolean) (Valgfritt)_: Enhetstilpasset override for ACK retry.
    + **dimmable** _(boolean) (Valgfritt)_: Er enheten dimbar? Standard er True.
    + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
    + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.

#### Plattform for bytte

For å bruke Buspro-kontakt i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **X.X.X** _(Påkrevd)_: Adressen til enheten på formatet `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Påkrevd)_: Enhetens navn
    + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
    + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.

#### Sensorplattform

For å bruke Buspro-sensor i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: temperature
        unit_of_measurement: °C
        device_class: temperature
        device: dlp
      - address: "1.74"
        name: Front Door
        type: illuminance
        unit_of_measurement: lux
      - address: "1.75"
        name: Hall
        type: humidity
        unit_of_measurement: "%"
        scan_interval: 30
```
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **address** _(string) (Påkrevd)_: Adressen til sensor-enheten på formatet `<subnet ID>.<device ID>`
  + **name** _(string) (Påkrevd)_: Enhetens navn
  + **type** _(string) (Påkrevd)_: Type sensor som skal overvåkes.
    + Tilgjengelige sensorer:
     + temperature
     + illuminance
     + humidity
  + **unit_of_measurement** _(string) (Valgfritt)_: Tekst som skal vises som måleenhet
  + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
  + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.
  + **device_class** _(string) (Valgfritt)_: Gyldig HASS sensor device class (f.eks. "temperature"). Hvis utelatt velges standard fra sensortypen.
  + **scan_interval** _(int) (Valgfritt)_: Polling-interval i sekunder. Hvis utelatt eller `0`, oppdateringer av Buspro-meldinger.
  (https://www.home-assistant.io/components/sensor/)
  + **device** _(string) (Valgfritt)_: Type sensor-enhet:
    + dlp

#### Binær sensor plattform

For å bruke Buspro binær sensor i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
binary_sensor:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Living Room
        type: motion
        device_class: motion
      - address: "1.74.100"
        name: Front Door
        type: universal_switch
      - address: "1.75.3"
        name: Kitchen switch
        type: single_channel
        scan_interval: 15
```
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **address** _(string) (Påkrevd)_: Adressen til sensor-enheten på formatet `<subnet ID>.<device ID>`. Hvis
  'type' = 'universal_switch' universell switch-nummer må legges til adressen.
  + **name** _(string) (Påkrevd)_: Enhetens navn
  + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
  + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.
  + **type** _(string) (Påkrevd)_: Type sensor som skal overvåkes.
    + Tilgjengelige sensorer:
      + motion
      + dry_contact_1
      + dry_contact_2
      + universal_switch
      + single_channel
      + dry_contact
    + Adresseformat-notater:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(string) (Valgfritt)_: Gyldig HASS binary sensor device class (f.eks. "motion"). Hvis utelatt, ingen device class blir tvunget.
  + **scan_interval** _(int) (Valgfritt)_: Polling-interval i sekunder. Hvis utelatt eller `0`, oppdateringer av Buspro-meldinger.
  (https://www.home-assistant.io/components/binary_sensor/)

#### Klima plattform

For å bruke Buspro panel klima kontroll i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
climate:
  - platform: buspro
    devices:
      - address: "1.74"
        name: Bedroom AC
        type: ac
      - address: "1.74"
        name: Living Room
        type: floor_heating
        floor_heating_device_type: dlp
        preset_modes: 
          - none
          - away
          - home
          - sleep
      - address: "1.90"
        type: floor_heating
        floor_heating_device_type: module
        channel: 1
        unique_id: "hdl_climate_floorheat_zone_1"
        min_temp: 22
        max_temp: 32
        precision: 1
        name: Floor Heating Zone 1
```
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **address** _(string) (Påkrevd)_: Adressen til sensor-enheten på formatet `<subnet ID>.<device ID>`
  + **name** _(string) (Påkrevd)_: Enhetens navn
  + **type** _(string) (Valgfritt)_: `ac` eller `floor_heating`. Standard er `floor_heating`.
  + **floor_heating_device_type** _(string) (Valgfritt)_: `dlp` eller `module`.
    Hvis utelatt, `module` velges automatisk når `channel` er gitt, ellers `dlp`.
  + **relay_address** _(string) (Valgfritt)_: Relé kanal adresse i format `<subnet ID>.<device ID>.<channel>`. Brukes som ekstern relé-status tilbakemelding for HVAC-handling.
  + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
  + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.
  + **preset_modes** _(list) (Valgfritt)_: Liste over støttede preset-modus. Preset modus-valg er deaktivert hvis ikke satt. Mulige verdier vises i tabell nedenfor. Tilsvarende modi må aktiveres i HDL (Floor Heating > Working Settings > Mode).
  + **channel** _(int) (Valgfritt)_: Floor heating modul kanal (`1..6`) for `floor_heating_device_type: module`.
  + **min_temp** _(float) (Valgfritt)_: Minimum mål temperatur vist i Home Assistant UI.
  + **max_temp** _(float) (Valgfritt)_: Maksimum mål temperatur vist i Home Assistant UI.
  + **precision** _(float) (Valgfritt)_: Mål temperatur steg i Home Assistant UI. Tillatt verdier: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Cover plattform

For å bruke Buspro covers i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Påkrevd)_: Kartlegging av Buspro gardinkanaler
  + **key** _(string)_: `<subnet ID>.<device ID>.<channel>`
  + **name** _(string) (Påkrevd)_: Vennlig navn
  + **invert** _(bool) (Valgfritt)_: Inverter åpen/lukk-retning. Standard `false`.
  + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra navn.
  + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.

Støttete funksjoner:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

#### Vifte plattform

For å bruke Buspro vifte i installasjonen, legg til følgende i configuration.yaml-filen:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Bedroom Fan
        dimmable: true
      1.89.4:
        name: Bathroom Fan
        dimmable: false
```
+ **running_time** _(int) (Valgfritt)_: Standard kjøretid i sekunder for alle enheter. Kjøretid er `0` hvis ikke satt.
+ **ack_retry_enabled** _(boolean) (Valgfritt)_: Aktiverer engangs-kommando-retry når ingen ACK mottas innen 0,8s. Standard er `True`.
+ **devices** _(Påkrevd)_: En liste over enheter som skal konfigureres
  + **X.X.X** _(Påkrevd)_: Adressen til enheten på formatet `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Påkrevd)_: Enhetens navn
    + **running_time** _(int) (Valgfritt)_: Per-enhet kjøretid i sekunder. Hvis utelatt, brukes standard kjøretid for plattformen.
    + **ack_retry_enabled** _(boolean) (Valgfritt)_: Per-enhet override for ACK retry.
    + **dimmable** _(boolean) (Valgfritt)_: Er viftehastighet kontrollerbar (prosent-modus). Standard er `True`.
    + **object_id** _(string) (Valgfritt)_: Enhets object_id. Standard genereres automatisk fra enhetsnavn.
    + **unique_id** _(string) (Valgfritt)_: Stabil enhets unique_id for Home Assistant entity-register.

---
## Migreringsnotater

Hvis du oppgraderer fra en tidligere versjon av denne integrasjonen, sjekk følgende:

- **v1.7.1 -> v2.0.0 klima breaking changes**
  - Klima-modellen ble delt:
    - `type: ac` opprett nå AC klima-oppførsel.
    - `type: floor_heating` opprett nå floor-heating-oppførsel.
    - Hvis `type` utelatt, standard er `floor_heating`.
  - Ny floor-heating enhet-typing:
    - `floor_heating_device_type: dlp | module` introdusert.
    - Hvis `channel` er gitt og `floor_heating_device_type` utelatt, enhettype auto-bytter til `module`.
    - For `floor_heating_device_type: module`, `channel` påkrevd (`1..6`), ellers enhet-oppsett hoppes over.
  - HVAC mode-oppførsel endret:
    - AC enheter viser `COOL/OFF`.
    - Floor-heating enheter viser `HEAT/OFF` (`COOL` tilgjengelig også for module type).
  - Handling påkrevd:
    - Eksplisitt sett `type` for hver klima-enhet under migrasjon.
    - Legg til `floor_heating_device_type` og `channel` for floor-heating modul enheter.
    - Re-sjekk automasjoner/skript som antas gammel klima-mode semantikk.

- Enhet domene-rettelse:
  - Bryt enheter bruker nå `switch.*` IDs (tidligere noen opprettet som `light.*`).
  - Sensor enheter bruker nå `sensor.*` IDs (tidligere noen opprettet som `light.*`).
  - Binary sensor enheter bruker nå `binary_sensor.*` IDs (tidligere noen opprettet som `light.*`).
- Oppdater dashboards, automasjoner, skript, og hjelpere som refererte gamle enhet IDs.
- `sensor` og `binary_sensor` validerer nå:
  - `scan_interval` som positiv integer-sekunder (`0` holder melding-drivne oppdateringer).
  - `device_class` som gyldig Home Assistant klasse (ugyldige verdier ignoreres for binary sensorer).

---
## Tjenester

#### Sende en vilkårlig melding:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Aktivere en scene:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Stille en universal switch:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
