# Dual-Mode YAML Configuration

[🇧🇾 Беларуская](../be/DUAL_MODE_YAML.md) | [🇩🇪 Deutsch](../de/DUAL_MODE_YAML.md) | 🇬🇧 English | [🇪🇸 Español](../es/DUAL_MODE_YAML.md) | [🇫🇷 Français](../fr/DUAL_MODE_YAML.md) | [🇮🇹 Italiano](../it/DUAL_MODE_YAML.md) | [🇳🇱 Nederlands](../nl/DUAL_MODE_YAML.md) | [🇳🇴 Norsk](../no/DUAL_MODE_YAML.md) | [🇷🇺 Русский](../ru/DUAL_MODE_YAML.md) | [🇺🇦 Українська](../uk/DUAL_MODE_YAML.md)

---

The buspro custom component supports two complementary YAML configuration approaches:

1. **Entity-Centric** (Legacy) - Individual entity definitions
2. **Device-Centric** (Modern) - Complete device definitions with all channels

You can use **either approach or both simultaneously** in your Home Assistant configuration.

## Entity-Centric Format (Legacy)

Define entities individually. Useful for organizing entities by domain (lights, switches, sensors).

### Characteristics

- One entity per YAML entry
- Focus on specific sensor types or outputs
- Automatic device grouping by address prefix
- Suited for individual entity organization

### Example

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
        - type: humidity
          name: "Kitchen Humidity"
          object_id: "hdl_sensor_humidity_kitchen_ceiling"
```

### File Organization

```
entities/
├── buspro_devices/
│   └── kitchen/
│       └── multisensor_2_10.yaml    # Entity-centric device config
```

## Device-Centric Format (Modern)

Define complete devices with all their channels/entities. Useful for managing all aspects of a device in one place.

### Characteristics

- One device = one YAML file
- All channels defined together
- Clear device grouping and structure
- Suited for comprehensive device management
- Maps directly to buspro device registry

### Example

```yaml
buspro:
  host: 192.168.1.100
  port: 6000
  client_address: 1.1
  devices:
    # Relay device with 6 channels
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
        - number: 3
          name: "Spare"
          enabled: false

    # Dimmer device with 6 channels
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

### File Organization

```
entities/
├── switches/
│   ├── light/
│   │   ├── guestroom/
│   │   │   ├── switch_light_guestroom_bra_window.yaml  # Device-centric
│   │   │   └── switch_light_guestroom_bra_door.yaml
│   │   └── bathroom/
│   │       └── switch_light_bathroom_main.yaml
```

## Device-Centric Channel Format Details

### Required Fields

```yaml
address: "2.5"                    # Device address (subnet.device)
name: "Device Name"               # Human-readable device name
model: "HDL-MD0606.32"           # Device model from catalog
device_type: "relay|dimmer|..."  # Entity type
channels:                         # List of channels/entities
  - number: 1                     # Channel number (1-N) or capability name
    name: "Channel Name"          # Channel display name
    enabled: true                 # Whether to create entity (default: true)
```

### Optional Fields

```yaml
channels:
  - number: 1
    name: "Channel Name"
    enabled: true
    object_id: "hdl_switch_light_guestroom_bra_window"  # Entity ID suffix
    unique_id: "buspro-2.5-relay-1"                     # Unique identifier
```

## Supported Device Types

**Lighting:**
- `relay` - Simple on/off switches
- `dimmer` - Dimmable lights (0-255 brightness control)

**Sensors & Input:**
- `dry_contact` - Binary sensors (door/window contacts)
- `multisensor` - Compound environmental sensors
- `universal_switch` - Universal switch inputs with day/night logic

**Climate & HVAC:**
- `floor_heating` - Floor heating/temperature control modules
- `ac` - Air conditioning controllers

**Motorized:**
- `cover` - Blinds/shutter motors with position control
- `fan` - Fan speed controllers

## Mixing Both Approaches

You can use both formats simultaneously, as long as they don't conflict:

```yaml
buspro:
  devices:
    # Entity-centric: multi-sensor
    - address: "2.10"
      name: "Kitchen Sensor"
      model: "HDL-MSP02.4C"
      profile: "12in1"
      entities:
        - type: temperature
          name: "Kitchen Temperature"
          object_id: "hdl_sensor_temp_air_kitchen_ceiling"

    # Device-centric: relay with channels
    - address: "2.4"
      name: "Bathroom Relay"
      model: "HDL-MD0606.32"
      device_type: "relay"
      channels:
        - number: 1
          name: "Main Light"
          object_id: "hdl_switch_light_bathroom_main"
```

**Important:** Each address can only be defined once. Don't use the same address in both entity-centric and device-centric formats.

## Device Registry Grouping

Both formats automatically group entities under their parent device in Home Assistant's device registry:

- Devices are identified by **base address** (e.g., `2.5`)
- All entities with addresses `2.5.1`, `2.5.2`, ... are grouped under device `2.5`
- Device properties (name, model, manufacturer) apply to all entities

### Example Device Registry Hierarchy

```
Device: Guestroom Relay (2.5)
├── Entity: Bra Okno (2.5.1) [dimmer/switch]
└── Entity: Bra Dver (2.5.2) [dimmer/switch]

Device: Bathroom Relay (2.4)
├── Entity: Main Light (2.4.1) [relay/switch]
└── Entity: Exhaust Fan (2.4.2) [relay/switch]
```

## Best Practices

### For Entity-Centric:
- Organize files by domain (`entities/sensors/`, `entities/lights/`)
- One entity per file
- Use descriptive filenames
- Suited for sensor-heavy configurations

### For Device-Centric:
- Organize files by room or device group
- All channels in one file
- Use consistent naming across channels
- Suited for organized device management

### For Both:
- Don't duplicate addresses across formats
- Use the format that matches your workflow
- Consider your team's preferences
- Document your choice in CLAUDE.md or README
