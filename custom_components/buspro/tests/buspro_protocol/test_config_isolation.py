"""Regression tests for installation-independent Buspro transport data."""

import sys
import unittest
from pathlib import Path


BUSPRO_PATH = Path(__file__).parents[2]
sys.path.insert(0, str(BUSPRO_PATH))

from pybuspro.core.telegram import Telegram  # noqa: E402
from pybuspro.helpers.enums import OperateCode  # noqa: E402
from pybuspro.helpers.telegram_helper import TelegramHelper  # noqa: E402


class ConfigIsolationTest(unittest.TestCase):
    def test_packet_uses_runtime_ip_and_client_address(self):
        helper = TelegramHelper((42, 77), "10.20.30.40")
        telegram = Telegram()
        telegram.target_address = (1, 2)
        telegram.operate_code = OperateCode.IsDeviceOnline
        telegram.payload = []

        packet = helper.build_send_buffer(telegram)

        self.assertEqual(packet[:4], bytes((10, 20, 30, 40)))
        self.assertEqual(packet[17:19], bytes((42, 77)))

    def test_component_has_no_installation_network_literals(self):
        config_flow = (BUSPRO_PATH / "config_flow.py").read_text()
        telegram_helper = (
            BUSPRO_PATH / "pybuspro" / "helpers" / "telegram_helper.py"
        ).read_text()
        udp_client = (
            BUSPRO_PATH / "pybuspro" / "transport" / "udp_client.py"
        ).read_text()

        self.assertNotIn("probe.target_address", config_flow)
        self.assertNotIn('default=form_values.get(CONF_ADDRESS, "2.")', config_flow)
        self.assertNotIn("192, 168, 1, 15", telegram_helper)
        self.assertNotIn("_last_rx", udp_client)


if __name__ == "__main__":
    unittest.main()
