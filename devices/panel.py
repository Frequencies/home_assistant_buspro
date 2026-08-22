"""Wall panel and user-interface models."""

from ..const import DEVICE_TYPE_MULTISENSOR


_PANEL_TEMPERATURE_ONLY = {
    "device_type": DEVICE_TYPE_MULTISENSOR,
    "profile": "dlp",
    "capabilities": ("temperature",),
    "panel_actions": True,
}


PANEL_MODELS = {
    "HDL-MPTL3C.48": {
        **_PANEL_TEMPERATURE_ONLY,
    },
    "HDL-MPTL4C.48": {
        **_PANEL_TEMPERATURE_ONLY,
    },
    "HDL-MPTL4.460": {
        **_PANEL_TEMPERATURE_ONLY,
    },
    "HDL-MP4S/TILE.48": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 4,
    },
    "HDL-MP2B/TILE.48": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 2,
    },
    "HDL-MP4B-A/TILE.48": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 4,
    },
    "HDL-MP4B/TILE.48": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 4,
    },
    "HDL-MP2B.480": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 2,
    },
    "HDL-MP4B.480": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 4,
    },
    "HDL-MPL8.431": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 8,
    },
    "HDL-M/PT4.1": {
        **_PANEL_TEMPERATURE_ONLY,
        "button_count": 4,
    },
    "HDL panel": {
        **_PANEL_TEMPERATURE_ONLY,
        "generic": True,
    },
}
