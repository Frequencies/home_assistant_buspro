# Buspro tests

Buspro tests are colocated with the integration module for easier extraction/publishing.

## Layout

- `buspro_protocol/` — protocol/library behavior (`pybuspro`), telegram parsing, transport assumptions.
- `buspro_integration/` — Home Assistant integration behavior: catalog, managed-device logic, normalization, logging helpers.

## Naming conventions

- Test files: `test_<scope>.py`
- Test classes: `<Scope>Test` or `<Scope>ProtocolTest`
- Keep protocol and integration concerns in separate files.

## Import/path convention

Tests in these folders should resolve the Buspro module root with:

```python
Path(__file__).parents[2]
```

(Example: from `custom_components/buspro/tests/buspro_protocol/test_*.py`, `parents[2]` is `custom_components/buspro`.)

## Run examples

```bash
python3 custom_components/buspro/tests/buspro_protocol/test_sensor_protocol.py
python3 custom_components/buspro/tests/buspro_integration/test_device_catalog.py
```
