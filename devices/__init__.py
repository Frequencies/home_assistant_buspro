"""Buspro device-catalog category modules."""

from .climate import CLIMATE_MODELS
from .dimmer import DIMMER_MODELS
from .infrastructure import INFRASTRUCTURE_MODELS
from .output import OUTPUT_MODELS
from .panel import PANEL_MODELS
from .relay import RELAY_MODELS
from .sensor import SENSOR_MODELS


DEVICE_CATALOG = {
    **INFRASTRUCTURE_MODELS,
    **RELAY_MODELS,
    **DIMMER_MODELS,
    **SENSOR_MODELS,
    **PANEL_MODELS,
    **CLIMATE_MODELS,
    **OUTPUT_MODELS,
}


MODEL_NOTES = {
    "HDL-MPED4.431": {
        "level": "warning",
        "note": (
            "Mapped to generic AC climate capabilities. "
            "Panel-specific thermostat UI and extended controls are not model-validated."
        ),
    },
    "HDL-MDT0203.532": {
        "level": "info",
        "note": (
            "Mapped to trailing-edge dimmer family behavior. "
            "Model-specific dimming curve tuning is not exposed yet."
        ),
    },
    "HDL-MDT04015.532": {
        "level": "info",
        "note": (
            "Mapped to trailing-edge dimmer family behavior. "
            "Model-specific dimming curve tuning is not exposed yet."
        ),
    },
    "HDL-MDT06015.533": {
        "level": "info",
        "note": (
            "Mapped to trailing-edge dimmer family behavior. "
            "Model-specific dimming curve tuning is not exposed yet."
        ),
    },
    "HDL-MR0416C.431": {
        "level": "info",
        "note": (
            "Mapped as a standard relay module. "
            "Current-detection specific telemetry is not exposed yet."
        ),
    },
    "HDL-MR0416D.431": {
        "level": "info",
        "note": (
            "Mapped as a standard relay module. "
            "Dry-contact loop inputs are not exposed yet."
        ),
    },
    "HDL-MR0816C.232": {
        "level": "info",
        "note": (
            "Mapped as a standard relay module. "
            "Current-detection specific telemetry is not exposed yet."
        ),
    },
    "HDL-MR0816D.432": {
        "level": "info",
        "note": (
            "Mapped as a standard relay module. "
            "Dry-contact loop inputs are not exposed yet."
        ),
    },
    "HDL-MR1216D.433": {
        "level": "info",
        "note": (
            "Mapped as a standard relay module. "
            "Dry-contact loop inputs are not exposed yet."
        ),
    },
    "HDL-MRDA0610.432": {
        "level": "info",
        "note": (
            "Mapped as a dimmer module. "
            "Ballast-specific 0-10V tuning is not exposed as dedicated entities yet."
        ),
    },
    "HDL-MRDA0610.433": {
        "level": "info",
        "note": (
            "Mapped as a dimmer module. "
            "Ballast-specific 0-10V tuning is not exposed as dedicated entities yet."
        ),
    },
    "HDL-MW02.431": {
        "level": "warning",
        "note": (
            "Mapped to fixed 2-channel cover behavior. "
            "Vendor-specific travel-time calibration parameters are not model-validated."
        ),
    },
    "HDL-M/HVAC8.1": {
        "level": "warning",
        "note": (
            "Mapped to generic AC climate capabilities. "
            "Protocol-level behavior is not yet validated against this exact model."
        ),
    },
    "HDL-MWM45.431": {
        "level": "warning",
        "note": (
            "Mapped to generic curtain/cover output behavior. "
            "Direction timing and calibration telegrams are not model-validated."
        ),
    },
    "HDL-MS08M.4C": {
        "level": "info",
        "note": (
            "Mapped to the 12in1 sensor profile by family similarity; "
            "extended capabilities may require a dedicated profile later."
        ),
    },
    "HDL-MS12M.4C": {
        "level": "info",
        "note": (
            "Mapped to the sensors_in_one profile by family similarity; "
            "extended capabilities may require a dedicated profile later."
        ),
    },
}
