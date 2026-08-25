import unittest

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import DeviceType, OperateCode
from custom_components.buspro.pybuspro.helpers.telegram_helper import TelegramHelper


class TelegramHelperTests(unittest.TestCase):
    def setUp(self):
        self.th = TelegramHelper()

    def _sample_telegram(self):
        telegram = Telegram()
        telegram.source_address = (200, 200)
        telegram.source_device_type = DeviceType.PyBusPro
        telegram.target_address = (1, 1)
        telegram.operate_code = OperateCode.ReadStatusOfChannels
        telegram.payload = []
        return telegram

    def test_build_send_buffer_and_parse_roundtrip(self):
        telegram = self._sample_telegram()
        raw = self.th.build_send_buffer(telegram)

        parsed = self.th.build_telegram_from_udp_data(raw, ("127.0.0.1", 6000))
        self.assertIsNotNone(parsed)
        self.assertEqual(parsed.source_address, telegram.source_address)
        self.assertEqual(parsed.target_address, telegram.target_address)
        self.assertEqual(parsed.operate_code, telegram.operate_code)
        self.assertEqual(parsed.payload, telegram.payload)

    def test_crc_mismatch_returns_none(self):
        telegram = self._sample_telegram()
        raw = bytearray(self.th.build_send_buffer(telegram))
        raw[-1] ^= 0xFF  # break CRC

        parsed = self.th.build_telegram_from_udp_data(raw, ("127.0.0.1", 6000))
        self.assertIsNone(parsed)

    def test_replace_none_values(self):
        telegram = Telegram()
        replaced = self.th.replace_none_values(telegram)
        self.assertEqual(replaced.payload, [])
        self.assertEqual(replaced.source_address, [200, 200])
        self.assertEqual(replaced.source_device_type, DeviceType.PyBusPro)


if __name__ == "__main__":
    unittest.main()
