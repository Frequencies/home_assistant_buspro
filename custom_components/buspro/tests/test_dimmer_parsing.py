"""Tests for DimmerDiagnostics telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.dimmer import DimmerDiagnostics

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)
CHANNEL_COUNT = 3


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


def _make_dimmer(channel_count=CHANNEL_COUNT):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = DimmerDiagnostics(buspro, DEVICE_ADDRESS, channel_count=channel_count)
    device._call_device_updated = MagicMock()
    return device


class TestDimmerReadLimitOfEveryChannelResponse(unittest.TestCase):
    """Opcode 0xF017 — minimum + per-channel maximum brightness.
    payload[0]=minimum; payload[1..channel_count]=maximum per channel.
    Guard: len(payload) >= channel_count + 1.
    NOTE: source address filter only controls the _online flag, NOT opcode processing.
    Opcodes are processed regardless of source address.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_minimum_brightness_parsed(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90, 95, 85],
                                               source_address=DEVICE_ADDRESS))
        self.assertEqual(device.minimum_brightness, 10)

    def test_maximum_brightness_per_channel(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90, 95, 85],
                                               source_address=DEVICE_ADDRESS))
        self.assertEqual(device.maximum_brightness(1), 90)
        self.assertEqual(device.maximum_brightness(2), 95)
        self.assertEqual(device.maximum_brightness(3), 85)

    def test_short_payload_ignored(self):
        device = _make_dimmer()
        # channel_count=3 requires 4 bytes minimum; only 2 provided
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90],
                                               source_address=DEVICE_ADDRESS))
        device._call_device_updated.assert_not_called()
        self.assertIsNone(device.minimum_brightness)

    def test_exactly_minimum_payload_accepted(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90, 95, 85],
                                               source_address=DEVICE_ADDRESS))
        self.assertEqual(device.minimum_brightness, 10)
        device._call_device_updated.assert_called_once()

    def test_opcode_processed_regardless_of_source_address(self):
        """Source address filter only sets the online flag, not gate opcodes."""
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90, 95, 85],
                                               source_address=(9, 9)))
        # Fields ARE still updated
        self.assertEqual(device.minimum_brightness, 10)
        # But online flag is NOT set (source doesn't match device address)
        self.assertIsNone(device.online)

    def test_online_flag_set_only_when_source_matches(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                               [10, 90, 95, 85],
                                               source_address=(9, 9)))
        self.assertIsNone(device.online)

        device2 = _make_dimmer()
        device2._telegram_received_cb(_telegram(OperateCode.ReadLimitOfEveryChannelResponse,
                                                [10, 90, 95, 85],
                                                source_address=DEVICE_ADDRESS))
        self.assertTrue(device2.online)


class TestDimmerReadChannelLoadTypeResponse(unittest.TestCase):
    """Opcode 0xF013 — load type per channel.
    payload[0..channel_count-1] = load type values.
    Guard: len(payload) >= channel_count.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_load_types_parsed(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadChannelLoadTypeResponse,
                                               [1, 2, 3],
                                               source_address=DEVICE_ADDRESS))
        self.assertEqual(device.load_type(1), 1)
        self.assertEqual(device.load_type(2), 2)
        self.assertEqual(device.load_type(3), 3)

    def test_short_payload_ignored(self):
        device = _make_dimmer()
        # channel_count=3 requires 3 bytes; only 2 provided
        device._telegram_received_cb(_telegram(OperateCode.ReadChannelLoadTypeResponse,
                                               [1, 2],
                                               source_address=DEVICE_ADDRESS))
        device._call_device_updated.assert_not_called()
        self.assertIsNone(device.load_type(1))

    def test_exactly_minimum_payload_accepted(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadChannelLoadTypeResponse,
                                               [5, 6, 7],
                                               source_address=DEVICE_ADDRESS))
        device._call_device_updated.assert_called_once()

    def test_opcode_processed_regardless_of_source_address(self):
        """Source address filter only sets the online flag, not gate opcodes."""
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadChannelLoadTypeResponse,
                                               [1, 2, 3],
                                               source_address=(9, 9)))
        self.assertEqual(device.load_type(1), 1)

    def test_different_load_types(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.ReadChannelLoadTypeResponse,
                                               [0, 1, 2],
                                               source_address=DEVICE_ADDRESS))
        self.assertEqual(device.load_type(1), 0)
        self.assertEqual(device.load_type(2), 1)
        self.assertEqual(device.load_type(3), 2)


class TestDimmerIsDeviceOnlineResponse(unittest.TestCase):
    """Opcode 0xF066 — device online ping.
    Source address filter controls online flag.
    The opcode itself (0xF066) always triggers _call_device_updated regardless of source.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_online_flag_set_when_source_matches(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.IsDeviceOnlineResponse, [],
                                               source_address=DEVICE_ADDRESS))
        self.assertTrue(device.online)

    def test_online_flag_not_set_when_source_differs(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.IsDeviceOnlineResponse, [],
                                               source_address=(9, 9)))
        self.assertIsNone(device.online)

    def test_device_updated_called_for_matching_source(self):
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.IsDeviceOnlineResponse, [],
                                               source_address=DEVICE_ADDRESS))
        device._call_device_updated.assert_called()

    def test_device_updated_called_even_for_wrong_source(self):
        """IsDeviceOnlineResponse fires _call_device_updated regardless of source address."""
        device = _make_dimmer()
        device._telegram_received_cb(_telegram(OperateCode.IsDeviceOnlineResponse, [],
                                               source_address=(99, 99)))
        device._call_device_updated.assert_called()


if __name__ == "__main__":
    unittest.main()
