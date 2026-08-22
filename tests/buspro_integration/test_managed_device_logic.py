"""Regression tests for Buspro managed-device option handling."""

import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[2]))

from managed_device_logic import (  # noqa: E402
    build_channel_records,
    fixed_channel_count,
    is_channel_configured,
    is_runtime_channel,
    registry_disabled_update,
    removed_managed_unique_ids,
)


def _device(address, *unique_ids):
    return {
        "address": address,
        "channels": [{"unique_id": unique_id} for unique_id in unique_ids],
    }


class ManagedDeviceLogicTest(unittest.TestCase):
    def test_cleanup_returns_only_removed_managed_ids(self):
        old = [
            _device("2.5", "relay-1", "relay-2"),
            _device("2.6", "relay-3"),
        ]
        new = [
            _device("2.5", "relay-1"),
            _device("2.6", "relay-3"),
        ]

        removed = removed_managed_unique_ids(old, new)

        self.assertEqual(removed, {"relay-2"})
        self.assertNotIn("buspro-2.100-action", removed)
        self.assertNotIn("buspro-2.9-dimmer-connectivity", removed)

    def test_catalog_model_has_fixed_physical_count(self):
        catalog = {
            "HDL-MR1210.433": {"channels": 12},
            "HDL-MR1610.433": {"channels": 16},
            "Generic relay": {
                "channels": 64,
                "configurable_channels": True,
            },
        }

        self.assertEqual(fixed_channel_count(catalog, "HDL-MR1210.433"), 12)
        self.assertEqual(fixed_channel_count(catalog, "HDL-MR1610.433"), 16)
        self.assertIsNone(fixed_channel_count(catalog, "Generic relay"))

    def test_empty_name_disables_runtime_channel(self):
        self.assertFalse(is_channel_configured(""))
        self.assertFalse(is_channel_configured("   "))
        self.assertTrue(is_channel_configured("Kitchen light"))
        self.assertFalse(is_runtime_channel({"enabled": False}))
        self.assertTrue(is_runtime_channel({"enabled": True}))
        self.assertTrue(is_runtime_channel({}))

    def test_channel_identity_survives_name_edit(self):
        existing = {
            1: {
                "object_id": "existing_entity_id",
                "unique_id": "(2, 5)-1",
            }
        }

        channels = build_channel_records(
            "buspro", "2.5", "relay", [1], {1: "Renamed"}, existing
        )

        self.assertEqual(channels[0]["object_id"], "existing_entity_id")
        self.assertEqual(channels[0]["unique_id"], "(2, 5)-1")
        self.assertTrue(channels[0]["enabled"])

    def test_integration_disabled_state_tracks_empty_name(self):
        self.assertEqual(
            registry_disabled_update(False, None), (True, "integration")
        )
        self.assertEqual(
            registry_disabled_update(True, "integration"), (True, None)
        )
        self.assertEqual(
            registry_disabled_update(True, "user"), (False, "user")
        )


if __name__ == "__main__":
    unittest.main()
