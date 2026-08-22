"""Cover, fan, and universal-switch output models."""

from ..const import DEVICE_TYPE_COVER, DEVICE_TYPE_FAN, DEVICE_TYPE_UNIVERSAL_SWITCH


OUTPUT_MODELS = {
    "HDL-MW02.431": {
        "device_type": DEVICE_TYPE_COVER,
        "channels": 2,
    },
    "HDL-MWM45.431": {
        "device_type": DEVICE_TYPE_COVER,
        "channels": 64,
        "configurable_channels": True,
    },
    "HDL Buspro Curtain Controller": {
        "device_type": DEVICE_TYPE_COVER,
        "channels": 64,
        "configurable_channels": True,
        "generic": True,
    },
    "HDL Buspro Variable-speed Fan Output": {
        "device_type": DEVICE_TYPE_FAN,
        "channels": 64,
        "configurable_channels": True,
        "dimmable": True,
        "generic": True,
    },
    "HDL Buspro On/Off Fan Output": {
        "device_type": DEVICE_TYPE_FAN,
        "channels": 64,
        "configurable_channels": True,
        "dimmable": False,
        "generic": True,
    },
    "HDL Buspro Universal Switch": {
        "device_type": DEVICE_TYPE_UNIVERSAL_SWITCH,
        "channels": 64,
        "configurable_channels": True,
        "generic": True,
    },
}
