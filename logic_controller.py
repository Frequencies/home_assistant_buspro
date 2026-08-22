"""Shared helpers for HDL logic-controller entities."""

from .entity_helpers import parse_device_address, registry_device_definitions


LOGIC_CONTROLLER_MODEL = "HDL-MCLog.431"


def logic_controller_definitions(hass, config_entry):
    """Return registered HDL logic controllers for this config entry."""
    return {
        device["address"]: device["device_info"]
        for device in registry_device_definitions(hass, config_entry)
        if device.get("model") == LOGIC_CONTROLLER_MODEL
    }


def logic_controller_coordinator(module, address):
    """Return the shared protocol coordinator for a physical address."""
    return module.get_logic_controller(parse_device_address(address))
