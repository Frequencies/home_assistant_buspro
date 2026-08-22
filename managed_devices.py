"""Definitions and helpers for UI-managed Buspro devices."""

from __future__ import annotations

import re
from copy import deepcopy

from homeassistant.const import CONF_ADDRESS, CONF_NAME
from homeassistant.helpers.device_registry import DeviceInfo

from .const import (
    CONF_CHANNEL_COUNT,
    CONF_CHANNELS,
    CONF_DEVICE_TYPE,
    CONF_MANAGED_DEVICES,
    CONF_MODEL,
    DEVICE_TYPE_AC,
    DEVICE_TYPE_COVER,
    DEVICE_TYPE_DIMMER,
    DEVICE_TYPE_DRY_CONTACT,
    DEVICE_TYPE_FAN,
    DEVICE_TYPE_FLOOR_HEATING,
    DEVICE_TYPE_MULTISENSOR,
    DEVICE_TYPE_RELAY,
    DEVICE_TYPE_UNIVERSAL_SWITCH,
    DOMAIN,
)
from .managed_device_logic import build_channel_records
from .device_catalog import DEVICE_CATALOG


DEVICE_TYPE_LABELS = {
    DEVICE_TYPE_RELAY: "Relay",
    DEVICE_TYPE_DIMMER: "Dimmer",
    DEVICE_TYPE_DRY_CONTACT: "Dry contact module",
    DEVICE_TYPE_MULTISENSOR: "Multisensor / panel sensor",
    DEVICE_TYPE_FLOOR_HEATING: "Floor heating module",
    DEVICE_TYPE_AC: "AC controller",
    DEVICE_TYPE_COVER: "Curtain / cover controller",
    DEVICE_TYPE_FAN: "Fan output",
    DEVICE_TYPE_UNIVERSAL_SWITCH: "Universal switch inputs",
}

def models_for_type(device_type: str) -> list[str]:
    """Return models supported by a UI device type."""
    return [
        model
        for model, spec in DEVICE_CATALOG.items()
        if spec.get(CONF_DEVICE_TYPE) == device_type
    ]


def managed_devices(config_entry) -> list[dict]:
    """Return an isolated copy of UI-managed device definitions."""
    return deepcopy(config_entry.options.get(CONF_MANAGED_DEVICES, []))


def validate_physical_address(address: str) -> str | None:
    """Normalize a subnet.device address, or return None when invalid."""
    match = re.fullmatch(r"\s*(\d{1,3})\.(\d{1,3})\s*", address)
    if match is None:
        return None
    subnet, device = (int(part) for part in match.groups())
    if not 0 <= subnet <= 255 or not 0 <= device <= 255:
        return None
    return f"{subnet}.{device}"


def build_channels(
    address: str,
    device_type: str,
    device_name: str,
    channel_keys: list[int | str],
    names: dict[int | str, str] | None = None,
    existing_channels: dict[int | str, dict] | None = None,
) -> list[dict]:
    """Build serializable channel definitions."""
    return build_channel_records(
        DOMAIN,
        address,
        device_type,
        channel_keys,
        names,
        existing_channels,
    )


def managed_device_info(device_config: dict) -> DeviceInfo:
    """Build Device Registry metadata for a UI-managed device."""
    address = device_config[CONF_ADDRESS]
    return DeviceInfo(
        identifiers={(DOMAIN, address)},
        name=device_config[CONF_NAME],
        manufacturer="HDL",
        model=device_config[CONF_MODEL],
        serial_number=address,
    )


def channel_count(device_config: dict) -> int:
    """Return configured channel/capability count."""
    return int(device_config.get(CONF_CHANNEL_COUNT, len(device_config[CONF_CHANNELS])))
