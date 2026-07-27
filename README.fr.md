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
        ack_retry_enabled: True
```
+ **running_time** _(int) (Facultatif)_ : durée d'exécution par défaut en secondes pour tous les appareils. Le temps d'exécution est de 0 seconde s'il n'est pas défini.
+ **ack_retry_enabled** _(boolean) (Optionnel)_: Active une nouvelle tentative unique si aucun ACK n'est recu sous 0,8 s. Par defaut : `True`.
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **X.X.X** _(Obligatoire)_ : L'adresse de l'appareil au format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
    + **running_time** _(int) (Facultatif)_ : la durée d'exécution en secondes de l'appareil. En cas d'omission, la durée d'exécution par défaut de tous les appareils est utilisée.
    + **ack_retry_enabled** _(boolean) (Optionnel)_: Remplacement par appareil du comportement de nouvelle tentative ACK.
    + **dimmable** _(booléen) (Facultatif)_ : L'appareil est-il dimmable ? La valeur par défaut est True.
    + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.
    + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.

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
    + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.

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
  + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.
  + **device_class** _(string) (Facultatif)_ : classe d'appareil HASS, par exemple "température"
  + **scan_interval** _(int) (Optionnel)_: Intervalle de polling en secondes. Si omis ou `0`, les mises a jour reposent uniquement sur les messages Buspro.
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
  + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.
  + **type** _(chaîne) (Obligatoire)_ : Type de capteur à surveiller.
    + Capteurs disponibles :
      + mouvement
      + sec_contact_1
      + sec_contact_2
      + commutateur_universel
      + canal_single
      + dry_contact
    + Notes sur le format d'adresse :
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(string) (Facultatif)_ : classe de périphérique HASS, par exemple "motion"
  + **scan_interval** _(int) (Optionnel)_: Intervalle de polling en secondes. Si omis ou `0`, les mises a jour reposent uniquement sur les messages Buspro.
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
        unique_id: "hdl_climate_floorheat_zone_1"
        min_temp: 22
        max_temp: 32
        precision: 1
        name: Floor Heating Zone 1
```
+ **appareils** _(obligatoire)_ : une liste d'appareils à configurer
  + **adresse** _(chaîne) (obligatoire)_ : l'adresse du capteur au format `<subnet ID>.<device ID>`
  + **name** _(string)(Obligatoire)_ : Le nom de l'appareil
  + **tapez** _(string) (Facultatif)_ : `ac` ou `floor_heating`. La valeur par défaut est « floor_heating ».
  + **floor_heating_device_type** _(string) (Facultatif)_ : `dlp` ou `module`.
S'il est omis, « module » est automatiquement sélectionné lorsque « canal » est fourni, sinon « dlp ».
  + **relay_address** _(string) (Optionnel)_: Adresse du canal relais au format `<subnet ID>.<device ID>.<channel>`. Utilisee comme retour d'etat relais externe pour l'action HVAC.
  + **object_id** _(string) (Facultatif)_ : ID_objet de l'appareil. La valeur par défaut est générée automatiquement à partir du nom de l'appareil.
  + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.
  + **preset_modes** _(list) (Facultatif)_ : Liste des modes prédéfinis pris en charge. La sélection du mode prédéfini est désactivée si elle n’est pas définie. Les valeurs possibles sont indiquées dans le tableau ci-dessous. Les modes correspondants doivent être activés dans HDL (Chauffage au sol > Paramètres de travail > Mode).
  + **canal** _(int) (Facultatif)_ : canal du module de chauffage par le sol (`1..6`) pour `floor_heating_device_type : module`.
  + **min_temp** _(float) (Facultatif)_ : Température cible minimale affichée dans l’interface Home Assistant.
  + **max_temp** _(float) (Facultatif)_ : Température cible maximale affichée dans l’interface Home Assistant.
  + **precision** _(float) (Facultatif)_ : Pas de réglage de la température cible dans l’interface Home Assistant. Valeurs autorisées : `1`, `0.5`, `0.1`.
    
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
  + **unique_id** _(string) (Facultatif)_ : Identifiant unique stable de l’entité pour le registre des entités Home Assistant.

Fonctionnalités prises en charge :
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

---
## Notes De Migration

Si vous mettez à jour depuis une version plus ancienne de cette intégration, vérifiez les points suivants:

- **Changements incompatibles climate v1.7.1 -> v2.0.0**
  - Le modèle climate a été scindé:
    - `type: ac` crée désormais un comportement climate AC.
    - `type: floor_heating` crée désormais un comportement de chauffage au sol.
    - Si `type` est omis, la valeur par défaut est `floor_heating`.
  - Nouvelle typologie chauffage au sol:
    - `floor_heating_device_type: dlp | module` a été introduit.
    - Si `channel` est renseigné et que `floor_heating_device_type` est omis, le type devient automatiquement `module`.
    - Pour `floor_heating_device_type: module`, `channel` (`1..6`) est obligatoire, sinon l'entité n'est pas créée.
  - Le comportement des modes HVAC a changé:
    - Les entités AC exposent `COOL/OFF`.
    - Les entités chauffage au sol exposent `HEAT/OFF` (`COOL` est également disponible pour `module`).
  - Action requise:
    - Définir explicitement `type` pour chaque entité climate.
    - Ajouter `floor_heating_device_type` et `channel` pour les modules de chauffage au sol.
    - Vérifier les automatisations/scripts qui supposent l'ancienne sémantique des modes climate.

---

#### Plateforme Ventilateur

Pour utiliser votre ventilateur Buspro, ajoutez ceci dans `configuration.yaml`:

```yaml
fan:
  - platform: buspro
    running_time: 3
    ack_retry_enabled: true
    devices:
      1.89.3:
        name: Ventilateur Chambre
        dimmable: true
      1.89.4:
        name: Ventilateur Salle de bain
        dimmable: false
```
+ **running_time** _(int) (Optionnel)_: Temps d'execution par defaut en secondes.
+ **ack_retry_enabled** _(boolean) (Optionnel)_: Retry unique sans ACK apres 0,8s.
+ **devices** _(Obligatoire)_: Liste d'appareils au format `<subnet>.<device>.<channel>`.


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
