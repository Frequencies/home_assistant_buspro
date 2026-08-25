"""Sensor and dry-contact input models."""

from ..const import DEVICE_TYPE_DRY_CONTACT, DEVICE_TYPE_MULTISENSOR


SENSOR_MODELS = {
    "HDL-MS04.432": {
        "device_type": DEVICE_TYPE_DRY_CONTACT,
        "channels": 4,
    },
    "HDL-MS24.232": {
        "device_type": DEVICE_TYPE_DRY_CONTACT,
        "channels": 24,
    },
    "HDL-MSP02.4C": {
        "device_type": DEVICE_TYPE_MULTISENSOR,
        "profile": "sensors_in_one",
        "capabilities": ("temperature", "illuminance", "motion"),
    },
    "HDL-MSP07M.4C": {
        "device_type": DEVICE_TYPE_MULTISENSOR,
        "profile": "sensors_in_one",
        "capabilities": (
            "temperature",
            "illuminance",
            "humidity",
            "motion",
            "dry_contact_1",
            "dry_contact_2",
        ),
    },
    "HDL-MS08M.4C": {
        "device_type": DEVICE_TYPE_MULTISENSOR,
        "profile": "12in1",
        "capabilities": ("temperature", "illuminance", "motion"),
    },
    "HDL-MS12M.4C": {
        "device_type": DEVICE_TYPE_MULTISENSOR,
        "profile": "sensors_in_one",
        "capabilities": (
            "temperature",
            "illuminance",
            "humidity",
            "motion",
            "dry_contact_1",
            "dry_contact_2",
        ),
    },
}
