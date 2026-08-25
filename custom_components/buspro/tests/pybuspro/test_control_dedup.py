import asyncio
import unittest

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.devices.control import _ReadStatusOfChannels


class _FakeNetworkInterface:
    def __init__(self):
        self.sent = []

    async def send_telegram(self, telegram):
        self.sent.append(telegram)


class _FakeBuspro:
    def __init__(self, loop):
        self.loop = loop
        self.network_interface = _FakeNetworkInterface()


class ControlDedupTests(unittest.IsolatedAsyncioTestCase):
    async def test_query_deduplicates_within_window(self):
        buspro = _FakeBuspro(asyncio.get_running_loop())
        ctrl = _ReadStatusOfChannels(buspro)
        ctrl.subnet_id = 1
        ctrl.device_id = 1

        await ctrl.send()
        await ctrl.send()

        self.assertEqual(len(buspro.network_interface.sent), 1)

    async def test_query_sends_again_after_window(self):
        buspro = _FakeBuspro(asyncio.get_running_loop())
        ctrl = _ReadStatusOfChannels(buspro)
        ctrl.subnet_id = 1
        ctrl.device_id = 1

        await ctrl.send()
        # Clear per-instance dedup cache to simulate the window expiring.
        if hasattr(buspro, "_query_dedup"):
            buspro._query_dedup["last_queries"].clear()

        await ctrl.send()
        self.assertEqual(len(buspro.network_interface.sent), 2)


if __name__ == "__main__":
    unittest.main()
