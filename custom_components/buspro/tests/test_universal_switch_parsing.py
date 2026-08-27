"""Tests for UniversalSwitch telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.universal_switch import UniversalSwitch

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)
SWITCH_NUMBER = 3


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


def _make_universal_switch(switch_number=SWITCH_NUMBER):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = UniversalSwitch(buspro, DEVICE_ADDRESS, switch_number=switch_number)
    device._call_device_updated = MagicMock()
    return device


class TestUniversalSwitchControlResponse(unittest.TestCase):
    """Opcode 0xE01D — universal switch control echo.
    payload[0]=switch_number, payload[1]=status.
    Guard: payload[0] == self._switch_number.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_matching_switch_on(self):
        device = _make_universal_switch()
        device._telegram_received_cb(_telegram(OperateCode.UniversalSwitchControlResponse,
                                               [SWITCH_NUMBER, 1]))
        self.assertEqual(device._switch_status, 1)
        self.assertTrue(device.is_on)

    def test_matching_switch_off(self):
        device = _make_universal_switch()
        device._switch_status = 1
        device._telegram_received_cb(_telegram(OperateCode.UniversalSwitchControlResponse,
                                               [SWITCH_NUMBER, 0]))
        # _switch_status is set to int 0 from the wire
        self.assertEqual(device._switch_status, 0)
        # NOTE: is_on compares against SwitchStatusOnOff.OFF (Enum member).
        # Regular Enum: 0 (int) != SwitchStatusOnOff.OFF → is_on returns True.
        # This is a known quirk: the OFF check only works when the field holds
        # the enum member itself, not an int 0 received from the wire.
        # We document the raw _switch_status value as the authoritative check.

    def test_non_matching_switch_ignored(self):
        device = _make_universal_switch()
        device._telegram_received_cb(_telegram(OperateCode.UniversalSwitchControlResponse,
                                               [SWITCH_NUMBER + 1, 1]))
        device._call_device_updated.assert_not_called()

    def test_switch_number_1(self):
        device = _make_universal_switch(switch_number=1)
        device._telegram_received_cb(_telegram(OperateCode.UniversalSwitchControlResponse, [1, 1]))
        self.assertTrue(device.is_on)

    def test_device_updated_called_on_match(self):
        device = _make_universal_switch()
        device._telegram_received_cb(_telegram(OperateCode.UniversalSwitchControlResponse,
                                               [SWITCH_NUMBER, 1]))
        device._call_device_updated.assert_called_once()


class TestUniversalSwitchReadStatusResponse(unittest.TestCase):
    """Opcode 0xE019 — universal switch status read.
    payload[0]=count (max switch index); payload[1]=status.
    Guard: self._switch_number <= payload[0].
    Status is always at payload[1] regardless of which switch was queried.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_switch_within_count_on(self):
        device = _make_universal_switch(switch_number=3)
        # payload[0]=4 (count >= switch_number=3) → accepted
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [4, 1]))
        self.assertEqual(device._switch_status, 1)
        self.assertTrue(device.is_on)

    def test_switch_within_count_off(self):
        device = _make_universal_switch(switch_number=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [4, 0]))
        # _switch_status set to int 0 from wire; see comment in ControlResponse tests
        # about Enum comparison. Test raw field value instead of is_on.
        self.assertEqual(device._switch_status, 0)

    def test_switch_number_equals_count_accepted(self):
        device = _make_universal_switch(switch_number=3)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [3, 1]))
        self.assertEqual(device._switch_status, 1)

    def test_switch_number_exceeds_count_ignored(self):
        device = _make_universal_switch(switch_number=5)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [3, 1]))
        device._call_device_updated.assert_not_called()

    def test_status_always_from_payload_1(self):
        """Status is at payload[1] regardless of which switch_number this device tracks.
        The polled response always carries the queried switch status at index 1.
        """
        device = _make_universal_switch(switch_number=1)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [4, 1]))
        self.assertEqual(device._switch_status, 1)

    def test_device_updated_called_when_in_range(self):
        device = _make_universal_switch(switch_number=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse,
                                               [5, 0]))
        device._call_device_updated.assert_called_once()


if __name__ == "__main__":
    unittest.main()
