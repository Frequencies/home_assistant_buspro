"""Dimmer and ballast-control actuator models."""

from ..const import DEVICE_TYPE_DIMMER


DIMMER_MODELS = {
    "HDL-MD0206.432": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 2,
    },
    "HDL-MD0403.432": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 4,
    },
    "HDL-MD0602.432": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
    },
    "HDL-MDT0203.433": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 2,
    },
    "HDL-MDT0203.532": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 2,
    },
    "HDL-MDT04015.433": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 4,
    },
    "HDL-MDT04015.532": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 4,
    },
    "HDL-MDT06015.433": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
    },
    "HDL-MDT06015.533": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
    },
    "HDL-MDLED0605.432": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
        "dimmer_diagnostics": True,
    },
    "HDL-MRDA0610.433": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
    },
    "HDL-MRDA0610.432": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 6,
    },
    "SB-DN-DALI64": {
        "device_type": DEVICE_TYPE_DIMMER,
        "channels": 64,
    },
}
