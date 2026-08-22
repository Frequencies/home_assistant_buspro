# HDL Buspro for Home Assistant

**Documentation:** English | [Беларуская](docs/README.be.md) |
[Deutsch](docs/README.de.md) | [Español](docs/README.es.md) |
[Français](docs/README.fr.md) | [Italiano](docs/README.it.md) |
[Nederlands](docs/README.nl.md) | [Norsk](docs/README.no.md) |
[Русский](docs/README.ru.md) | [Українська](docs/README.uk.md)

Local Home Assistant integration for HDL Buspro gateways and devices. The
integration supports config-entry gateway management, model-driven physical
devices, grouped entities, read-only diagnostics, and Buspro control services.

## Installation

### HACS (recommended)

1. Open **HACS > Integrations**.
2. Open the three-dot menu and select **Custom repositories**.
3. Add `https://github.com/Frequencies/home_assistant_buspro` with category
   **Integration**.
4. Search for **HDL Buspro**, open it, and select **Download**.
5. Restart Home Assistant when HACS requests it.

Future releases can then be installed from **HACS > Integrations**. Restart
Home Assistant after each integration update.

### Manual installation

1. Download the integration repository.
2. Copy its `custom_components/buspro` directory to
   `/config/custom_components/buspro` in Home Assistant.
3. Restart Home Assistant.

## First setup

1. Open **Settings > Devices & services > Add integration** and select
   **HDL Buspro**.
2. Enter the gateway host and UDP ports. Port `6000` is the normal default.
3. Enter an unused Home Assistant Buspro address in `subnet.device` format.
   The default is `200.200`; it must not belong to another Buspro device.
4. Open **Configure > Add device**, select the device type and exact model,
   then enter its physical Buspro address and a display name.
5. Name each required channel or capability. Leave a name empty to keep that
   channel disabled and prevent its entity from being instantiated.

Known models use the fixed channel count or capability list in the device
catalog. Generic profiles ask for a channel count within the supported limit.
After saving, Home Assistant reloads the config entry and groups the generated
entities under one physical device.

To change an existing device, open **Configure > Edit device**. UI-managed
devices support model, name, channel, and removal changes. Legacy YAML devices
can expose registry naming controls, but their protocol configuration must
still be changed in YAML. Restart Home Assistant after changing YAML.

## Breaking changes in 2.2.0

Read this section before upgrading from 2.1.x.

> [!WARNING]
> This release changes device ownership, channel creation, panel event
> semantics, and the embedded Python constructor. Complete the upgrade
> checklist before removing legacy YAML.

1. **Installation-specific devices are no longer built into the integration.**
   Device addresses, names, channel assignments, and device counts now belong
   to config-entry options or the Home Assistant Device Registry. The device
   catalog contains hardware capabilities only.

2. **UI-managed relay modules use their physical channel count.**
   `HDL-MR1210.433` always exposes 12 channel slots and
   `HDL-MR1610.433` always exposes 16. An existing device cannot be reduced
   below its model's physical channel count.

3. **An empty channel name disables the channel.**
   Disabled channels are not instantiated, do not create protocol objects, and
   are marked disabled by the integration in the Entity Registry. Entering a
   name enables the channel again.

4. **The exact model controls generated entities.**
   A generic `HDL panel` has no known button count. Select the physical model
   to create button events. Changing a model reloads the config entry.

5. **Home Assistant has its own Buspro address.**
   Existing config entries migrate to `200.200`. This address must be unused on
   the Buspro network and can be changed under **Configure > Gateway settings**.

6. **Packet source IP is no longer hardcoded.**
   The integration derives it from the route to the configured gateway. A
   multi-interface Home Assistant host must route the gateway through the
   intended LAN interface.

7. **Panel action events are now decoded.**
   Automations consuming old raw action values should be checked. Events use
   `channel_on`, `channel_off`, `channel_level`, `scene`,
   `universal_switch_on`, or `universal_switch_off`, with target and summary
   attributes where they can be resolved.

8. **The embedded Python API changed.**
   Direct `pybuspro.Buspro` users must provide `client_address`; see
   [pybuspro/README.md](pybuspro/README.md).

The integration still reads legacy YAML entities during migration. Do not keep
the same physical channel in both YAML and UI-managed configuration, because
that can create duplicate entities and duplicate protocol subscriptions.

## Upgrade checklist

1. Restart Home Assistant after replacing the custom component.
2. Open **Settings > Devices & services > HDL Buspro > Configure**.
3. Check the gateway host, ports, and unused Home Assistant Buspro address.
4. Open each physical device and select its exact model.
5. Check every relay channel name. Empty channels intentionally remain disabled.
6. Verify automations that consume panel action events.
7. Remove or comment migrated YAML entities only after their UI-managed
   replacements have retained the expected entity IDs.

## Gateway setup

Add **HDL Buspro** from **Settings > Devices & services** and configure:

- **Host**: HDL IP gateway host name or IPv4 address.
- **Port**: primary UDP port, normally `6000`.
- **UDP send/receive ports**: only change these for a nonstandard gateway.
- **Home Assistant Buspro address**: an unused `subnet.device` identity, such
  as the migration default `200.200`.

UDP has no connection handshake. Setup validates address resolution, routing,
and creation of the local receive socket without assuming that a device exists
at a hardcoded Buspro address.

## Device management

Open **Configure** on the integration and choose:

- **Gateway settings** to update network settings and client identity.
- **Add device** to select a device type, model, Buspro address, and channel or
  capability names.
- **Edit device** to rename channels, enable or disable channels, remove a
  UI-managed device, or correct the model of an existing registry device.

Physical addresses are shown in Home Assistant as the device serial number.
Entities belonging to one physical module are attached to the same Device
Registry entry.

## Supported models

| Model | Home Assistant support |
| --- | --- |
| `HDL-MBUS01IP.431` | Gateway device metadata |
| `HDL-MCLog.431` | Connectivity, firmware query, last seen, logic events |
| `HDL-MR0410.431` | 4 relay channels |
| `HDL-MR0810.432` | 8 relay channels |
| `HDL-MR1210.433` | 12 relay channels |
| `HDL-MR1610.433` | 16 relay channels |
| `HDL-MR0416.431` | 4 high-power relay channels |
| `HDL-MR0416C.431` | 4 high-power relay channels |
| `HDL-MR0416D.431` | 4 high-power relay channels |
| `HDL-MR0816.432` | 8 high-power relay channels |
| `HDL-MR0816C.232` | 8 high-power relay channels |
| `HDL-MR0816D.432` | 8 high-power relay channels |
| `HDL-MR1216.433` | 12 high-power relay channels |
| `HDL-MR1616.434` | 16 high-power relay channels |
| `HDL-MR1216D.433` | 12 high-power relay channels |
| `HDL-MR0420C.431`, `HDL-MR0820C.432`, `HDL-MR1220C.433` | 4/8/12 high-current relay channels |
| `HDL-MD0206.432` | 2 dimmer channels |
| `HDL-MD0403.432` | 4 dimmer channels |
| `HDL-MD0602.432` | 6 dimmer channels |
| `HDL-MDT0203.433` | 2 trailing-edge dimmer channels |
| `HDL-MDT0203.532` | 2 trailing-edge dimmer channels |
| `HDL-MDT04015.433` | 4 trailing-edge dimmer channels |
| `HDL-MDT04015.532` | 4 trailing-edge dimmer channels |
| `HDL-MDT06015.433` | 6 trailing-edge dimmer channels |
| `HDL-MDT06015.533` | 6 trailing-edge dimmer channels |
| `HDL-MDLED0605.432` | 6 dimmer channels and diagnostics |
| `HDL-MRDA0610.432` | 6 ballast-control dimmer channels |
| `HDL-MRDA0610.433` | 6 ballast-control dimmer channels |
| `SB-DN-DALI64` | Up to 64 DALI channels |
| `HDL-MS04.432` | 4 dry-contact channels |
| `HDL-MS24.232` | 24 dry-contact channels |
| `HDL-MSP02.4C` | Temperature, illuminance, motion |
| `HDL-MSP07M.4C` | Temperature, illuminance, humidity, motion, two contacts |
| `HDL-MS08M.4C` | Temperature, illuminance, motion |
| `HDL-MS12M.4C` | Temperature, illuminance, humidity, motion, two contacts |
| `HDL-MPTL3C.48`, `HDL-MPTL4C.48` | Temperature and panel actions |
| `HDL-MPTL4.460` | Temperature and panel actions |
| `HDL-MP4S/TILE.48` | Temperature, four button events, panel actions |
| `HDL-MP2B/TILE.48` | Temperature, two button events, panel actions |
| `HDL-MP4B-A/TILE.48` | Temperature, four button events, panel actions |
| `HDL-MP4B/TILE.48` | Temperature, four button events, panel actions |
| `HDL-MP2B.480` | Temperature, two button events, panel actions |
| `HDL-MP4B.480` | Temperature, four button events, panel actions |
| `HDL-MPL8.431` | Temperature, eight button events, panel actions |
| `HDL-M/PT4.1` | Temperature, four button events, panel actions |
| `HDL-MFH04.432` | 4 floor-heating channels |
| `HDL-MFH06.432` | 6 floor-heating channels |
| `HDL-M/HVAC8.1` | AC climate entities |
| `HDL-MPED4.431` | AC climate entities |
| `HDL-MW02.431` | 2 curtain / cover channels |
| `HDL-MWM45.431` | Curtain / cover entities (configurable channels) |

Generic AC, curtain, variable-speed fan, on/off fan, universal-switch, and
panel profiles are also available. Their physical address and any configurable
output count are provided by the user; they are not installation inventory.

Some models are added via family mapping or generic protocol compatibility.
During integration startup, Buspro logs explicit model-support notes for those
models (for example, model-validated vs. family-mapped behavior) together with
detected physical addresses.

For legacy YAML devices, the integration now normalizes missing profiles using
catalog model metadata. Unknown models and unsupported profile strings are
reported as startup warnings, then fall back to generic `sensor_status`
behavior to keep the setup functional.

## Catalog maintenance helper

To compare the integration catalog with the maintained official HDL model list,
run:

```bash
python3 custom_components/buspro/tools/check_catalog_models.py
```

The helper reads `custom_components/buspro/devices/official_models.json` and
prints:

- official models missing in `DEVICE_CATALOG`
- catalog models not present in the official list
- virtual integration-only generic models

Use strict mode for CI-style checks (non-zero exit when official models are
missing in the catalog):

```bash
python3 custom_components/buspro/tools/check_catalog_models.py --strict
```

## Entity behavior

### Relays

One shared coordinator queries relay status once per physical module and
distributes the response to all enabled channel entities. Disabled channels do
not subscribe to or query the bus.

### Panels

Known button panels create one `event` entity per physical button, an `Action`
event, and a `Last action` sensor. UI button event entities represent received
physical Buspro button telegrams; they do not simulate a hardware press.

### Dimmers

Supported dimmers can expose connectivity, per-channel maximum brightness,
load type, and protocol-reported minimum brightness. `Not reported` means the
device returned the protocol sentinel rather than a usable value.

### Logic controller

`HDL-MCLog.431` exposes read-only connectivity, firmware version, last seen,
and logic event entities. Some firmware does not answer the standard firmware
query; in that case the firmware entity remains unavailable. Logic blocks are
not writable because changing them can overwrite controller programming.

## Services

- `buspro.activate_scene`
- `buspro.set_universal_switch`
- `buspro.send_message`

`buspro.send_message` sends a raw protocol command and should only be used with
a verified HDL operation code and payload.

## Legacy YAML

Legacy platform entities and top-level compound sensor definitions remain
supported as a migration path. A config entry can own the gateway while YAML
describes legacy entities. New physical devices should be configured from the
integration's UI so model capabilities, Device Registry grouping, channel
state, and edits remain consistent.

## Development

Run the focused regression suite from the Home Assistant configuration root:

```bash
python3 custom_components/buspro/tests/buspro_protocol/test_sensor_protocol.py
python3 custom_components/buspro/tests/buspro_protocol/test_relay_coordinator.py
python3 custom_components/buspro/tests/buspro_protocol/test_logic_controller_protocol.py
python3 custom_components/buspro/tests/buspro_protocol/test_config_isolation.py
python3 custom_components/buspro/tests/buspro_integration/test_device_catalog.py
python3 custom_components/buspro/tests/buspro_integration/test_managed_device_logic.py
python3 custom_components/buspro/tests/buspro_integration/test_model_notes_logging.py
python3 custom_components/buspro/tests/buspro_integration/test_yaml_normalization.py
```
