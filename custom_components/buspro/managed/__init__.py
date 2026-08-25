"""UI-managed Buspro device helpers."""

from .devices import (
    DEVICE_TYPE_LABELS,
    build_channels,
    channel_count,
    managed_device_info,
    managed_devices,
    models_for_type,
    validate_physical_address,
)
from .logic import (
    build_channel_records,
    fixed_channel_count,
    is_channel_configured,
    is_runtime_channel,
    managed_unique_ids,
    registry_disabled_update,
    removed_managed_unique_ids,
)
