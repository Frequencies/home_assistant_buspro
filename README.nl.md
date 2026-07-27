# HDL Buspro
## Talen

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md)

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

Dankzij de HDL Buspro-integratie kunt u uw HDL Buspro-systeem bedienen vanuit Home Assistant.

## Installatie
Voeg onder HACS -> Integraties de aangepaste repository "https://github.com/Frequencies/home_assistant_buspro" toe met de categorie "Integratie". Selecteer de integratie met de naam "HDL Buspro" en download deze.

Start Home Assistant opnieuw.

Ga naar Instellingen > Integraties en voeg Integratie "HDL Buspro" toe. Voer het IP-adres en poortnummer van de gateway in.

## Configuratie

#### Licht platform
   
Om uw Buspro-lamp in uw installatie te gebruiken, voegt u het volgende toe aan uw configuratie.yaml-bestand:

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
+ **running_time** _(int) (Optioneel)_: standaard looptijd in seconden voor alle apparaten. De looptijd is 0 seconden als deze niet is ingesteld.
+ **ack_retry_enabled** _(boolean) (Optioneel)_: Schakelt eenmalige herpoging van een opdracht in als binnen 0,8 s geen ACK wordt ontvangen. Standaard is `True`.
+ **apparaten** _(vereist)_: een lijst met apparaten die moeten worden ingesteld
  + **X.X.X** _(Vereist)_: Het adres van het apparaat in de notatie `<subnet-ID>.<apparaat-ID>.<kanaalnummer>`
    + **naam** _(string) (vereist)_: de naam van het apparaat
    + **running_time** _(int) (Optioneel)_: de looptijd in seconden voor het apparaat. Als u dit weglaat, wordt de standaardlooptijd voor alle apparaten gebruikt.
    + **ack_retry_enabled** _(boolean) (Optioneel)_: Overschrijving per apparaat voor ACK-herpoging.
    + **dimbaar** _(boolean) (Optioneel)_: Is het apparaat dimbaar? Standaard is Waar.
    + **object_id** _(string) (Optioneel)_: Object_id van apparaat. De standaardwaarde wordt automatisch gegenereerd op basis van de apparaatnaam.
    + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.

#### Van platform wisselen

Om uw Buspro-switch in uw installatie te gebruiken, voegt u het volgende toe aan uw configuratie.yaml-bestand:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **apparaten** _(vereist)_: een lijst met apparaten die moeten worden ingesteld
  + **X.X.X** _(Vereist)_: Het adres van het apparaat in de notatie `<subnet-ID>.<apparaat-ID>.<kanaalnummer>`
    + **naam** _(string) (vereist)_: de naam van het apparaat
    + **object_id** _(string) (Optioneel)_: Object_id van apparaat. De standaardwaarde wordt automatisch gegenereerd op basis van de apparaatnaam.
    + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.

#### Sensorplatform

Om uw Buspro-sensor in uw installatie te gebruiken, voegt u het volgende toe aan uw configuratie.yaml-bestand:

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
```
+ **apparaten** _(vereist)_: een lijst met apparaten die moeten worden ingesteld
  + **adres** _(string) (vereist)_: het adres van het sensorapparaat in de indeling `<subnet-ID>.<apparaat-ID>`
  + **naam** _(string) (vereist)_: de naam van het apparaat
  + **type** _(string) (vereist)_: type sensor dat moet worden bewaakt.
    + Beschikbare sensoren:
     + temperatuur
     + verlichtingssterkte
     + luchtvochtigheid
  + **unit_of_measurement** _(string) (Optioneel)_: tekst die moet worden weergegeven als meeteenheid
  + **object_id** _(string) (Optioneel)_: Object_id van apparaat. De standaardwaarde wordt automatisch gegenereerd op basis van de apparaatnaam.
  + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.
  + **device_class** _(string) (Optioneel)_: HASS-apparaatklasse, bijvoorbeeld 'temperatuur'
  + **scan_interval** _(int) (Optioneel)_: Pollinginterval in seconden. Als dit ontbreekt of `0` is, verlopen updates alleen via Buspro-berichten.
(https://www.home-assistant.io/components/sensor/)
  + **apparaat** _(string) (Optioneel)_: Het type sensorapparaat:
    + dlp

#### Binair sensorplatform

Om uw Buspro binaire sensor in uw installatie te gebruiken, voegt u het volgende toe aan uw configuratie.yaml-bestand:

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
```
+ **apparaten** _(vereist)_: een lijst met apparaten die moeten worden ingesteld
  + **adres** _(string) (vereist)_: het adres van het sensorapparaat in de notatie `<subnet-ID>.<apparaat-ID>`. Als
'type' = 'universal_switch' universeel schakelaarnummer moet aan het adres worden toegevoegd.
  + **naam** _(string) (vereist)_: de naam van het apparaat
  + **object_id** _(string) (Optioneel)_: Object_id van apparaat. De standaardwaarde wordt automatisch gegenereerd op basis van de apparaatnaam.
  + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.
  + **type** _(string) (vereist)_: type sensor dat moet worden bewaakt.
    + Beschikbare sensoren:
      + beweging
      + droog_contact_1
      + droog_contact_2
      + universele_schakelaar
      + enkel_kanaal
      + dry_contact
    + Opmerkingen over adresformaat:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(string) (Optioneel)_: HASS-apparaatklasse, bijvoorbeeld 'motion'
  + **scan_interval** _(int) (Optioneel)_: Pollinginterval in seconden. Als dit ontbreekt of `0` is, verlopen updates alleen via Buspro-berichten.
(https://www.home-assistant.io/components/binary_sensor/)

#### Klimaatplatform

Om uw Buspro paneelklimaatbeheersing in uw installatie te gebruiken, voegt u het volgende toe aan uw configuratie.yaml-bestand:

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
+ **apparaten** _(vereist)_: een lijst met apparaten die moeten worden ingesteld
  + **adres** _(string) (vereist)_: het adres van het sensorapparaat in de indeling `<subnet-ID>.<apparaat-ID>`
  + **naam** _(string) (vereist)_: de naam van het apparaat
  + **type** _(string) (Optioneel)_: `ac` of `floor_heat`. Standaard is `vloerverwarming`.
  + **floor_heating_device_type** _(string) (Optioneel)_: `dlp` of `module`.
Indien dit wordt weggelaten, wordt `module` automatisch geselecteerd wanneer `channel` wordt opgegeven, anders `dlp`.
  + **relay_address** _(string) (Optioneel)_: Relaikanaaladres in formaat `<subnet ID>.<device ID>.<channel>`. Wordt gebruikt als externe relaisstatus-terugkoppeling voor HVAC-actie.
  + **object_id** _(string) (Optioneel)_: Object_id van apparaat. De standaardwaarde wordt automatisch gegenereerd op basis van de apparaatnaam.
  + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.
  + **preset_modes** _(list) (Optioneel)_: Lijst met ondersteunde vooraf ingestelde modi. De selectie van de vooraf ingestelde modus is uitgeschakeld als deze niet is ingesteld. Mogelijke waarden worden weergegeven in onderstaande tabel. De overeenkomstige modi moeten zijn ingeschakeld in HDL (Vloerverwarming > Werkinstellingen > Modus).
  + **channel** _(int) (Optioneel)_: Kanaal vloerverwarmingsmodule (`1..6`) voor `floor_heat_device_type: module`.
  + **min_temp** _(float) (Optioneel)_: Minimale doeltemperatuur die in de Home Assistant-interface wordt getoond.
  + **max_temp** _(float) (Optioneel)_: Maximale doeltemperatuur die in de Home Assistant-interface wordt getoond.
  + **precision** _(float) (Optioneel)_: Stapgrootte voor de doeltemperatuur in de Home Assistant-interface. Toegestane waarden: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Coverplatform

Om je Buspro-covers in je installatie te gebruiken, voeg je het volgende toe aan je `configuration.yaml`-bestand:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Vereist)_: Toewijzing van Buspro-gordijnkanalen
  + **sleutel** _(string)_: `<subnet-ID>.<device-ID>.<kanaal>`
  + **name** _(string) (Vereist)_: Weergavenaam
  + **invert** _(bool) (Optioneel)_: Draait open/sluit-richting om. Standaard `false`.
  + **object_id** _(string) (Optioneel)_: Entity-`object_id`. Standaard automatisch gegenereerd op basis van naam.
  + **unique_id** _(string) (Optioneel)_: Stabiele unieke entity-id voor het Home Assistant entiteitenregister.

Ondersteunde functies:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Migratieopmerkingen

Als je upgrade vanaf een oudere versie van deze integratie, controleer dan het volgende:

- **Climate breaking changes v1.7.1 -> v2.0.0**
  - Het climate-model is opgesplitst:
    - `type: ac` maakt nu AC-climategedrag aan.
    - `type: floor_heating` maakt nu vloerverwarmingsgedrag aan.
    - Als `type` ontbreekt, is de standaard `floor_heating`.
  - Nieuwe typering voor vloerverwarming:
    - `floor_heating_device_type: dlp | module` is toegevoegd.
    - Als `channel` is ingesteld en `floor_heating_device_type` ontbreekt, wordt het type automatisch `module`.
    - Voor `floor_heating_device_type: module` is `channel` (`1..6`) verplicht, anders wordt de entiteit niet aangemaakt.
  - HVAC-modusgedrag is gewijzigd:
    - AC-entiteiten bieden `COOL/OFF`.
    - Vloerverwarmingsentiteiten bieden `HEAT/OFF` (`COOL` is extra beschikbaar voor `module`).
  - Vereiste actie:
    - Stel `type` expliciet in per climate-entiteit.
    - Voeg `floor_heating_device_type` en `channel` toe voor vloerverwarmingsmodules.
    - Controleer automatiseringen/scripts die uitgaan van oude climate-modussemantiek.

---

#### Ventilatorplatform

Om je Buspro-ventilator te gebruiken, voeg dit toe aan `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Slaapkamer Ventilator
        dimmable: true
      1.89.4:
        name: Badkamer Ventilator
        dimmable: false
```
+ **running_time** _(int) (Optioneel)_: Standaard looptijd in seconden.
+ **ack_retry_enabled** _(boolean) (Optioneel)_: Eenmalige retry zonder ACK na 0,8s.
+ **devices** _(Verplicht)_: Lijst apparaten in formaat `<subnet>.<device>.<channel>`.


---
## Diensten

#### Een willekeurig bericht verzenden:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Een scène activeren:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Een universele schakelaar instellen:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
