# Changelog

All notable changes to this project are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Fixed

- **HDL-MSP02.4C lux and motion now populate.** The device answers the
  *sensors-in-one* query (`0x1604`/`0x1605`), not the standard sensor query
  (`0x1645`), so its catalog profile was switched from `12in1` to
  `sensors_in_one`. Home Assistant now polls the frame that actually carries
  illuminance and motion.
- **Sensors-in-one temperature offset corrected.** The `0x1605` frame encodes
  temperature with a `+20` offset (20 == 0 °C). It is now decoded as
  `payload[1] - 20`, matching the `0xE3E5` broadcast value (confirmed on the
  MSP02.4C: raw 49 → 29 °C). Previously a poll would have reported 49 °C.
- **Humidity `0xFF` sentinel handled.** Devices without a humidity sensor (e.g.
  MSP02.4C) report `0xFF` in the humidity byte; this is now surfaced as `None`
  instead of 255. The diagnostics decoder applies the same offset and sentinel
  handling.

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
