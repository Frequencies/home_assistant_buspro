"""Helpers shared by HDL dimmer diagnostic platforms."""

from ..const import CONF_MANAGED_DEVICES
from ..catalog import DEVICE_CATALOG
from .entity import registry_device_definitions
from ..managed import managed_device_info


def dimmer_diagnostic_definitions(hass, config_entry):
    """Return configured dimmers that support extended diagnostics."""
    definitions = {}
    for device in registry_device_definitions(hass, config_entry):
        spec = DEVICE_CATALOG.get(device.get("model"), {})
        if spec.get("dimmer_diagnostics"):
            definitions[device["address"]] = (
                int(spec["channels"]),
                device["device_info"],
            )

    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        spec = DEVICE_CATALOG.get(device_config.get("model"), {})
        if spec.get("dimmer_diagnostics"):
            definitions[device_config["address"]] = (
                int(spec["channels"]),
                managed_device_info(device_config),
            )
    return definitions
