# HDL Buspro

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)

## Languages

[![English](https://flagcdn.com/24x18/gb.png) English](README.md) |
[![Deutsch](https://flagcdn.com/24x18/de.png) Deutsch](README.de.md) |
[![Français](https://flagcdn.com/24x18/fr.png) Français](README.fr.md) |
[![Nederlands](https://flagcdn.com/24x18/nl.png) Nederlands](README.nl.md) |
[![Español](https://flagcdn.com/24x18/es.png) Español](README.es.md) |
[![Italiano](https://flagcdn.com/24x18/it.png) Italiano](README.it.md) |
[![Русский](https://flagcdn.com/24x18/ru.png) Русский](README.ru.md) |
[![Українська](https://flagcdn.com/24x18/ua.png) Українська](README.uk.md) |
[![Беларуская](https://flagcdn.com/24x18/by.png) Беларуская](README.be.md)

# The HDL Buspro integration allows you to control your HDL Buspro system from Home Assistant.

## Installation

### One-click install (HACS)

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Frequencies&repository=home_assistant_buspro&category=integration)

### Manual installation

Under HACS -> Integrations, add custom repository "https://github.com/Frequencies/home_assistant_buspro" with Category "Integration". Select the integration named "HDL Buspro" and download it.

Restart Home Assistant.

Go to Settings > Integrations and Add Integration "HDL Buspro". Type in IP address and port number of the gateway.

## Configuration

#### Light platform
   
To use your Buspro light in your installation, add the following to your configuration.yaml file: 

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
+ **running_time** _(int) (Optional)_: Default running time in seconds for all devices. Running time is 0 seconds if not set.
+ **ack_retry_enabled** _(boolean) (Optional)_: Enables one-time command retry when no ACK is received within 0.8s. Default is `True`.
+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on the format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device
    + **running_time** _(int) (Optional)_: The running time in seconds for the device. If omitted, the default running time for all devices is used.
    + **ack_retry_enabled** _(boolean) (Optional)_: Per-device override for ACK retry.
    + **dimmable** _(boolean) (Optional)_: Is the device dimmable? Default is True. 
    + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name. 
    + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.

#### Switch platform

To use your Buspro switch in your installation, add the following to your configuration.yaml file: 

```yaml
switch:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Switch
      1.89.2:
        name: Front Door Switch
```
+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on the format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device
    + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name. 
    + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.

#### Sensor platform

To use your Buspro sensor in your installation, add the following to your configuration.yaml file: 

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
+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`
  + **name** _(string) (Required)_: The name of the device
  + **type** _(string) (Required)_: Type of sensor to monitor. 
    + Available sensors: 
     + temperature
     + illuminance
     + humidity
  + **unit_of_measurement** _(string) (Optional)_: text to be displayed as unit of measurement
  + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name. 
  + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.
  + **device_class** _(string) (Optional)_: Valid HASS sensor device class (e.g., "temperature"). If omitted, a default is selected from sensor type.
  + **scan_interval** _(int) (Optional)_: Polling interval in seconds. If omitted or `0`, updates rely on Buspro messages.
  (https://www.home-assistant.io/components/sensor/)
  + **device** _(string) (Optional)_: The type of sensor device:
    + dlp 

#### Binary sensor platform

To use your Buspro binary sensor in your installation, add the following to your configuration.yaml file: 

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
+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`. If 
  'type' = 'universal_switch' universal switch number must be appended to the address. 
  + **name** _(string) (Required)_: The name of the device
  + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name. 
  + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.
  + **type** _(string) (Required)_: Type of sensor to monitor. 
    + Available sensors: 
      + motion 
      + dry_contact_1 
      + dry_contact_2
      + universal_switch
      + single_channel
      + dry_contact
    + Address format notes:
      + `motion`, `dry_contact_1`, `dry_contact_2`: `<subnet ID>.<device ID>`
      + `universal_switch`, `single_channel`, `dry_contact`: `<subnet ID>.<device ID>.<number>`
  + **device_class** _(string) (Optional)_: Valid HASS binary sensor device class (e.g., "motion"). If omitted, no device class is forced.
  + **scan_interval** _(int) (Optional)_: Polling interval in seconds. If omitted or `0`, updates rely on Buspro messages.
  (https://www.home-assistant.io/components/binary_sensor/)

#### Climate platform

To use your Buspro panel climate control in your installation, add the following to your configuration.yaml file: 

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
+ **devices** _(Required)_: A list of devices to set up
  + **address** _(string) (Required)_: The address of the sensor device on the format `<subnet ID>.<device ID>`
  + **name** _(string) (Required)_: The name of the device
  + **type** _(string) (Optional)_: `ac` or `floor_heating`. Default is `floor_heating`.
  + **floor_heating_device_type** _(string) (Optional)_: `dlp` or `module`.
    If omitted, `module` is auto-selected when `channel` is provided, otherwise `dlp`.
  + **relay_address** _(string) (Optional)_: Relay channel address in format `<subnet ID>.<device ID>.<channel>`. Used as external relay-state feedback for HVAC action.
  + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name. 
  + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.
  + **preset_modes** _(list) (Optional)_: List of supported preset modes. Preset mode selection is disabled if not set. Possible values are shown in table below. Corresponding modes must be enabled in HDL (Floor Heating > Working Settings > Mode).
  + **channel** _(int) (Optional)_: Floor heating module channel (`1..6`) for `floor_heating_device_type: module`.
  + **min_temp** _(float) (Optional)_: Minimum target temperature shown in Home Assistant UI.
  + **max_temp** _(float) (Optional)_: Maximum target temperature shown in Home Assistant UI.
  + **precision** _(float) (Optional)_: Target temperature step in Home Assistant UI. Allowed values: `1`, `0.5`, `0.1`.
    
| HA preset mode | HDL mode |
|:--------------:|:--------:|
|      none      |  Normal  |
|      away      |   Away   |
|      home      |   Day    |
|     sleep      |  Night   |


#### Cover platform

To use your Buspro covers in your installation, add the following to your configuration.yaml file:

```yaml
cover:
  - platform: buspro
    devices:
      1.89.1:
        name: Living Room Curtain
        invert: false
        object_id: living_room_curtain
```
+ **devices** _(Required)_: Mapping of Buspro curtain channels
  + **key** _(string)_: `<subnet ID>.<device ID>.<channel>`
  + **name** _(string) (Required)_: Friendly name
  + **invert** _(bool) (Optional)_: Invert open/close direction. Default `false`.
  + **object_id** _(string) (Optional)_: Entity object_id. Default is auto-generated from name.
  + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.

Supported features:
- open
- close
- stop
- open_tilt
- close_tilt
- stop_tilt

#### Fan platform

To use your Buspro fan in your installation, add the following to your configuration.yaml file:

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
+ **running_time** _(int) (Optional)_: Default running time in seconds for all devices. Running time is `0` if not set.
+ **ack_retry_enabled** _(boolean) (Optional)_: Enables one-time command retry when no ACK is received within 0.8s. Default is `True`.
+ **devices** _(Required)_: A list of devices to set up
  + **X.X.X** _(Required)_: The address of the device on format `<subnet ID>.<device ID>.<channel number>`
    + **name** _(string) (Required)_: The name of the device
    + **running_time** _(int) (Optional)_: Per-device running time in seconds. If omitted, platform default is used.
    + **ack_retry_enabled** _(boolean) (Optional)_: Per-device override for ACK retry.
    + **dimmable** _(boolean) (Optional)_: Whether fan speed is controllable (percentage mode). Default is `True`.
    + **object_id** _(string) (Optional)_: Device object_id. Default is auto-generated from device name.
    + **unique_id** _(string) (Optional)_: Stable entity unique_id for Home Assistant entity registry.

---
## Migration notes

If you are upgrading from an earlier version of this integration, check the following:

- **v1.7.1 -> v2.0.0 climate breaking changes**
  - Climate model was split:
    - `type: ac` now creates AC climate behavior.
    - `type: floor_heating` now creates floor-heating behavior.
    - If `type` is omitted, default is `floor_heating`.
  - New floor-heating device typing:
    - `floor_heating_device_type: dlp | module` was introduced.
    - If `channel` is provided and `floor_heating_device_type` is omitted, device type auto-switches to `module`.
    - For `floor_heating_device_type: module`, `channel` is required (`1..6`), otherwise entity setup is skipped.
  - HVAC mode behavior changed:
    - AC entities expose `COOL/OFF`.
    - Floor-heating entities expose `HEAT/OFF` (`COOL` is additionally available for module type).
  - Action required:
    - Explicitly set `type` for each climate entity during migration.
    - Add `floor_heating_device_type` and `channel` for floor-heating module devices.
    - Re-check automations/scripts that assumed old climate mode semantics.

- Entity domain correction:
  - Switch entities now use `switch.*` IDs (previously some were created as `light.*`).
  - Sensor entities now use `sensor.*` IDs (previously some were created as `light.*`).
  - Binary sensor entities now use `binary_sensor.*` IDs (previously some were created as `light.*`).
- Update dashboards, automations, scripts, and helpers that referenced old entity IDs.
- `sensor` and `binary_sensor` now validate:
  - `scan_interval` as positive integer seconds (`0` keeps message-driven updates).
  - `device_class` as a valid Home Assistant class (invalid values are ignored for binary sensors).

---
## Services

#### Sending an arbitrary message:
```
Domain: buspro
Service: send_message
Service Data: {"address": [1,74], "operate_code": [4,78], "payload": [1,100,0,3]}
```
#### Activating a scene:
```
Domain: buspro
Service: activate_scene
Service Data: {"address": [1,74], "scene_address": [3,5]}
```
#### Setting an universal switch:
```
Domain: buspro
Service: set_universal_switch
Service Data: {"address": [1,74], "switch_number": 100, "status": 1}
```
