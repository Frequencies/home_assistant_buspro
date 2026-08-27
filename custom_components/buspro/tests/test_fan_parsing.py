"""Tests for Fan (fan_confirmable) telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.fan_confirmable import Fan

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)
CHANNEL = 1


def _no_op_ensure_future(coro):
    try:
        coro.close()
    except AttributeError:
        pass
    return MagicMock(done=lambda: True, cancel=lambda: None)


def _telegram(operate_code, payload, target_address=None, source_address=None):
    t = Telegram()
    t.operate_code = operate_code
    t.payload = payload
    t.target_address = target_address or (0, 0)
    t.source_address = source_address or DEVICE_ADDRESS
    return t


def _make_fan(channel=CHANNEL):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = Fan(buspro, DEVICE_ADDRESS, channel_number=channel)
    device._call_device_updated = MagicMock()
    return device


class TestFanSingleChannelControlResponse(unittest.TestCase):
    """Opcode 0x0032 — fan speed echo.
    payload[0]=channel, payload[2]=speed. Length guard >= 3.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_sets_speed(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 75]))
        self.assertEqual(device.speed, 75)

    def test_non_matching_channel_ignored(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL + 1, 0, 75]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0]))
        device._call_device_updated.assert_not_called()

    def test_speed_100_is_on(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 100]))
        self.assertTrue(device.is_on)

    def test_speed_0_is_off(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 0]))
        self.assertFalse(device.is_on)

    def test_partial_speed(self):
        device = _make_fan()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 50]))
        self.assertEqual(device.speed, 50)
        self.assertTrue(device.is_on)


class TestFanReadStatusOfChannelsResponse(unittest.TestCase):
    """Opcode 0x0034 — channel status.
    Guard: len(payload) > channel_number.
    Speed is at payload[channel_number] (direct index, not count-based).
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_speed_from_channel_index(self):
        device = _make_fan(channel=1)
        # CHANNEL=1; payload=[_, speed] → payload[1]=50
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 50]))
        self.assertEqual(device.speed, 50)

    def test_payload_too_short_ignored(self):
        device = _make_fan(channel=1)
        # CHANNEL=1 but payload has only 1 element → len=1, 1 > 1 is False
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0]))
        device._call_device_updated.assert_not_called()

    def test_zero_speed_is_off(self):
        device = _make_fan(channel=1)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 0]))
        self.assertFalse(device.is_on)

    def test_channel_2(self):
        device = _make_fan(channel=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 0, 80]))
        self.assertEqual(device.speed, 80)

    def test_channel_2_payload_too_short(self):
        device = _make_fan(channel=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 50]))
        device._call_device_updated.assert_not_called()


if __name__ == "__main__":
    unittest.main()
