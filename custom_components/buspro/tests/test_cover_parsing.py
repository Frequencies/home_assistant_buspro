"""Tests for Cover and CoverConfirmable telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.cover import Cover
from custom_components.buspro.pybuspro.devices.cover_confirmable import Cover as CoverConfirmable

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


def _make_cover():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = Cover(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


def _make_cover_confirmable():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = CoverConfirmable(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


class TestCoverCurtainSwitchControlResponse(unittest.TestCase):
    """Opcode 0xE3E1 — cover control echo.
    payload[0]=channel, payload[1]=state (0=stop, 1=opening, 2=closing).
    Guard: payload[0] == self._channel AND len >= 2.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_state_opening(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 1]))
        self.assertEqual(device._state, 1)
        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)

    def test_state_closing(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 2]))
        self.assertEqual(device._state, 2)
        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)

    def test_state_stopped(self):
        device = _make_cover()
        device._state = 1
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 0]))
        self.assertEqual(device._state, 0)
        self.assertFalse(device.is_opening)
        self.assertFalse(device.is_closing)

    def test_wrong_channel_ignored(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL + 1, 1]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL]))
        device._call_device_updated.assert_not_called()

    def test_device_updated_called_on_state_change(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 1]))
        device._call_device_updated.assert_called_once()


class TestCoverReadStatusofCurtainSwitchResponse(unittest.TestCase):
    """Opcode 0xE3E3 — status read. Same handling as 0xE3E1."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_state_opening(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL, 1]))
        self.assertTrue(device.is_opening)

    def test_state_closing(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL, 2]))
        self.assertTrue(device.is_closing)

    def test_state_stopped(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL, 0]))
        self.assertFalse(device.is_opening)
        self.assertFalse(device.is_closing)

    def test_wrong_channel_ignored(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL + 5, 1]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_cover()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL]))
        device._call_device_updated.assert_not_called()


class TestCoverConfirmableCurtainSwitchControlResponse(unittest.TestCase):
    """CoverConfirmable — same state parsing plus mark_confirmed calls."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_state_opening(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 1]))
        self.assertEqual(device._state, 1)

    def test_state_closing(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 2]))
        self.assertEqual(device._state, 2)

    def test_state_stopped(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 0]))
        self.assertEqual(device._state, 0)

    def test_wrong_channel_ignored(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL + 1, 1]))
        device._call_device_updated.assert_not_called()

    def test_is_opening_property(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 1]))
        self.assertTrue(device.is_opening)
        self.assertFalse(device.is_closing)

    def test_is_closing_property(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.CurtainSwitchControlResponse,
                                               [CHANNEL, 2]))
        self.assertTrue(device.is_closing)
        self.assertFalse(device.is_opening)


class TestCoverConfirmableReadStatusofCurtainSwitchResponse(unittest.TestCase):
    """CoverConfirmable 0xE3E3 — same as control response."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_state_opening(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL, 1]))
        self.assertEqual(device._state, 1)

    def test_state_closing(self):
        device = _make_cover_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusofCurtainSwitchResponse,
                                               [CHANNEL, 2]))
        self.assertEqual(device._state, 2)


if __name__ == "__main__":
    unittest.main()
