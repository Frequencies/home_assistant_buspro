"""Dual-mode YAML support: entity-centric and device-centric formats."""

from __future__ import annotations

import logging
from typing import Any

from .const import (
    CONF_ADDRESS,
    CONF_CHANNEL_COUNT,
    CONF_CHANNEL_ENABLED,
    CONF_CHANNEL_NUMBER,
    CONF_CHANNELS,
    CONF_DEVICE_TYPE,
    CONF_ENTITIES,
    CONF_MODEL,
    CONF_NAME,
    CONF_OBJECT_ID,
    CONF_PROFILE,
    CONF_TYPE,
    CONF_UNIQUE_ID,
    DEFAULT_MANUFACTURER,
)

_LOGGER = logging.getLogger(__name__)


def is_device_centric(device_config: dict) -> bool:
    """Check if device config is in device-centric format (has channels key)."""
    return CONF_CHANNELS in device_config and CONF_DEVICE_TYPE in device_config


def is_entity_centric(device_config: dict) -> bool:
    """Check if device config is in entity-centric format (has entities key)."""
    return CONF_ENTITIES in device_config


def normalize_dual_mode(
    devices: list[dict],
    device_catalog: dict,
    logger: logging.Logger,
) -> list[dict]:
    """
    Normalize both entity-centric and device-centric YAML formats.

    Returns a unified list of devices with their entities properly structured.
    Entity-centric format is expanded to include full device info.
    Device-centric format is validated and preserved.
    """
    normalized = []
    seen_addresses: dict[str, str] = {}  # address -> format type

    for device in devices:
        address = device.get(CONF_ADDRESS, "unknown")

        # Detect format and normalize
        if is_device_centric(device):
            normalized_device = _normalize_device_centric(device, device_catalog, logger)
            format_type = "device-centric"
        elif is_entity_centric(device):
            normalized_device = _normalize_entity_centric(device, device_catalog, logger)
            format_type = "entity-centric"
        else:
            # Ambiguous - default to entity-centric (legacy format)
            normalized_device = _normalize_entity_centric(device, device_catalog, logger)
            format_type = "entity-centric (inferred)"

        # Check for duplicates
        if address in seen_addresses:
            logger.warning(
                f"Device at address {address} defined multiple times "
                f"({seen_addresses[address]} and {format_type}). "
                f"Using the last definition."
            )
        else:
            seen_addresses[address] = format_type

        normalized.append(normalized_device)

    return normalized


def _normalize_device_centric(
    device: dict,
    device_catalog: dict,
    logger: logging.Logger,
) -> dict:
    """
    Normalize device-centric format:
    {
        address: "2.5",
        name: "Device Name",
        model: "HDL-MD0606.32",
        device_type: "relay",
        channel_count: 6,
        channels: [
            { number: 1, name: "Ch1", enabled: true, object_id: "...", unique_id: "..." },
            ...
        ]
    }
    """
    normalized = dict(device)
    address = normalized.get(CONF_ADDRESS, "unknown")
    model = normalized.get(CONF_MODEL, "Buspro device")

    # Validate model against catalog
    if model not in device_catalog and model != "Buspro device":
        logger.warning(f"Unknown model '{model}' at address {address}")

    # Validate channels structure
    channels = normalized.get(CONF_CHANNELS, [])
    if not isinstance(channels, list):
        logger.warning(f"Invalid channels format at address {address}")
        normalized[CONF_CHANNELS] = []
        return normalized

    # Ensure all channels have required fields
    validated_channels = []
    for channel in channels:
        validated_channel = {
            CONF_CHANNEL_NUMBER: channel.get(CONF_CHANNEL_NUMBER),
            CONF_NAME: channel.get(CONF_NAME, f"Channel {channel.get(CONF_CHANNEL_NUMBER)}"),
            CONF_CHANNEL_ENABLED: channel.get(CONF_CHANNEL_ENABLED, True),
        }

        # Copy optional fields
        if CONF_OBJECT_ID in channel:
            validated_channel[CONF_OBJECT_ID] = channel[CONF_OBJECT_ID]
        if CONF_UNIQUE_ID in channel:
            validated_channel[CONF_UNIQUE_ID] = channel[CONF_UNIQUE_ID]

        validated_channels.append(validated_channel)

    normalized[CONF_CHANNELS] = validated_channels

    # Ensure device_type is present
    if CONF_DEVICE_TYPE not in normalized:
        logger.warning(f"Missing device_type at address {address}")

    return normalized


def _normalize_entity_centric(
    device: dict,
    device_catalog: dict,
    logger: logging.Logger,
) -> dict:
    """
    Normalize entity-centric format (legacy):
    {
        address: "2.10",
        name: "Device Name",
        model: "HDL-MSP02.4C",  # optional
        profile: "12in1",  # optional
        entities: [
            { type: "temperature", name: "Temp", object_id: "...", ... },
            ...
        ]
    }

    This format focuses on the entities within a device.
    """
    from .yaml_normalization import KNOWN_SENSOR_PROFILES

    normalized = dict(device)
    address = normalized.get(CONF_ADDRESS, "unknown")
    model = normalized.get(CONF_MODEL, "Buspro device")
    profile = normalized.get(CONF_PROFILE)

    # Validate model
    if model not in device_catalog and model != "Buspro device":
        logger.warning(f"Unknown model '{model}' at address {address}")

    # Validate and infer profile
    inferred_profile = device_catalog.get(model, {}).get(CONF_PROFILE)

    if (
        isinstance(profile, str)
        and profile
        and profile not in KNOWN_SENSOR_PROFILES
    ):
        logger.warning(f"Unsupported profile '{profile}' at address {address}")
        profile = None

    if model != "Buspro device" and inferred_profile and not profile:
        normalized[CONF_PROFILE] = inferred_profile
    elif not profile:
        normalized[CONF_PROFILE] = "sensor_status"
    else:
        normalized[CONF_PROFILE] = profile

    # Validate entities structure
    entities = normalized.get(CONF_ENTITIES, [])
    if not isinstance(entities, list):
        logger.warning(f"Invalid entities format at address {address}")
        normalized[CONF_ENTITIES] = []
        return normalized

    # Ensure all entities have required fields
    validated_entities = []
    for entity in entities:
        validated_entity = {
            CONF_TYPE: entity.get(CONF_TYPE),
            CONF_NAME: entity.get(CONF_NAME),
            CONF_OBJECT_ID: entity.get(CONF_OBJECT_ID),
        }

        # Copy optional fields
        for optional_field in [CONF_UNIQUE_ID, "device_class", "unit_of_measurement",
                               "scan_interval", "offset"]:
            if optional_field in entity:
                validated_entity[optional_field] = entity[optional_field]

        validated_entities.append(validated_entity)

    normalized[CONF_ENTITIES] = validated_entities

    return normalized


def detect_conflicts(
    entity_centric_devices: list[dict],
    device_centric_devices: list[dict],
    logger: logging.Logger,
) -> bool:
    """
    Detect conflicts between entity-centric and device-centric configs.
    Returns True if no conflicts, False if conflicts found.
    """
    entity_addresses = {d.get(CONF_ADDRESS) for d in entity_centric_devices}
    device_addresses = {d.get(CONF_ADDRESS) for d in device_centric_devices}

    overlapping = entity_addresses & device_addresses
    if overlapping:
        logger.error(
            f"Address conflict: same address defined in both "
            f"entity-centric and device-centric formats: {overlapping}"
        )
        return False

    return True


def merge_device_lists(
    entity_centric: list[dict],
    device_centric: list[dict],
    logger: logging.Logger,
) -> list[dict]:
    """Merge entity-centric and device-centric device lists."""
    if not detect_conflicts(entity_centric, device_centric, logger):
        logger.error("Cannot merge configs with address conflicts")
        return entity_centric + device_centric

    # Both lists can coexist since they don't overlap
    return entity_centric + device_centric
