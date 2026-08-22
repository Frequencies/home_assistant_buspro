"""Normalization and validation helpers for legacy YAML Buspro devices."""

from __future__ import annotations

import logging


KNOWN_SENSOR_PROFILES = {
    "sensor_status",
    "12in1",
    "sensors_in_one",
    "dlp",
    "dry_contact",
}


def _compact_addresses(addresses: set[str], limit: int = 8) -> str:
    ordered = sorted(addresses)
    if len(ordered) <= limit:
        return ", ".join(ordered)
    shown = ", ".join(ordered[:limit])
    return f"{shown} (+{len(ordered) - limit} more)"


def normalize_yaml_devices(
    devices: list[dict],
    device_catalog: dict,
    default_model: str,
    default_profile: str,
    logger: logging.Logger,
) -> list[dict]:
    """Normalize legacy YAML devices to universal defaults and known profiles."""
    normalized = []
    unknown_model_addresses: dict[str, set[str]] = {}
    invalid_profile_addresses: dict[str, set[str]] = {}

    for device in devices:
        item = dict(device)
        model = item.get("model") or default_model
        item["model"] = model

        address = str(item.get("address", "unknown"))
        if model not in device_catalog and model != default_model:
            unknown_model_addresses.setdefault(model, set()).add(address)

        current_profile = item.get("profile")
        inferred_profile = device_catalog.get(model, {}).get("profile")

        if (
            isinstance(current_profile, str)
            and current_profile
            and current_profile not in KNOWN_SENSOR_PROFILES
        ):
            invalid_profile_addresses.setdefault(current_profile, set()).add(address)
            current_profile = None

        if model != default_model and inferred_profile and (
            not current_profile or current_profile == default_profile
        ):
            item["profile"] = inferred_profile
        elif not current_profile:
            item["profile"] = default_profile
        else:
            item["profile"] = current_profile

        normalized.append(item)

    for model in sorted(unknown_model_addresses):
        logger.warning(
            "Unknown YAML Buspro model '%s' at %s. Falling back to generic behavior.",
            model,
            _compact_addresses(unknown_model_addresses[model]),
        )

    for profile in sorted(invalid_profile_addresses):
        logger.warning(
            "Unsupported YAML Buspro profile '%s' at %s. "
            "Falling back to inferred/default profile.",
            profile,
            _compact_addresses(invalid_profile_addresses[profile]),
        )

    return normalized


def compact_addresses(addresses: set[str], limit: int = 8) -> str:
    """Public helper for compact address rendering in logs."""
    return _compact_addresses(addresses, limit=limit)
