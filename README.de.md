# HDL Buspro
## Sprachen

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

Mit der HDL Buspro-Integration können Sie Ihr HDL Buspro-System über Home Assistant steuern.

## Installation
Fügen Sie unter HACS -> Integrationen das benutzerdefinierte Repository "https://github.com/Frequencies/home_assistant_buspro" mit der Kategorie "Integration" hinzu. Wählen Sie die Integration mit dem Namen "HDL Buspro" aus und laden Sie sie herunter.

Starten Sie Home Assistant neu.

Gehen Sie zu Einstellungen > Integrationen und fügen Sie die Integration „HDL Buspro“ hinzu. Geben Sie die IP-Adresse und die Portnummer des Gateways ein.

## Konfiguration

#### Leichte Plattform
   
Um Ihre Buspro-Leuchte in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer Datei „configuration.yaml“ hinzu:

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
+ **running_time** _(int) (Optional)_: Standardlaufzeit in Sekunden für alle Geräte. Die Laufzeit beträgt 0 Sekunden, wenn nicht eingestellt.
+ **ack_retry_enabled** _(boolean) (Optional)_: Aktiviert einen einmaligen Befehls-Retry, wenn innerhalb von 0,8 s kein ACK empfangen wird. Standard ist `True`.
+ **Geräte** _(Erforderlich)_: Eine Liste der einzurichtenden Geräte
  + **X.X.X** _(Erforderlich)_: Die Adresse des Geräts im Format „<Subnetz-ID>.<Geräte-ID>.<Kanalnummer>“.
    + **Name** _(string) (Erforderlich)_: Der Name des Geräts
    + **running_time** _(int) (Optional)_: Die Laufzeit in Sekunden für das Gerät. Wenn es weggelassen wird, wird die Standardlaufzeit für alle Geräte verwendet.
    + **ack_retry_enabled** _(boolean) (Optional)_: Geräte-spezifische Überschreibung für ACK-Retry.
    + **dimmbar** _(boolean) (Optional)_: Ist das Gerät dimmbar? Der Standardwert ist True.
    + **object_id** _(string) (Optional)_: Geräteobjekt_id. Die Standardeinstellung wird automatisch aus dem Gerätenamen generiert.
    + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.

#### Plattform wechseln

Um Ihren Buspro-Switch in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer Datei „configuration.yaml“ hinzu:

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **Geräte** _(Erforderlich)_: Eine Liste der einzurichtenden Geräte
  + **X.X.X** _(Erforderlich)_: Die Adresse des Geräts im Format „<Subnetz-ID>.<Geräte-ID>.<Kanalnummer>“.
    + **Name** _(string) (Erforderlich)_: Der Name des Geräts
    + **object_id** _(string) (Optional)_: Geräteobjekt_id. Die Standardeinstellung wird automatisch aus dem Gerätenamen generiert.
    + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.

#### Sensorplattform

Um Ihren Buspro-Sensor in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer Datei „configuration.yaml“ hinzu:

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
+ **Geräte** _(Erforderlich)_: Eine Liste der einzurichtenden Geräte
  + **Adresse** _(Zeichenfolge) (Erforderlich)_: Die Adresse des Sensorgeräts im Format „<Subnetz-ID>.<Geräte-ID>“.
  + **Name** _(string) (Erforderlich)_: Der Name des Geräts
  + **Typ** _(string) (Erforderlich)_: Typ des zu überwachenden Sensors.
    + Verfügbare Sensoren:
     + Temperatur
     + Beleuchtungsstärke
     + Luftfeuchtigkeit
  + **unit_of_measurement** _(string) (Optional)_: Text, der als Maßeinheit angezeigt werden soll
  + **object_id** _(string) (Optional)_: Geräteobjekt_id. Die Standardeinstellung wird automatisch aus dem Gerätenamen generiert.
  + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.
  + **device_class** _(string) (Optional)_: HASS-Geräteklasse, z. B. „temperature“
(https://www.home-assistant.io/components/sensor/)
  + **Gerät** _(string) (Optional)_: Der Typ des Sensorgeräts:
    + dlp

#### Binäre Sensorplattform

Um Ihren Buspro-Binärsensor in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer Datei „configuration.yaml“ hinzu:

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
+ **Geräte** _(Erforderlich)_: Eine Liste der einzurichtenden Geräte
  + **Adresse** _(Zeichenfolge) (Erforderlich)_: Die Adresse des Sensorgeräts im Format „<Subnetz-ID>.<Geräte-ID>“. Wenn
'type' = 'universal_switch' Die universelle Switch-Nummer muss an die Adresse angehängt werden.
  + **Name** _(string) (Erforderlich)_: Der Name des Geräts
  + **object_id** _(string) (Optional)_: Geräteobjekt_id. Die Standardeinstellung wird automatisch aus dem Gerätenamen generiert.
  + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.
  + **Typ** _(string) (Erforderlich)_: Typ des zu überwachenden Sensors.
    + Verfügbare Sensoren:
      + Bewegung
      + dry_contact_1
      + dry_contact_2
      + universal_switch
      + single_channel
  + **device_class** _(string) (Optional)_: HASS-Geräteklasse, z. B. „motion“
(https://www.home-assistant.io/components/binary_sensor/)

#### Klimaplattform

Um Ihre Buspro-Panel-Klimasteuerung in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer Datei „configuration.yaml“ hinzu:

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
+ **Geräte** _(Erforderlich)_: Eine Liste der einzurichtenden Geräte
  + **Adresse** _(Zeichenfolge) (Erforderlich)_: Die Adresse des Sensorgeräts im Format „<Subnetz-ID>.<Geräte-ID>“.
  + **Name** _(string) (Erforderlich)_: Der Name des Geräts
  + **Typ** _(string) (Optional)_: „ac“ oder „floor_heating“. Der Standardwert ist „floor_heating“.
  + **floor_heating_device_type** _(string) (Optional)_: „dlp“ oder „module“.
Wenn es weggelassen wird, wird „Modul“ automatisch ausgewählt, wenn „Kanal“ bereitgestellt wird, andernfalls „dlp“.
  + **object_id** _(string) (Optional)_: Geräteobjekt_id. Die Standardeinstellung wird automatisch aus dem Gerätenamen generiert.
  + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.
  + **preset_modes** _(list) (Optional)_: Liste der unterstützten voreingestellten Modi. Die Auswahl des Voreinstellungsmodus ist deaktiviert, wenn sie nicht festgelegt ist. Mögliche Werte sind in der folgenden Tabelle aufgeführt. Entsprechende Modi müssen in HDL (Fußbodenheizung > Arbeitseinstellungen > Modus) aktiviert sein.
  + **channel** _(int) (Optional)_: Fußbodenheizungsmodulkanal (`1..6`) für `floor_heating_device_type: module`.
  + **min_temp** _(float) (Optional)_: Minimale Solltemperatur, die in der Home Assistant UI angezeigt wird.
  + **max_temp** _(float) (Optional)_: Maximale Solltemperatur, die in der Home Assistant UI angezeigt wird.
  + **precision** _(float) (Optional)_: Schrittweite der Solltemperatur in der Home Assistant UI. Zulässige Werte: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Cover-Plattform

Um Ihre Buspro-Abdeckungen in Ihrer Installation zu verwenden, fügen Sie Folgendes zu Ihrer `configuration.yaml`-Datei hinzu:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Erforderlich)_: Zuordnung der Buspro-Vorhangkanäle
  + **Schlüssel** _(string)_: `<Subnetz-ID>.<Geräte-ID>.<Kanal>`
  + **name** _(string) (Erforderlich)_: Anzeigename
  + **invert** _(bool) (Optional)_: Öffnen/Schließen-Richtung umkehren. Standardwert ist `false`.
  + **object_id** _(string) (Optional)_: Entity-`object_id`. Standardmäßig automatisch aus dem Namen generiert.
  + **unique_id** _(string) (Optional)_: Stabile eindeutige Kennung der Entität für die Home Assistant-Entitätsregistrierung.

Unterstützte Funktionen:
- öffnen
- schließen
- stopp
- öffnen_tilt
- schließen_tilt
- stopp_tilt

---
## Dienstleistungen

#### Senden einer beliebigen Nachricht:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Szene aktivieren:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Universalschalter einstellen:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
