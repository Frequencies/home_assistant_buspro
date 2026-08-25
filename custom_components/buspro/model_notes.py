"""Helpers for emitting Buspro model-support diagnostic notes."""

from __future__ import annotations

import logging

from .yaml_normalization import compact_addresses


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
