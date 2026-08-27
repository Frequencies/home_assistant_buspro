"""Tests for LogicControllerDiagnostics telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.logic_controller import (
    LogicControllerDiagnostics,
    decode_firmware_version,
)

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)


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


def _make_logic_controller():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = LogicControllerDiagnostics(buspro, DEVICE_ADDRESS, initial_refresh_delay=9999)
    device._call_device_updated = MagicMock()
    return device


class TestDecodeFirmwareVersion(unittest.TestCase):
    """Unit tests for the decode_firmware_version standalone function."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_printable_ascii_returned_as_string(self):
        payload = list(b"V1.2.3")
        self.assertEqual(decode_firmware_version(payload), "V1.2.3")

    def test_null_padded_ascii_stripped(self):
        payload = list(b"V2.0\x00\x00")
        self.assertEqual(decode_firmware_version(payload), "V2.0")

    def test_non_ascii_returns_dotted_decimal(self):
        payload = [1, 2, 3]
        self.assertEqual(decode_firmware_version(payload), "1.2.3")

    def test_empty_payload_returns_none(self):
        self.assertIsNone(decode_firmware_version([]))

    def test_none_payload_returns_none(self):
        self.assertIsNone(decode_firmware_version(None))

    def test_single_non_printable_byte_as_decimal(self):
        # 0x01 is non-printable → dotted decimal format
        self.assertEqual(decode_firmware_version([1]), "1")

    def test_mixed_non_printable_returns_dotted(self):
        # 0x01 is non-printable
        payload = [0x01, 0x02]
        self.assertEqual(decode_firmware_version(payload), "1.2")


class TestLogicControllerFirmwareVersionResponse(unittest.TestCase):
    """Opcode 0xEEFE — firmware version payload.
    Source address filter: only telegrams from the device's own address are processed.
    Sets _firmware_payload and _firmware_version.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_ascii_firmware_version_parsed(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse,
                      list(b"V3.1.0"),
                      source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertEqual(device.firmware_version, "V3.1.0")

    def test_firmware_payload_stored_as_list(self):
        device = _make_logic_controller()
        payload = [1, 2, 3]
        t = _telegram(OperateCode.ReadFirmwareVersionResponse, payload, source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertEqual(device.firmware_payload, [1, 2, 3])

    def test_wrong_source_address_ignored(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse,
                      list(b"V3.1.0"),
                      source_address=(9, 9))
        device._telegram_received_cb(t)
        self.assertIsNone(device.firmware_version)

    def test_empty_firmware_payload(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse, [], source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertIsNone(device.firmware_version)

    def test_numeric_firmware_as_dotted_decimal(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse,
                      [3, 1, 0],
                      source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertEqual(device.firmware_version, "3.1.0")


class TestLogicControllerOnlineFlag(unittest.TestCase):
    """Any telegram from the device address sets online=True and last_seen."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_online_flag_set_on_any_telegram(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.IsDeviceOnlineResponse, [], source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertTrue(device.online)

    def test_last_seen_set(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.IsDeviceOnlineResponse, [], source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertIsNotNone(device.last_seen)

    def test_wrong_source_telegram_fully_ignored(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse,
                      list(b"V1.0"),
                      source_address=(5, 5))
        device._telegram_received_cb(t)
        self.assertIsNone(device.online)
        self.assertIsNone(device.last_seen)

    def test_device_updated_called_for_matching_source(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.IsDeviceOnlineResponse, [], source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        device._call_device_updated.assert_called()

    def test_device_updated_not_called_for_wrong_source(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.IsDeviceOnlineResponse, [], source_address=(99, 99))
        device._telegram_received_cb(t)
        device._call_device_updated.assert_not_called()

    def test_firmware_telegram_also_sets_online(self):
        device = _make_logic_controller()
        t = _telegram(OperateCode.ReadFirmwareVersionResponse,
                      list(b"V1.0"),
                      source_address=DEVICE_ADDRESS)
        device._telegram_received_cb(t)
        self.assertTrue(device.online)


if __name__ == "__main__":
    unittest.main()
