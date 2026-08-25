"""YAML compatibility helpers for Buspro integration."""

from .normalization import (
    KNOWN_SENSOR_PROFILES,
    compact_addresses,
    normalize_yaml_devices,
)
from .dual_mode import (
    detect_conflicts,
    is_device_centric,
    is_entity_centric,
    merge_device_lists,
    normalize_dual_mode,
)
