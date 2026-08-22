"""Regression tests for YAML normalization in Buspro integration."""

import importlib.util
import logging
import sys
import types
import unittest
from pathlib import Path


BUSPRO_PATH = Path(__file__).parents[2]
PACKAGE = "_buspro_yaml_norm_test"
package = types.ModuleType(PACKAGE)
package.__path__ = [str(BUSPRO_PATH)]
sys.modules.setdefault(PACKAGE, package)
spec = importlib.util.spec_from_file_location(
    f"{PACKAGE}.yaml_normalization",
    BUSPRO_PATH / "yaml_normalization.py",
)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)

normalize_yaml_devices = module.normalize_yaml_devices


class _CaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.messages = []

    def emit(self, record):
        self.messages.append(record.getMessage())


class YamlNormalizationTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("buspro-yaml-normalization-test")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.capture = _CaptureHandler()
        self.logger.handlers = [self.capture]

    def tearDown(self):
        self.logger.handlers = []

    def test_infers_catalog_profile_when_missing(self):
        devices = [{"address": "2.10", "name": "Sensor", "model": "HDL-MSP07M.4C"}]
        catalog = {
            "HDL-MSP07M.4C": {"profile": "sensors_in_one"},
        }

        normalized = normalize_yaml_devices(
            devices,
            catalog,
            "Buspro device",
            "sensor_status",
            self.logger,
        )

        self.assertEqual(normalized[0]["profile"], "sensors_in_one")

    def test_preserves_explicit_valid_profile(self):
        devices = [
            {
                "address": "2.11",
                "name": "Sensor",
                "model": "HDL-MSP02.4C",
                "profile": "12in1",
            }
        ]
        catalog = {"HDL-MSP02.4C": {"profile": "12in1"}}

        normalized = normalize_yaml_devices(
            devices,
            catalog,
            "Buspro device",
            "sensor_status",
            self.logger,
        )

        self.assertEqual(normalized[0]["profile"], "12in1")

    def test_invalid_profile_warns_and_falls_back_to_inferred(self):
        devices = [
            {
                "address": "2.12",
                "name": "Sensor",
                "model": "HDL-MSP07M.4C",
                "profile": "typo_profile",
            }
        ]
        catalog = {"HDL-MSP07M.4C": {"profile": "sensors_in_one"}}

        normalized = normalize_yaml_devices(
            devices,
            catalog,
            "Buspro device",
            "sensor_status",
            self.logger,
        )

        self.assertEqual(normalized[0]["profile"], "sensors_in_one")
        self.assertTrue(
            any("Unsupported YAML Buspro profile 'typo_profile'" in msg for msg in self.capture.messages)
        )

    def test_unknown_model_warns_and_uses_generic_profile(self):
        devices = [
            {
                "address": "2.13",
                "name": "Unknown model sensor",
                "model": "HDL-UNKNOWN.000",
            }
        ]

        normalized = normalize_yaml_devices(
            devices,
            {},
            "Buspro device",
            "sensor_status",
            self.logger,
        )

        self.assertEqual(normalized[0]["profile"], "sensor_status")
        self.assertTrue(
            any("Unknown YAML Buspro model 'HDL-UNKNOWN.000'" in msg for msg in self.capture.messages)
        )


if __name__ == "__main__":
    unittest.main()
