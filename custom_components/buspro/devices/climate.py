"""Climate and floor-heating models."""

from ..const import DEVICE_TYPE_AC, DEVICE_TYPE_FLOOR_HEATING


CLIMATE_MODELS = {
    "HDL-MFH04.432": {
        "device_type": DEVICE_TYPE_FLOOR_HEATING,
        "channels": 4,
    },
    "HDL-MFH06.432": {
        "device_type": DEVICE_TYPE_FLOOR_HEATING,
        "channels": 6,
    },
    "HDL-M/HVAC8.1": {
        "device_type": DEVICE_TYPE_AC,
        "capabilities": ("climate",),
    },
    "HDL-MPED4.431": {
        "device_type": DEVICE_TYPE_AC,
        "capabilities": ("climate",),
    },
    "HDL Buspro AC Controller": {
        "device_type": DEVICE_TYPE_AC,
        "capabilities": ("climate",),
        "generic": True,
    },
}
