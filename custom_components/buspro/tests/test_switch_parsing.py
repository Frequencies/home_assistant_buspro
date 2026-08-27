"""Tests for Switch and SwitchConfirmable telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.switch import Switch
from custom_components.buspro.pybuspro.devices.switch_confirmable import Switch as SwitchConfirmable

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)
CHANNEL = 3


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


def _make_switch():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = Switch(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


def _make_switch_confirmable():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    device = SwitchConfirmable(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


class TestSwitchSingleChannelControlResponse(unittest.TestCase):
    """Opcode 0x0032 in Switch (switch.py).
    payload[0]=channel, payload[2]=brightness. No length guard.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_sets_brightness(self):
        device = _make_switch()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 100]))
        self.assertEqual(device._brightness, 100)

    def test_non_matching_channel_ignored(self):
        device = _make_switch()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL + 1, 0, 100]))
        device._call_device_updated.assert_not_called()

    def test_is_on_when_nonzero(self):
        device = _make_switch()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 100]))
        self.assertTrue(device.is_on)

    def test_is_off_when_zero(self):
        device = _make_switch()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 0]))
        self.assertFalse(device.is_on)

    def test_channel_1(self):
        buspro = MagicMock()
        buspro.client_address = CLIENT_ADDRESS
        with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
            device = Switch(buspro, DEVICE_ADDRESS, channel_number=1)
        device._call_device_updated = MagicMock()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse, [1, 0, 50]))
        self.assertEqual(device._brightness, 50)


class TestSwitchReadStatusOfChannelsResponse(unittest.TestCase):
    """Opcode 0x0034 in Switch.
    payload[0]=count; payload[channel]=brightness.
    Guard: channel <= payload[0].
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_brightness_from_channel_index(self):
        device = _make_switch()
        # CHANNEL=3; payload[3]=100
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 0, 100, 0]))
        self.assertEqual(device._brightness, 100)

    def test_channel_exceeds_count_ignored(self):
        device = _make_switch()
        # CHANNEL=3, payload[0]=2 → 3 > 2 → ignored
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [2, 0, 0]))
        device._call_device_updated.assert_not_called()

    def test_zero_brightness(self):
        device = _make_switch()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 0, 0, 0]))
        self.assertEqual(device._brightness, 0)
        self.assertFalse(device.is_on)


class TestSwitchSceneControlResponse(unittest.TestCase):
    """Opcode 0x0003 in Switch — triggers status re-read (no direct state change)."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_scene_response_does_not_change_brightness(self):
        device = _make_switch()
        initial = device._brightness
        device._telegram_received_cb(_telegram(OperateCode.SceneControlResponse, []))
        self.assertEqual(device._brightness, initial)


class TestSwitchConfirmableSingleChannelControlResponse(unittest.TestCase):
    """SwitchConfirmable (switch_confirmable.py).
    Same as Switch but with length guard (>= 3 bytes) and mark_confirmed.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_on(self):
        device = _make_switch_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 100]))
        self.assertEqual(device._brightness, 100)
        self.assertTrue(device.is_on)

    def test_matching_channel_off(self):
        device = _make_switch_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0, 0]))
        self.assertEqual(device._brightness, 0)
        self.assertFalse(device.is_on)

    def test_non_matching_channel_ignored(self):
        device = _make_switch_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [99, 0, 100]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_switch_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0]))
        device._call_device_updated.assert_not_called()


if __name__ == "__main__":
    unittest.main()
