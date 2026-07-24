# HDL Buspro
## Langues

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

L'intégration HDL Buspro vous permet de contrôler votre système HDL Buspro depuis Home Assistant.

## Installation
Sous HACS -> Intégrations, ajoutez le dépôt personnalisé "https://github.com/Frequencies/home_assistant_buspro" avec la catégorie "Intégration". Sélectionnez l’intégration nommée "HDL Buspro" et téléchargez-la.

Redémarrez Home Assistant.

Accédez à Paramètres > Intégrations et ajoutez l'intégration « HDL Buspro ». Saisissez l'adresse IP et le numéro de port de la passerelle.

## Configuration

#### Plateforme légère
   
Pour utiliser votre lampe Buspro dans votre installation, ajoutez ce qui suit à votre fichier configuration.yaml :

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
```
+ **running_time** _(int) (Facultatif)_ : durée d'exécution par défaut en secondes pour tous les appareils. Le temps d'exécution est de 0 seconde s'il n'est pas défini.
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **X.X.X** _(Obligatoire)_ : L'adresse de l'appareil au format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
    + **running_time** _(int) (Facultatif)_ : la durée d'exécution en secondes de l'appareil. En cas d'omission, la durée d'exécution par défaut de tous les appareils est utilisée.
    + **dimmable** _(booléen) (Facultatif)_ : L'appareil est-il dimmable ? La valeur par défaut est True.
    + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.

#### Changer de plateforme

Pour utiliser votre commutateur Buspro dans votre installation, ajoutez ce qui suit à votre fichier configuration.yaml :

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **X.X.X** _(Obligatoire)_ : L'adresse de l'appareil au format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
    + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.

#### Plateforme de capteurs

Pour utiliser votre capteur Buspro dans votre installation, ajoutez ce qui suit à votre fichier configuration.yaml :

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
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **adresse** _(chaîne) (obligatoire)_ : l'adresse du capteur au format `<subnet ID>.<device ID>`
  + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
  + **type** _(chaîne) (Obligatoire)_ : Type de capteur à surveiller.
    + Capteurs disponibles :
     + température
     + éclairement
     + humidité
  + **unit_of_measurement** _(string) (Facultatif)_ : texte à afficher comme unité de mesure
  + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.
  + **device_class** _(string) (Facultatif)_ : classe d'appareil HASS, par exemple "température"
(https://www.home-assistant.io/components/sensor/)
  + **device** _(string) (Facultatif)_ : Le type de capteur :
    + dlp

#### Plateforme de capteurs binaires

Pour utiliser votre capteur binaire Buspro dans votre installation, ajoutez ce qui suit à votre fichier configuration.yaml :

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
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **adresse** _(chaîne) (Obligatoire)_ : L'adresse du périphérique capteur au format `<subnet ID>.<device ID>`. Si
'type' = 'universal_switch' Le numéro du commutateur universel doit être ajouté à l'adresse.
  + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
  + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.
  + **type** _(chaîne) (Obligatoire)_ : Type de capteur à surveiller.
    + Capteurs disponibles :
      + mouvement
      + sec_contact_1
      + sec_contact_2
      + commutateur_universel
      + canal_single
  + **device_class** _(string) (Facultatif)_ : classe de périphérique HASS, par exemple "motion"
(https://www.home-assistant.io/components/binary_sensor/)

#### Plateforme climatique

Pour utiliser votre panneau de climatisation Buspro dans votre installation, ajoutez ce qui suit à votre fichier configuration.yaml :

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
        name: Floor Heating Zone 1
```
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **adresse** _(chaîne) (obligatoire)_ : l'adresse du capteur au format `<subnet ID>.<device ID>`
  + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
  + **tapez** _(string) (Facultatif)_ : `ac` ou `floor_heating`. La valeur par défaut est « floor_heating ».
  + **floor_heating_device_type** _(string) (Facultatif)_ : `dlp` ou `module`.
S'il est omis, « module » est automatiquement sélectionné lorsque « canal » est fourni, sinon « dlp ».
  + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.
  + **preset_modes** _(list) (Facultatif)_ : Liste des modes prédéfinis pris en charge. La sélection du mode prédéfini est désactivée si elle n’est pas définie. Les valeurs possibles sont indiquées dans le tableau ci-dessous. Les modes correspondants doivent être activés dans HDL (Chauffage au sol > Paramètres de travail > Mode).
  + **canal** _(int) (Facultatif)_ : canal du module de chauffage par le sol (`1..6`) pour `floor_heating_device_type : module`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Plateforme des volets

Pour utiliser vos volets Buspro dans votre installation, ajoutez ce qui suit à votre fichier `configuration.yaml` :

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Obligatoire)_: Mappage des canaux de rideaux Buspro
  + **clé** _(string)_: `<ID sous-réseau>.<ID appareil>.<canal>`
  + **name** _(string) (Obligatoire)_: Nom affiché
  + **invert** _(bool) (Optionnel)_: Inverse le sens ouverture/fermeture. Valeur par défaut `false`.
  + **object_id** _(string) (Optionnel)_: `object_id` de l'entité. Généré automatiquement à partir du nom.

Fonctionnalités prises en charge :
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Services

#### Envoi d'un message arbitraire :
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Activer une scène :
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Configuration d'un interrupteur universel :
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
