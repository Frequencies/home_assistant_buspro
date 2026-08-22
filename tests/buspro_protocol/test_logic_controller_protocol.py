"""Regression tests for HDL logic-controller diagnostics."""

import asyncio
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[2]))

from pybuspro.core.telegram import Telegram  # noqa: E402
from pybuspro.devices.logic_controller import (  # noqa: E402
    LogicControllerDiagnostics,
    decode_firmware_version,
)
from pybuspro.helpers.enums import OperateCode  # noqa: E402


class _Network:
    def __init__(self):
        self.telegrams = []

    async def send_telegram(self, telegram):
        self.telegrams.append(telegram)


class _Bus:
    def __init__(self, loop):
        self.loop = loop
        self.network_interface = _Network()
        self.callbacks = []

    def register_telegram_received_device_cb(self, callback, address, postfix=None):
        self.callbacks.append((callback, tuple(address), postfix))

    def unregister_telegram_received_device_cb(self, callback, address, postfix=None):
        self.callbacks.remove((callback, tuple(address), postfix))


class LogicControllerDiagnosticsTest(unittest.IsolatedAsyncioTestCase):
    async def test_response_updates_shared_diagnostics_and_listeners(self):
        bus = _Bus(asyncio.get_running_loop())
        diagnostics = LogicControllerDiagnostics(
            bus, (2, 2), initial_refresh_delay=3600
        )
        telegrams = []
        updates = []

        diagnostics.register_telegram_cb(telegrams.append)

        async def updated(_device):
            updates.append(True)

        diagnostics.register_device_updated_cb(updated)
        response = Telegram()
        response.source_address = (2, 2)
        response.target_address = (2, 0)
        response.operate_code = OperateCode.ReadFirmwareVersionResponse
        response.payload = list(b"1.2.3\x00")
        diagnostics._telegram_received_cb(response)
        await asyncio.sleep(0)

        self.assertTrue(diagnostics.online)
        self.assertEqual(diagnostics.firmware_version, "1.2.3")
        self.assertIsNotNone(diagnostics.last_seen)
        self.assertEqual(telegrams, [response])
        self.assertEqual(updates, [True])
        diagnostics.close()

    async def test_refresh_uses_only_read_only_diagnostic_query(self):
        bus = _Bus(asyncio.get_running_loop())
        diagnostics = LogicControllerDiagnostics(
            bus, (2, 2), initial_refresh_delay=3600
        )
        diagnostics._firmware_version = "known"
        diagnostics._last_firmware_query = asyncio.get_running_loop().time()
        await diagnostics.refresh()

        self.assertEqual(len(bus.network_interface.telegrams), 1)
        self.assertEqual(
            bus.network_interface.telegrams[0].operate_code,
            OperateCode.IsDeviceOnline,
        )
        diagnostics.close()

    def test_firmware_decoder_supports_text_and_numeric_payloads(self):
        self.assertEqual(decode_firmware_version(b"V1.4\x00"), "V1.4")
        self.assertEqual(decode_firmware_version([1, 4, 2]), "1.4.2")


if __name__ == "__main__":
    unittest.main()
