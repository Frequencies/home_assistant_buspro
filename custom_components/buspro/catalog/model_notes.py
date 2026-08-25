"""Model-support notes and diagnostic logging for HDL Buspro devices."""

from __future__ import annotations

import logging

from ..yaml_compat.normalization import compact_addresses


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


def emit_model_support_notes(
    logger: logging.Logger,
    model_addresses: dict[str, set[str]],
    model_notes: dict[str, dict],
) -> tuple[int, int]:
    """Emit per-model support notes and a grouped summary.

    Returns a tuple of (warning_models, info_models).
    """
    info_models = 0
    warning_models = 0

    for model in sorted(model_addresses):
        note = model_notes.get(model)
        if note is None:
            continue
        addresses = compact_addresses(model_addresses[model], limit=8)
        message = note["note"]
        if addresses:
            message = f"{message} Addresses: {addresses}."
        if note.get("level") == "warning":
            warning_models += 1
            logger.warning("Model support note for %s: %s", model, message)
        else:
            info_models += 1
            logger.info("Model support note for %s: %s", model, message)

    if warning_models or info_models:
        logger.info(
            "Model support notes summary: %s warning, %s info",
            warning_models,
            info_models,
        )

    return warning_models, info_models
