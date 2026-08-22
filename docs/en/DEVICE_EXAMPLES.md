# HDL Buspro Device Configuration Examples

[English](../en/DEVICE_EXAMPLES.md) | [Русский](../ru/DEVICE_EXAMPLES.md) | [Українська](../uk/DEVICE_EXAMPLES.md) | [Беларуская](../be/DEVICE_EXAMPLES.md) | [Deutsch](../de/DEVICE_EXAMPLES.md) | [Français](../fr/DEVICE_EXAMPLES.md) | [Español](../es/DEVICE_EXAMPLES.md) | [Italiano](../it/DEVICE_EXAMPLES.md) | [Nederlands](../nl/DEVICE_EXAMPLES.md) | [Norsk](../no/DEVICE_EXAMPLES.md)

This guide provides practical UI and YAML configuration examples for all supported device types in the HDL Buspro integration.

**Table of Contents:**
- [Relay Devices](#relay-devices)
- [Dimmer Devices](#dimmer-devices)
- [Cover Devices (Blinds/Shutters)](#cover-devices)
- [Fan Devices](#fan-devices)
- [Climate Devices](#climate-devices)
- [Sensor Devices](#sensor-devices)
- [Binary Sensor Devices](#binary-sensor-devices)

---

## Relay Devices

Relay devices are simple on/off switches used for lighting, fans, and other binary loads.

**Supported Models:**
- `HDL-MR0410.431` - 4 relay channels
- `HDL-MR0810.432` - 8 relay channels
- `HDL-MR1210.433` - 12 relay channels
- `HDL-MR1610.433` - 16 relay channels
- HDL high-power relay variants (MR0416, MR0816, MR1216, MR1616, MR0420C, etc.)

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Relay**
4. Select exact model: **HDL-MR0410.431** (4 channels)
5. Enter Buspro address: `1.10`
6. Enter device name: "Living Room Lights"
7. Name the channels:
   - Channel 1: "Ceiling Light"
   - Channel 2: "Table Lamp"
   - Channel 3: "Wall Sconce"
   - Channel 4: "" (leave empty to disable)
8. Click **Save**

**Result:**
- `light.living_room_lights_ceiling_light`
- `light.living_room_lights_table_lamp`
- `light.living_room_lights_wall_sconce`

### YAML Configuration Example

**Entity-Centric (Individual files):**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.10.1":
        name: "Living Room Ceiling Light"
        object_id: "ceiling_light"
      "1.10.2":
        name: "Living Room Table Lamp"
        object_id: "table_lamp"
      "1.10.3":
        name: "Living Room Wall Sconce"
        object_id: "wall_sconce"
```

**Device-Centric (Complete device definition):**

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    - address: "1.10"
      name: "Living Room Relays"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
          object_id: "hdl_light_ceiling"
        - number: 2
          name: "Table Lamp"
          enabled: true
          object_id: "hdl_light_table"
        - number: 3
          name: "Wall Sconce"
          enabled: true
          object_id: "hdl_light_sconce"
        - number: 4
          enabled: false
```

---

## Dimmer Devices

Dimmer devices control brightness levels (0-255) for dimmable lights.

**Supported Models:**
- `HDL-MD0206.432` - 2 dimmer channels
- `HDL-MD0403.432` - 4 dimmer channels
- `HDL-MD0602.432` - 6 dimmer channels
- HDL trailing-edge dimmers (MDT0203, MDT04015, MDT06015, etc.)
- `HDL-MDLED0605.432` - 6 dimmer channels with diagnostics

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Dimmer**
4. Select exact model: **HDL-MD0602.432** (6 channels)
5. Enter Buspro address: `1.5`
6. Enter device name: "Bedroom Dimmers"
7. Name the channels:
   - Channel 1: "Main Light"
   - Channel 2: "Bedside Left"
   - Channel 3: "Bedside Right"
   - Channels 4-6: leave empty
8. Click **Save**

**Result:**
- `light.bedroom_dimmers_main_light` (dimmable 0-255)
- `light.bedroom_dimmers_bedside_left` (dimmable 0-255)
- `light.bedroom_dimmers_bedside_right` (dimmable 0-255)

### YAML Configuration Example

**Entity-Centric:**

```yaml
# configuration.yaml
light:
  - platform: buspro
    devices:
      "1.5.1":
        name: "Bedroom Main Light"
        dimmable: true
      "1.5.2":
        name: "Bedroom Bedside Left"
        dimmable: true
      "1.5.3":
        name: "Bedroom Bedside Right"
        dimmable: true
```

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
          object_id: "hdl_dimmer_main"
        - number: 2
          name: "Bedside Left"
          enabled: true
          object_id: "hdl_dimmer_left"
        - number: 3
          name: "Bedside Right"
          enabled: true
          object_id: "hdl_dimmer_right"
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false
```

---

## Cover Devices

Cover devices control motorized blinds, shutters, and curtains.

**Supported Models:**
- `HDL-MW02.431` - 2 curtain/cover channels
- `HDL-MWM45.431` - Curtain/cover entities (configurable channels)

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Cover**
4. Select exact model: **HDL-MW02.431** (2 channels)
5. Enter Buspro address: `2.10`
6. Enter device name: "Living Room Blinds"
7. Name the channels:
   - Channel 1: "Windows"
   - Channel 2: "Patio Door"
8. Click **Save**

**Result:**
- `cover.living_room_blinds_windows`
- `cover.living_room_blinds_patio_door`

### YAML Configuration Example

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.10"
      name: "Living Room Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Windows"
          enabled: true
          object_id: "hdl_cover_windows"
        - number: 2
          name: "Patio Door"
          enabled: true
          object_id: "hdl_cover_patio"
```

---

## Fan Devices

Fan devices control variable-speed fans.

**Supported Models:**
- Generic fan profile (variable-speed fans)

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Fan**
4. Select exact model: **Generic** (specify channel count)
5. Enter Buspro address: `3.5`
6. Enter device name: "Bathroom Exhaust Fan"
7. Name the channel: "Main Fan"
8. Click **Save**

**Result:**
- `fan.bathroom_exhaust_fan_main_fan` (0-255 speed control)

### YAML Configuration Example

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.5"
      name: "Bathroom Exhaust Fan"
      device_type: "fan"
      channels:
        - number: 1
          name: "Main Fan"
          enabled: true
          object_id: "hdl_fan_exhaust"
```

---

## Climate Devices

Climate devices control temperature and HVAC systems.

**Supported Models:**
- `HDL-MFH04.432` - 4 floor heating channels
- `HDL-MFH06.432` - 6 floor heating channels
- `HDL-M/HVAC8.1` - AC climate control
- `HDL-MPED4.431` - AC climate control
- Generic AC profile
- Generic floor heating profile

### UI Configuration Example - AC Unit

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Climate**
4. Select exact model: **HDL-M/HVAC8.1** (AC)
5. Enter Buspro address: `3.1`
6. Enter device name: "Living Room AC"
7. Click **Save**

**Result:**
- `climate.living_room_ac` (target temp, mode, power control)

### YAML Configuration Example

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "3.1"
      name: "Living Room AC"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"
      object_id: "hdl_climate_ac"

    - address: "4.2"
      name: "Master Bedroom Floor Heating"
      model: "HDL-MFH06.432"
      device_type: "floor_heating"
      channels:
        - number: 1
          name: "Zone 1"
          enabled: true
        - number: 2
          name: "Zone 2"
          enabled: true
        - number: 3
          enabled: false
```

---

## Sensor Devices

Sensor devices provide temperature, humidity, illuminance, and motion data.

**Supported Models:**
- `HDL-MSP02.4C` - Temperature, illuminance, motion
- `HDL-MSP07M.4C` - Temperature, illuminance, humidity, motion, 2 contacts
- `HDL-MS08M.4C` - Temperature, illuminance, motion
- `HDL-MS12M.4C` - Temperature, illuminance, humidity, motion, 2 contacts
- `HDL-MCLog.431` - Logic controller (read-only)
- Panel temperature sensors (MPTL, MP2B, MP4B, MPL8, etc.)

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Multisensor**
4. Select exact model: **HDL-MSP07M.4C**
5. Enter Buspro address: `2.5`
6. Enter device name: "Living Room Sensor"
7. Click **Save**

**Result:**
- `sensor.living_room_sensor_temperature`
- `sensor.living_room_sensor_illuminance`
- `sensor.living_room_sensor_humidity`
- `binary_sensor.living_room_sensor_motion`
- 2 additional dry contacts

### YAML Configuration Example

**Entity-Centric:**

```yaml
# configuration.yaml
sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: temperature
            name: "Temperature"
            object_id: "hdl_temp_living_room"
          - type: illuminance
            name: "Light Level"
            object_id: "hdl_lux_living_room"
          - type: humidity
            name: "Humidity"
            object_id: "hdl_humidity_living_room"

binary_sensor:
  - platform: buspro
    devices:
      "2.5":
        name: "Living Room Sensor"
        model: "HDL-MSP07M.4C"
        profile: "12in1"
        entities:
          - type: motion
            name: "Motion"
            object_id: "hdl_motion_living_room"
          - type: dry_contact
            number: 1
            name: "Door Contact"
            object_id: "hdl_door_living_room"
          - type: dry_contact
            number: 2
            name: "Window Contact"
            object_id: "hdl_window_living_room"
```

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
          object_id: "hdl_temp_living_room"
        - type: illuminance
          name: "Illuminance"
          object_id: "hdl_lux_living_room"
        - type: humidity
          name: "Humidity"
          object_id: "hdl_humidity_living_room"
        - type: motion
          name: "Motion"
          object_id: "hdl_motion_living_room"
        - type: dry_contact
          number: 1
          name: "Door Contact"
          object_id: "hdl_door_contact"
        - type: dry_contact
          number: 2
          name: "Window Contact"
          object_id: "hdl_window_contact"
```

---

## Binary Sensor Devices

Binary sensor devices provide on/off status from dry contacts and door/window sensors.

**Supported Models:**
- `HDL-MS04.432` - 4 dry contact channels
- `HDL-MS24.232` - 24 dry contact channels
- Multisensors with integrated contacts (MSP07M, MS12M, etc.)

### UI Configuration Example

**Steps:**
1. Go to **Settings > Devices & services > HDL Buspro > Configure**
2. Click **Add device**
3. Select device type: **Dry Contact**
4. Select exact model: **HDL-MS04.432** (4 channels)
5. Enter Buspro address: `1.20`
6. Enter device name: "Door & Window Sensors"
7. Name the channels:
   - Channel 1: "Front Door"
   - Channel 2: "Garage Door"
   - Channel 3: "Living Room Window"
   - Channel 4: leave empty
8. Click **Save**

**Result:**
- `binary_sensor.door_window_sensors_front_door`
- `binary_sensor.door_window_sensors_garage_door`
- `binary_sensor.door_window_sensors_living_room_window`

### YAML Configuration Example

**Device-Centric:**

```yaml
# configuration.yaml
buspro:
  devices:
    - address: "1.20"
      name: "Door & Window Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
          object_id: "hdl_door_front"
        - number: 2
          name: "Garage Door"
          enabled: true
          object_id: "hdl_door_garage"
        - number: 3
          name: "Living Room Window"
          enabled: true
          object_id: "hdl_window_living_room"
        - number: 4
          enabled: false
```

---

## Complex Multi-Device Example

Here's a complete configuration file showing multiple device types working together:

```yaml
# configuration.yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 200.200
  devices:
    # Relay devices
    - address: "1.10"
      name: "Living Room Lights"
      model: "HDL-MR0410.431"
      device_type: "relay"
      channels:
        - number: 1
          name: "Ceiling Light"
          enabled: true
        - number: 2
          name: "Table Lamp"
          enabled: true
        - number: 3
          name: "Wall Sconce"
          enabled: true
        - number: 4
          enabled: false

    # Dimmer devices
    - address: "1.5"
      name: "Bedroom Dimmers"
      model: "HDL-MD0602.432"
      device_type: "dimmer"
      channels:
        - number: 1
          name: "Main Light"
          enabled: true
        - number: 2
          name: "Bedside Left"
          enabled: true
        - number: 3
          name: "Bedside Right"
          enabled: true
        - number: 4
          enabled: false
        - number: 5
          enabled: false
        - number: 6
          enabled: false

    # Cover devices (blinds)
    - address: "2.10"
      name: "Blinds"
      model: "HDL-MW02.431"
      device_type: "cover"
      channels:
        - number: 1
          name: "Living Room"
          enabled: true
        - number: 2
          name: "Patio"
          enabled: true

    # Climate
    - address: "3.1"
      name: "AC Unit"
      model: "HDL-M/HVAC8.1"
      device_type: "ac"

    # Sensors
    - address: "2.5"
      name: "Living Room Sensor"
      model: "HDL-MSP07M.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Temperature"
        - type: illuminance
          name: "Illuminance"
        - type: humidity
          name: "Humidity"
        - type: motion
          name: "Motion"
        - type: dry_contact
          number: 1
          name: "Door"
        - type: dry_contact
          number: 2
          name: "Window"

    # Dry contacts
    - address: "1.20"
      name: "Door Sensors"
      model: "HDL-MS04.432"
      device_type: "dry_contact"
      channels:
        - number: 1
          name: "Front Door"
          enabled: true
        - number: 2
          name: "Garage Door"
          enabled: true
        - number: 3
          enabled: false
        - number: 4
          enabled: false
```

---

## Tips & Best Practices

1. **Use UI for simple setups** - The UI provides an intuitive way to add and manage devices without needing to write YAML.

2. **Use YAML for complex or programmatic configurations** - YAML is better for large installations or when you need version control.

3. **Address Naming** - Always use the format `subnet.device` for addresses (e.g., `1.5`, `2.10`). The `subnet` and `device` values must be valid Buspro addresses on your network.

4. **Channel Numbering** - Channels are numbered starting from 1. Leave a channel's name empty in the UI to disable it, which prevents entity creation for unused channels.

5. **Device Names** - Use descriptive, location-based names (e.g., "Living Room Lights" instead of "Relays"). This makes automations and scenes easier to understand.

6. **Object IDs** - In YAML, `object_id` is optional but recommended. It controls the entity's ID slug. If omitted, Home Assistant generates one from the channel name.

7. **Unique IDs** - For advanced cases where you need to manually control entity registry entries, use `unique_id` in YAML configuration. This allows Home Assistant to track the entity reliably even if the device name changes.

For more detailed information on YAML configuration formats, see [../en/DUAL_MODE_YAML.md](../en/DUAL_MODE_YAML.md).
