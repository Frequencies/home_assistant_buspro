"""Regression tests for shared Buspro relay protocol state."""

import asyncio
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[2]))

from pybuspro.core.telegram import Telegram  # noqa: E402
from pybuspro.devices.relay import RelayModule  # noqa: E402
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


class RelayCoordinatorTest(unittest.IsolatedAsyncioTestCase):
    async def test_one_status_query_serves_all_channels(self):
        bus = _Bus(asyncio.get_running_loop())
        module = RelayModule(bus, (240, 1), initial_refresh_delay=0)
        channel_1 = module.channel(1, "One")
        channel_2 = module.channel(2, "Two")
        updates = []

        async def updated(channel):
            updates.append(channel.channel_number)

        channel_1.register_device_updated_cb(updated)
        channel_2.register_device_updated_cb(updated)
        await asyncio.sleep(0)

        self.assertEqual(len(bus.network_interface.telegrams), 1)
        self.assertEqual(
            bus.network_interface.telegrams[0].operate_code,
            OperateCode.ReadStatusOfChannels,
        )

        response = Telegram()
        response.operate_code = OperateCode.ReadStatusOfChannelsResponse
        response.payload = [2, 0, 100]
        module._telegram_received_cb(response)
        await asyncio.sleep(0)

        self.assertFalse(channel_1.is_on)
        self.assertTrue(channel_2.is_on)
        self.assertCountEqual(updates, [1, 2])
        channel_1.close()
        channel_2.close()
        self.assertEqual(bus.callbacks, [])

    async def test_control_response_updates_only_matching_channel(self):
        bus = _Bus(asyncio.get_running_loop())
        module = RelayModule(bus, (240, 2), initial_refresh_delay=60)
        channel_1 = module.channel(1, "One")
        channel_2 = module.channel(2, "Two")

        response = Telegram()
        response.operate_code = OperateCode.SingleChannelControlResponse
        response.payload = [2, 1, 100]
        module._telegram_received_cb(response)
        await asyncio.sleep(0)

        self.assertFalse(channel_1.is_on)
        self.assertTrue(channel_2.is_on)
        channel_1.close()
        channel_2.close()

    async def test_channel_control_targets_requested_output(self):
        bus = _Bus(asyncio.get_running_loop())
        module = RelayModule(bus, (240, 3), initial_refresh_delay=60)
        channel = module.channel(5, "Five")

        await channel.set_on()

        telegram = bus.network_interface.telegrams[-1]
        self.assertEqual(telegram.operate_code, OperateCode.SingleChannelControl)
        self.assertEqual(telegram.target_address, (240, 3))
        self.assertEqual(telegram.payload, [5, 100, 0, 0])
        channel.close()


if __name__ == "__main__":
    unittest.main()
