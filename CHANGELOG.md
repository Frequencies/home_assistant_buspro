# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [3.5.4] - 2026-08-26

### Fixed

- Illuminance sensors now returns lx instead of lux.

## [3.5.3] - 2026-08-26

### Fixed

- Motion sensor for MSP02.4C device.

## [3.5.2] - 2026-08-26

### Fixed

- **Lux now updates in real time via the `0xE441` broadcast.** The MSP02.4C
  (and other sensors-in-one devices) automatically broadcast illuminance every
  ~60 s as opcode `0xE441` (`[?, 1, HIGH, LOW, ?, ?]`). The opcode was
  previously unmapped (`operate_code: None` in debug logs). It is now registered
  as `BroadcastLuminanceResponse` in the `OperateCode` enum and handled in the
  `Sensor` device: `brightness = (payload[2] << 8) | payload[3]`. Lux becomes
  available immediately on first broadcast without any poll.


## [3.5.1] - 2026-08-26

### Fixed

- **HDL-MSP02.4C motion now updates in real time.** The device broadcasts PIR
  state as a Universal Switch event (switch #201, opcode `0xE01D`) in addition
  to the polled `0x1605` sensors-in-one frame. The integration now subscribes
  to that UV switch broadcast, so the motion binary sensor flips immediately on
  occupancy change instead of waiting up to one poll interval. The catalog entry
  for `HDL-MSP02.4C` records `motion_uv_switch: 201`; the `Sensor` device, the
  `BusproModule.get_sensor()` factory, and the managed sensor/binary-sensor
  setup all thread the value through.

- **Illuminance sensors now poll, report `available`, and carry correct
  metadata.** The catalog uses `"illuminance"` as the capability key, but the
  `ILLUMINANCE` constant equals `"lux"`. The string comparison
  `sensor_type == ILLUMINANCE` therefore never matched for catalog-managed
  devices, causing four silent failures: the poll flag was not set (lux froze
  after the first reading), `available` always returned `True` even when no
  value had arrived, `device_class` and `native_unit_of_measurement` fell
  through to `None`, and `state_class` was not set. All comparisons now accept
  both `ILLUMINANCE` and `"illuminance"` via a small `_is_illuminance()` helper.

[3.5.1]: https://github.com/Frequencies/home_assistant_buspro/releases/tag/3.5.1

## [3.5.0] - 2026-08-26

Introduces automatic gateway discovery and bus scanning for device import.
Also contains a broad stability pass targeting HA 2025 compatibility, gateway
availability tracking, config-flow edge cases, and sensor correctness.

### Added

- **Automatic gateway discovery.** When starting the integration setup, Home
  Assistant now broadcasts harmless UDP probes to every local interface and
  presents a dropdown of discovered HDL IP gateways (IP address, number of bus
  devices heard). If nothing is found the flow falls through to manual entry
  automatically — no extra click required. Implemented in
  `gateway_discovery.py` (`async_discover_gateways`).

- **Bus scanner — import devices from the UI.** A new **Scan bus for devices**
  option is available in the integration's options menu. It broadcasts a spread
  of read requests for 12 seconds, listens for replies, and identifies relays,
  dimmers, sensors, covers, floor-heating modules, and AC units by their
  telegram pattern. Results are shown as a checklist; selected devices are added
  as managed entities without restarting HA. A directed follow-up phase asks
  each found device individually for its channel status, which many relay and
  dimmer modules only answer when addressed directly. Implemented in
  `bus_scanner.py` (`BusScanner`).

- **CI/CD workflows.** A `tests.yml` workflow runs the full test suite on Python
  3.12 and 3.13 on every push and pull request. A `release.yml` workflow creates
  a GitHub Release with the matching CHANGELOG section when a `v*` tag is pushed.

### Changed

- **Internal code reorganized into four subpackages.** The flat `buspro/`
  directory is split into `catalog/` (device definitions and model registry),
  `managed/` (runtime device tracking and logic), `yaml_compat/` (YAML loading
  helpers), and `helpers/` (shared HA entity and network utilities). All 54
  tests pass; no behavioral changes.

- **UTF-8 BOM stripped from pybuspro source files.** Seven files under
  `pybuspro/` were saved with a BOM by a Windows editor. `hassfest` on Python
  3.14 rejects `U+FEFF` as an invalid non-printable character; all seven files
  are now clean UTF-8.

### Fixed

**Critical / Home Assistant compatibility**

- **`hass.loop` replaced with `asyncio.get_running_loop()`.** The deprecated
  `hass.loop` attribute was removed in Home Assistant 2025.x. The integration
  used it in two places (`__init__.py` and `config_flow.py`); both are now
  updated. On affected HA versions the integration would fail to start or log a
  hard error.

**High — gateway / startup**

- **Gateway startup failure now raises `ConfigEntryNotReady`.** When the UDP
  socket cannot be bound (port already in use, OS error), HA will now
  automatically schedule a retry instead of leaving the entry in a broken,
  non-retrying state.
- **`async_step_scan_bus` empty-selection no longer silently saves nothing.**
  Submitting the scan form with no devices selected previously called
  `async_create_entry` — which wrote an unchanged options dict and gave no
  feedback. It now aborts with `scan_no_new_devices`, which surfaces a clear
  message in the UI.
- **Fire-and-forget reload removed from `async_step_edit_legacy_device`.**
  Device name/model edits scheduled a bare `async_create_task` coroutine that
  was never awaited; exceptions were silently dropped and the reload could
  complete in an indeterminate order relative to the options write. The task is
  removed; HA reloads the entry through the normal `async_update_entry` +
  `async_create_entry` path.

**High — entity availability**

- **Connectivity and diagnostic sensors now track gateway state.** The `module`
  parameter was not forwarded to `BusproLogicControllerConnectivitySensor`,
  `BusproDimmerConnectivitySensor`, and their diagnostic counterparts, so
  `available` was always `True` regardless of whether the gateway was connected.
  All four classes now accept `module=None` and check `module.connected` when
  the module is present.
- **Climate, switch, and binary-sensor `available` properties also updated.**
  The same `module`-forwarding fix was applied to climate channel entities and
  switch entities so all platform types consistently reflect gateway connectivity.

**Medium — correctness**

- **Private `_device_address` and `_device_type` replaced with public
  properties** across `climate.py`, `cover.py`, `light.py`, and `fan.py`. The
  pybuspro `FloorHeating` and `ConfirmableFloorHeating` classes now expose a
  public `device_type` property.
- **Climate callback no longer replaces `self._device` on every push update.**
  `async_register_callbacks` was reassigning `self._device = device` on each
  state push, discarding the original reference; removed.
- **`BusproSensor.should_poll` fixed.** The property previously forced polling
  whenever `native_value` was `None`, which made sensors poll indefinitely even
  when no scan interval was configured. Polling is now controlled exclusively by
  the configured `scan_interval`.
- **Deprecated `state` and `unit_of_measurement` properties removed from
  `BusproSensor`.** These shadowed `native_value` / `native_unit_of_measurement`
  and caused HA to emit deprecation warnings on each state update.
- **Cover `supported_features` migrated to `_attr_supported_features`.** Tilt
  features (`OPEN_TILT`, `CLOSE_TILT`, `STOP_TILT`) were advertised but never
  implemented; they are removed. The remaining features are now set once in
  `__init__` rather than recomputed on every property access.
- **Bus scanner uses a `time.monotonic()` deadline.** The previous
  elapsed-accumulation pattern could overshoot or undershoot the scan window due
  to `asyncio.sleep` jitter; the deadline approach is drift-free.
- **Bus scanner preserves the existing `all_messages` callback.** Registering
  the scan handler previously replaced the UDP client's running callback, which
  could drop other in-flight messages; callbacks are now chained.
- **YAML sensor: malformed `relay_address` is now skipped with a warning.**
  An address with fewer than three dot-separated segments previously raised an
  `IndexError`; it now logs a clear warning and continues.

**Config flow**

- **Manual step preserves user input on validation errors.** Host, port, send
  port, receive port, and client address fields were reset to defaults whenever
  validation failed; they now repopulate from the submitted values.
- **`async_step_reconfigure` skips socket probe when entry is already loaded.**
  Attempting to bind the same receive port twice raises `OSError`; the probe is
  now skipped for loaded entries where the socket is already open.
- **`async_step_gateway` double-reload race fixed.** Options were written across
  two separate `async_update_entry` calls, creating a window where a reload
  could see stale options; options are now written in the first call.

**UI strings**

- Fixed typo: "An error occured." → "An error occurred." (`strings.json`).
- Removed dead `selector.gateway_manual` key from the `config` block of
  `strings.json`.

**Sensor protocol**

- **HDL-MSP02.4C lux and motion now populate.** The device answers the
  *sensors-in-one* query (`0x1604`/`0x1605`), not the standard sensor query
  (`0x1645`), so its catalog profile was switched from `12in1` to
  `sensors_in_one`. Home Assistant now polls the frame that actually carries
  illuminance and motion.
- **Sensors-in-one temperature offset corrected.** The `0x1605` frame encodes
  temperature with a `+20` offset (20 == 0 °C). It is now decoded as
  `payload[1] - 20`, matching the `0xE3E5` broadcast value (confirmed on the
  MSP02.4C: raw 49 → 29 °C).
- **Humidity `0xFF` sentinel handled.** Devices without a humidity sensor (e.g.
  MSP02.4C) report `0xFF` in the humidity byte; this is now surfaced as `None`
  instead of 255.

[3.5.0]: https://github.com/Frequencies/home_assistant_buspro/releases/tag/3.5.0

## [3.4.0] - 2026-08-25

Fixes illuminance (lux) and motion on the **HDL-MSP02.4C** multi-sensor, based
on live `buspro.telegram` captures from a real device.

### Fixed

- **HDL-MSP02.4C now reports lux and motion.** The model was catalogued with
  the `12in1` profile, so the integration polled it with `ReadSensorStatus`
  (`0x1645`), which the device never answers. Captures show it is a
  *sensors-in-one* device: it replies to `ReadSensorsInOneStatus` (`0x1604`)
  with a `0x1605` frame carrying lux in `payload[2..3]` and motion in
  `payload[7]`. The catalog profile is corrected to `sensors_in_one`.
- **UI-managed multi-sensors now poll for lux/humidity instead of reading
  once.** `sensors-in-one` lux and humidity only arrive in the polled `0x1605`
  response, but managed measurement entities were created with
  `scan_interval = 0`, so they read a single value at startup and then froze
  (`should_poll` stayed false once a non-`None` value was cached). The
  illuminance channel of a managed multi-sensor now polls, and because bus
  telegrams are dispatched to every device object at an address, that one poll
  also refreshes temperature, humidity, and motion on the sibling entities.
- **`sensors-in-one` temperature offset.** The `0x1605` frame encodes
  temperature as `actual + 20` (raw `49` → `29 °C`, matching the device's own
  `0xE3E5` broadcast). The runtime parser and the diagnostics decoder now
  subtract the offset, so a polled reading no longer disagrees with the
  broadcast value.
- **`sensors-in-one` humidity sentinel.** `payload[4] == 0xFF` on models
  without a humidity sensor (e.g. MSP02.4C) is now treated as "not present"
  (`None`) instead of a bogus `255 %` reading.

### Notes

- **Instant motion:** the MSP02.4C also broadcasts PIR state as a Universal
  Switch event (observed on switch `201`, `UniversalSwitchControlResponse`
  `[201, 1]` / `[201, 0]`). For zero-lag occupancy, add a Universal Switch
  binary sensor at the device address with that switch number; the polled
  `payload[7]` motion above is a lower-frequency fallback.
- **HDL-MS08M.4C** is still catalogued as `12in1` and may need the same
  `sensors_in_one` correction — left unchanged pending a capture from that
  model.

### Contributors

- Protocol and integration suites still pass:
  ```bash
  python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v
  python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v
  ```
  A new regression test, `test_sensors_in_one_decodes_real_msp02_frame`, locks
  in the captured MSP02.4C `0x1605` payload
  (`[248, 49, 0, 6, 255, 255, 255, 1, 0, 0, 0, 0, 255]` → 29 °C, 6 lux, motion
  on, no humidity).

[3.4.0]: https://github.com/Frequencies/home_assistant_buspro/releases/tag/3.4.0

## [3.3.0] - 2026-08-25

Packaging release. The integration is now shipped in the **standard Home
Assistant / HACS repository layout**. This is a structural change only — there
are **no functional or behavioral changes** to the integration itself, and no
device, entity, or configuration changes.

### Changed

- **Repository restructured to the standard `custom_components/buspro/` layout.**
  All integration code (`__init__.py`, platform modules, `manifest.json`,
  `strings.json`, `services.yaml`, `pybuspro/`, `devices/`, `tools/`,
  `translations/`, `tests/`) now lives under `custom_components/buspro/` instead
  of the repository root. `README.md`, `LICENSE`, `hacs.json`, and `docs/` remain
  at the repository root. Moves were done with `git mv`, so file history is
  preserved. (107 files relocated, 0 code changes.)

### Fixed

- **`tools/check_catalog_models.py` now resolves its paths correctly.** In the
  previous flat layout its repo-root calculation pointed outside the repository,
  so the catalog-vs-official-model check could not find
  `devices/official_models.json`. It works again in the standard layout.

### Removed

- **Stale compiled artifacts** (a leftover `custom_components/buspro/*.pyc`
  copy and stray `.DS_Store` files) that were shadowing the real source during
  local test runs.

### Upgrade notes

- **HACS users:** because the source layout changed, HACS may ask you to
  reinstall/redownload the integration. Your config entry, devices, and entities
  are unaffected — no reconfiguration is required.
- **Manual installers:** copy `custom_components/buspro/` from the repository
  into your Home Assistant `config/custom_components/` directory (previously the
  files sat at the repository root).
- **Contributors:** the documented test suites are unchanged and still pass:
  ```bash
  python3 -m unittest discover -s custom_components/buspro/tests/buspro_protocol -v
  python3 -m unittest discover -s custom_components/buspro/tests/buspro_integration -v
  ```
  The full-integration tests under `tests/pybuspro/` and the root `tests/test_*`
  modules import the whole integration and therefore require a real Home
  Assistant environment (e.g. `pytest-homeassistant-custom-component`); they are
  not covered by the lightweight stub used by the suites above.

[3.3.0]: https://github.com/Frequencies/home_assistant_buspro/releases/tag/3.3.0
