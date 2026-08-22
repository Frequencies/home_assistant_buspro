"""Pure helpers for Buspro managed-device configuration."""


def managed_unique_ids(devices):
    """Return unique IDs owned by a collection of managed devices."""
    return {
        channel["unique_id"]
        for device in devices
        for channel in device.get("channels", ())
        if channel.get("unique_id")
    }


def removed_managed_unique_ids(old_devices, new_devices):
    """Return only managed entity IDs removed by an options update."""
    return managed_unique_ids(old_devices) - managed_unique_ids(new_devices)


def fixed_channel_count(device_catalog, model):
    """Return a catalogued model's physical channel count, if fixed."""
    spec = device_catalog.get(model)
    if (
        spec is None
        or "channels" not in spec
        or spec.get("configurable_channels", False)
    ):
        return None
    return int(spec["channels"])


def is_channel_configured(name):
    """Return whether a channel name opts the channel into runtime setup."""
    return bool((name or "").strip())


def is_runtime_channel(channel):
    """Return whether a managed channel should create a protocol object."""
    return bool(channel.get("enabled", True))


def build_channel_records(
    domain,
    address,
    device_type,
    channel_keys,
    names=None,
    existing_channels=None,
):
    """Build channels while preserving existing registry identities."""
    names = names or {}
    existing_channels = existing_channels or {}
    address_part = address.replace(".", "_")
    records = []
    for channel in channel_keys:
        name = names.get(channel, "")
        channel_part = str(channel).replace("-", "_")
        existing = existing_channels.get(channel, {})
        records.append(
            {
                "number": channel,
                "name": name,
                "enabled": is_channel_configured(name),
                "object_id": existing.get(
                    "object_id",
                    f"hdl_buspro_{device_type}_{address_part}_{channel_part}",
                ),
                "unique_id": existing.get(
                    "unique_id", f"{domain}-{address}-{device_type}-{channel}"
                ),
            }
        )
    return records


def registry_disabled_update(channel_enabled, current_disabled_by):
    """Return whether and how integration-owned disabled state should change."""
    if not channel_enabled and current_disabled_by is None:
        return True, "integration"
    if channel_enabled and current_disabled_by == "integration":
        return True, None
    return False, current_disabled_by
