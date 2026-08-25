"""Regression tests for the reusable Buspro model catalog."""

import importlib.util
import re
import sys
import types
import unittest
from pathlib import Path


BUSPRO_PATH = Path(__file__).parents[2]
PACKAGE = "_buspro_catalog_test"

# --- set up the top-level fake package ---
package = types.ModuleType(PACKAGE)
package.__path__ = [str(BUSPRO_PATH)]
sys.modules.setdefault(PACKAGE, package)


def _load_module(module_name, file_path):
    """Load a single .py file as the given module name."""
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module


def _make_package(module_name, dir_path):
    """Register a directory as a package in sys.modules."""
    pkg = types.ModuleType(module_name)
    pkg.__path__ = [str(dir_path)]
    pkg.__package__ = module_name
    sys.modules.setdefault(module_name, pkg)
    return pkg


# 1. const (needed by catalog sub-modules via `from ..const import ...`)
_load_module(f"{PACKAGE}.const", BUSPRO_PATH / "const.py")

# 2. yaml_compat package stub + normalization (needed by catalog.model_notes)
_make_package(f"{PACKAGE}.yaml_compat", BUSPRO_PATH / "yaml_compat")
_load_module(
    f"{PACKAGE}.yaml_compat.normalization",
    BUSPRO_PATH / "yaml_compat" / "normalization.py",
)

# 3. catalog package
_make_package(f"{PACKAGE}.catalog", BUSPRO_PATH / "catalog")

# 4. catalog sub-modules (relative imports resolved via sys.modules entries above)
for _sub in ("climate", "dimmer", "infrastructure", "output", "panel", "relay", "sensor"):
    _load_module(f"{PACKAGE}.catalog.{_sub}", BUSPRO_PATH / "catalog" / f"{_sub}.py")

_load_module(f"{PACKAGE}.catalog.model_notes", BUSPRO_PATH / "catalog" / "model_notes.py")

# 5. catalog __init__
catalog_module = _load_module(
    f"{PACKAGE}.catalog",
    BUSPRO_PATH / "catalog" / "__init__.py",
)
DEVICE_CATALOG = catalog_module.DEVICE_CATALOG
MODEL_NOTES = catalog_module.MODEL_NOTES


class DeviceCatalogTest(unittest.TestCase):
    def test_catalog_contains_models_not_installation_addresses(self):
        self.assertFalse(
            any(re.fullmatch(r"\d+\.\d+", key) for key in DEVICE_CATALOG)
        )
        for spec in DEVICE_CATALOG.values():
            self.assertNotIn("address", spec)
            self.assertNotIn("name", spec)
            self.assertNotIn("configured_channels", spec)

    def test_known_relay_capabilities_are_exact(self):
        self.assertEqual(DEVICE_CATALOG["HDL-MR0410.431"]["channels"], 4)
        self.assertEqual(DEVICE_CATALOG["HDL-MR0810.432"]["channels"], 8)
        self.assertEqual(DEVICE_CATALOG["HDL-MR1210.433"]["channels"], 12)
        self.assertEqual(DEVICE_CATALOG["HDL-MR1610.433"]["channels"], 16)
        self.assertEqual(DEVICE_CATALOG["HDL-MR0416D.431"]["channels"], 4)
        self.assertEqual(DEVICE_CATALOG["HDL-MR0816C.232"]["channels"], 8)
        self.assertEqual(DEVICE_CATALOG["HDL-MR1220C.433"]["channels"], 12)
        self.assertEqual(DEVICE_CATALOG["HDL-MR1616.434"]["channels"], 16)
        self.assertNotIn(
            "configurable_channels", DEVICE_CATALOG["HDL-MR1210.433"]
        )

    def test_known_dimmer_capabilities_are_exact(self):
        self.assertEqual(DEVICE_CATALOG["HDL-MD0206.432"]["channels"], 2)
        self.assertEqual(DEVICE_CATALOG["HDL-MDT0203.532"]["channels"], 2)
        self.assertEqual(DEVICE_CATALOG["HDL-MDT04015.433"]["channels"], 4)
        self.assertEqual(DEVICE_CATALOG["HDL-MDT04015.532"]["channels"], 4)
        self.assertEqual(DEVICE_CATALOG["HDL-MDT06015.533"]["channels"], 6)
        self.assertEqual(DEVICE_CATALOG["HDL-MRDA0610.432"]["channels"], 6)
        self.assertEqual(DEVICE_CATALOG["HDL-MRDA0610.433"]["channels"], 6)

    def test_generic_outputs_allow_user_selected_channel_count(self):
        self.assertTrue(
            DEVICE_CATALOG["HDL Buspro Curtain Controller"][
                "configurable_channels"
            ]
        )

    def test_new_sensor_and_panel_variants_are_present(self):
        self.assertEqual(
            DEVICE_CATALOG["HDL-MS12M.4C"]["profile"], "sensors_in_one"
        )
        self.assertEqual(DEVICE_CATALOG["HDL-MPL8.431"]["button_count"], 8)
        self.assertEqual(
            DEVICE_CATALOG["HDL-MPED4.431"]["device_type"], "ac"
        )

    def test_four_button_tile_variants_expose_four_buttons(self):
        for model in ("HDL-MP4B-A/TILE.48", "HDL-MP4B/TILE.48"):
            self.assertEqual(DEVICE_CATALOG[model]["button_count"], 4)
            self.assertTrue(DEVICE_CATALOG[model]["panel_actions"])

    def test_model_notes_mark_unverified_or_family_mapped_models(self):
        self.assertEqual(MODEL_NOTES["HDL-M/HVAC8.1"]["level"], "warning")
        self.assertEqual(MODEL_NOTES["HDL-MPED4.431"]["level"], "warning")
        self.assertEqual(MODEL_NOTES["HDL-MW02.431"]["level"], "warning")
        self.assertEqual(MODEL_NOTES["HDL-MWM45.431"]["level"], "warning")
        self.assertEqual(MODEL_NOTES["HDL-MDT0203.532"]["level"], "info")
        self.assertEqual(MODEL_NOTES["HDL-MDT04015.532"]["level"], "info")
        self.assertEqual(MODEL_NOTES["HDL-MDT06015.533"]["level"], "info")
        self.assertEqual(MODEL_NOTES["HDL-MR0416D.431"]["level"], "info")
        self.assertEqual(MODEL_NOTES["HDL-MS08M.4C"]["level"], "info")
        self.assertIn("family similarity", MODEL_NOTES["HDL-MS12M.4C"]["note"])


if __name__ == "__main__":
    unittest.main()
