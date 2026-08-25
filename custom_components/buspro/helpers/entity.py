"""Shared helpers for Buspro entities."""

import logging
import re

from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.helpers.device_registry import DeviceInfo

from ..const import (
    CONF_MANUFACTURER,
    CONF_MODEL,
    DEFAULT_MANUFACTURER,
    DEFAULT_SENSOR_MODEL,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)


def parse_device_address(address):
    """Parse a subnet.device address."""
    parts = address.split(".")
    if len(parts) != 2:
        raise ValueError(f"Expected subnet.device address, got {address!r}")
    return int(parts[0]), int(parts[1])


def address_key(address):
    """Return the normalized subnet.device key for an address."""
    if isinstance(address, str):
        parts = address.split(".")
    else:
        parts = list(address)
    if len(parts) != 2:
        raise ValueError(f"Expected subnet.device address, got {address!r}")
    return f"{int(parts[0])}.{int(parts[1])}"


def device_info_for_address(hass, address, name=None, model=None):
    """Build generic metadata, preserving existing registry information."""
    key = address_key(address)
    existing = dr.async_get(hass).async_get_device(
        identifiers={(DOMAIN, key)}, connections=set()
    )
    return DeviceInfo(
        identifiers={(DOMAIN, key)},
        name=(
            name
            or (existing.name_by_user if existing is not None else None)
            or (existing.name if existing is not None else None)
            or f"HDL Buspro {key}"
        ),
        manufacturer=(
            existing.manufacturer
            if existing is not None and existing.manufacturer
            else DEFAULT_MANUFACTURER
        ),
        model=(
            model
            or (existing.model if existing is not None else None)
            or "Buspro device"
        ),
        serial_number=key,
    )


def registry_device_metadata(hass, address):
    """Return user-visible metadata for a registered physical address."""
    key = address_key(address)
    device = dr.async_get(hass).async_get_device(
        identifiers={(DOMAIN, key)}, connections=set()
    )
    if device is None:
        return {
            "address": key,
            "name": f"HDL Buspro {key}",
            "model": "Buspro device",
        }
    return {
        "address": key,
        "name": device.name_by_user or device.name or f"HDL Buspro {key}",
        "model": device.model or "Buspro device",
    }


def registry_device_definitions(hass, config_entry):
    """Return address/model metadata already known by the Device Registry."""
    definitions = []
    for device in dr.async_get(hass).devices.values():
        if config_entry.entry_id not in device.config_entries:
            continue
        address = None
        for identifier in device.identifiers:
            if len(identifier) >= 2 and identifier[0] == DOMAIN:
                try:
                    address = address_key(identifier[1])
                except (TypeError, ValueError):
                    pass
                break
        if address is None:
            continue
        definitions.append(
            {
                "address": address,
                "name": device.name_by_user or device.name or f"HDL Buspro {address}",
                "model": device.model,
                "device_info": device_info_for_address(hass, address),
            }
        )
    return definitions


def channel_number_from_unique_id(unique_id, address):
    """Extract a physical channel from legacy or managed unique IDs."""
    subnet, device = parse_device_address(address)
    patterns = (
        rf"^\(\s*{subnet}\s*,\s*{device}\s*\)-(\d+)$",
        rf"^{re.escape(DOMAIN)}-{re.escape(address)}-[^-]+-(\d+)$",
    )
    for pattern in patterns:
        match = re.fullmatch(pattern, unique_id or "")
        if match is not None:
            return int(match.group(1))
    return None


def build_device_info(device_config):
    """Build stable Device Registry metadata for a physical Buspro device."""
    address = address_key(device_config["address"])
    return DeviceInfo(
        identifiers={(DOMAIN, address)},
        name=device_config["name"],
        manufacturer=device_config.get(CONF_MANUFACTURER, DEFAULT_MANUFACTURER),
        model=device_config.get(CONF_MODEL, DEFAULT_SENSOR_MODEL),
        serial_number=address,
    )


def attach_entity_to_physical_device(hass, entity, address):
    """Attach a legacy YAML entity to its config-entry-owned physical device."""
    physical_address = address_key(address)
    device_registry = dr.async_get(hass)
    device = device_registry.async_get_device(
        identifiers={(DOMAIN, physical_address)}, connections=set()
    )
    if device is None:
        _LOGGER.warning(
            "Cannot attach %s: Buspro physical device %s is not registered",
            entity.entity_id,
            physical_address,
        )
        return

    entity_registry = er.async_get(hass)
    registry_entry = entity_registry.async_get(entity.entity_id)
    if registry_entry is None:
        _LOGGER.warning(
            "Cannot attach %s to Buspro device %s: entity is not registered",
            entity.entity_id,
            physical_address,
        )
        return

    if registry_entry.device_id != device.id:
        try:
            entity_registry.async_update_entity(entity.entity_id, device_id=device.id)
        except Exception:  # pragma: no cover - HA registry guardrail
            _LOGGER.warning(
                "Failed to attach %s to Buspro device %s",
                entity.entity_id,
                physical_address,
                exc_info=True,
            )
