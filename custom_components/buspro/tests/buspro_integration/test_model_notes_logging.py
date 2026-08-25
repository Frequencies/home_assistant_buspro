"""Regression tests for Buspro model-support note logging."""

import importlib.util
import logging
import sys
import types
import unittest
from pathlib import Path


BUSPRO_PATH = Path(__file__).parents[2]
PACKAGE = "_buspro_model_notes_test"

# --- set up fake top-level package ---
package = types.ModuleType(PACKAGE)
package.__path__ = [str(BUSPRO_PATH)]
sys.modules.setdefault(PACKAGE, package)


def _load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = mod
    spec.loader.exec_module(mod)
    return mod


def _make_package(module_name, dir_path):
    pkg = types.ModuleType(module_name)
    pkg.__path__ = [str(dir_path)]
    pkg.__package__ = module_name
    sys.modules.setdefault(module_name, pkg)
    return pkg


# yaml_compat.normalization (needed by catalog.model_notes)
_make_package(f"{PACKAGE}.yaml_compat", BUSPRO_PATH / "yaml_compat")
_load_module(
    f"{PACKAGE}.yaml_compat.normalization",
    BUSPRO_PATH / "yaml_compat" / "normalization.py",
)

# catalog.model_notes
_make_package(f"{PACKAGE}.catalog", BUSPRO_PATH / "catalog")
module = _load_module(
    f"{PACKAGE}.catalog.model_notes",
    BUSPRO_PATH / "catalog" / "model_notes.py",
)

emit_model_support_notes = module.emit_model_support_notes


class _CaptureHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


class ModelNotesLoggingTest(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("buspro-model-notes-test")
        self.logger.setLevel(logging.INFO)
        self.logger.propagate = False
        self.capture = _CaptureHandler()
        self.logger.handlers = [self.capture]

    def tearDown(self):
        self.logger.handlers = []

    def test_emits_summary_with_warning_and_info_counters(self):
        model_addresses = {
            "Model-A": {"2.1"},
            "Model-B": {"2.2"},
        }
        model_notes = {
            "Model-A": {"level": "warning", "note": "Warn note"},
            "Model-B": {"level": "info", "note": "Info note"},
        }

        warning_count, info_count = emit_model_support_notes(
            self.logger, model_addresses, model_notes
        )

        self.assertEqual((warning_count, info_count), (1, 1))
        messages = [record.getMessage() for record in self.capture.records]
        self.assertTrue(
            any("Model support notes summary: 1 warning, 1 info" in msg for msg in messages)
        )

    def test_compacts_addresses_in_note_message(self):
        model_addresses = {
            "Model-C": {f"2.{index}" for index in range(1, 13)},
        }
        model_notes = {
            "Model-C": {"level": "info", "note": "Family-mapped note"},
        }

        emit_model_support_notes(self.logger, model_addresses, model_notes)

        messages = [record.getMessage() for record in self.capture.records]
        note_messages = [msg for msg in messages if "Model support note for Model-C" in msg]
        self.assertEqual(len(note_messages), 1)
        self.assertIn("(+4 more)", note_messages[0])


if __name__ == "__main__":
    unittest.main()
