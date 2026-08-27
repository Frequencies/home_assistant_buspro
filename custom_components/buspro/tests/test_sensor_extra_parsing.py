"""Tests for Sensor telegram parsing — universal switch, channel, dry contact branches."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.sensor import Sensor

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


def _make_sensor_universal(switch_number=3, motion_uv_switch=None):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        s = Sensor(buspro, DEVICE_ADDRESS, universal_switch_number=switch_number,
                   motion_uv_switch=motion_uv_switch)
    s._call_device_updated = MagicMock()
    return s


def _make_sensor_channel(channel_number=2):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        s = Sensor(buspro, DEVICE_ADDRESS, channel_number=channel_number)
    s._call_device_updated = MagicMock()
    return s


def _make_sensor_switch(switch_number=1):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        s = Sensor(buspro, DEVICE_ADDRESS, switch_number=switch_number)
    s._call_device_updated = MagicMock()
    return s


class TestSensorReadStatusOfUniversalSwitchResponse(unittest.TestCase):
    """Opcode 0xE019 — polled universal switch status in Sensor.
    payload[0] = switch_number returned by device, payload[1] = status.
    Matches when payload[0] == self._universal_switch_number.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_switch_updates_status(self):
        sensor = _make_sensor_universal(switch_number=3)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse, [3, 1]))
        self.assertEqual(sensor._universal_switch_status, 1)

    def test_non_matching_switch_ignored(self):
        sensor = _make_sensor_universal(switch_number=3)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse, [5, 1]))
        sensor._call_device_updated.assert_not_called()

    def test_off_status(self):
        sensor = _make_sensor_universal(switch_number=2)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse, [2, 0]))
        self.assertEqual(sensor._universal_switch_status, 0)
        self.assertFalse(sensor.universal_switch_is_on)

    def test_on_status(self):
        sensor = _make_sensor_universal(switch_number=1)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfUniversalSwitchResponse, [1, 1]))
        self.assertTrue(sensor.universal_switch_is_on)


class TestSensorBroadcastStatusOfUniversalSwitch(unittest.TestCase):
    """Opcode 0xE017 — broadcast of all switch statuses.
    payload[0] = count; payload[switch_number] = status (direct index).
    Guard: switch_number <= payload[0].
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_status_read_by_switch_number_index(self):
        sensor = _make_sensor_universal(switch_number=3)
        # payload[0]=4 (count), payload[3]=1 (our switch is ON)
        sensor._handle_telegram(_telegram(OperateCode.BroadcastStatusOfUniversalSwitch,
                                          [4, 0, 0, 1, 0]))
        self.assertEqual(sensor._universal_switch_status, 1)

    def test_switch_number_exceeds_count_ignored(self):
        sensor = _make_sensor_universal(switch_number=5)
        # count=3, switch 5 > 3 → ignored
        sensor._handle_telegram(_telegram(OperateCode.BroadcastStatusOfUniversalSwitch,
                                          [3, 0, 0, 0]))
        sensor._call_device_updated.assert_not_called()

    def test_switch_number_equals_count_accepted(self):
        sensor = _make_sensor_universal(switch_number=3)
        # count=3, switch_number=3 <= 3
        sensor._handle_telegram(_telegram(OperateCode.BroadcastStatusOfUniversalSwitch,
                                          [3, 0, 0, 1]))
        self.assertEqual(sensor._universal_switch_status, 1)

    def test_no_universal_switch_number_ignored(self):
        buspro = MagicMock()
        buspro.client_address = CLIENT_ADDRESS
        with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
            sensor = Sensor(buspro, DEVICE_ADDRESS)
        sensor._call_device_updated = MagicMock()
        sensor._handle_telegram(_telegram(OperateCode.BroadcastStatusOfUniversalSwitch,
                                          [4, 1, 1, 1, 1]))
        sensor._call_device_updated.assert_not_called()

    def test_off_status_at_index(self):
        sensor = _make_sensor_universal(switch_number=2)
        sensor._handle_telegram(_telegram(OperateCode.BroadcastStatusOfUniversalSwitch,
                                          [3, 0, 0, 0]))
        self.assertFalse(sensor.universal_switch_is_on)


class TestSensorUniversalSwitchControlResponse(unittest.TestCase):
    """Opcode 0xE01D — universal switch state change echo in Sensor.
    payload[0] = switch_number, payload[1] = status.
    Updates _universal_switch_status if matches, or _motion_sensor if motion_uv_switch.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_switch_updates_universal_status(self):
        sensor = _make_sensor_universal(switch_number=2)
        sensor._handle_telegram(_telegram(OperateCode.UniversalSwitchControlResponse, [2, 1]))
        self.assertEqual(sensor._universal_switch_status, 1)

    def test_non_matching_switch_ignored(self):
        sensor = _make_sensor_universal(switch_number=2)
        sensor._handle_telegram(_telegram(OperateCode.UniversalSwitchControlResponse, [7, 1]))
        sensor._call_device_updated.assert_not_called()

    def test_motion_uv_switch_updates_motion_sensor(self):
        sensor = _make_sensor_universal(switch_number=2, motion_uv_switch=5)
        sensor._handle_telegram(_telegram(OperateCode.UniversalSwitchControlResponse, [5, 1]))
        self.assertEqual(sensor._motion_sensor, 1)
        self.assertTrue(sensor.movement)

    def test_motion_uv_switch_off(self):
        sensor = _make_sensor_universal(switch_number=2, motion_uv_switch=5)
        sensor._motion_sensor = 1
        sensor._handle_telegram(_telegram(OperateCode.UniversalSwitchControlResponse, [5, 0]))
        self.assertEqual(sensor._motion_sensor, 0)

    def test_universal_switch_off(self):
        sensor = _make_sensor_universal(switch_number=3)
        sensor._universal_switch_status = 1
        sensor._handle_telegram(_telegram(OperateCode.UniversalSwitchControlResponse, [3, 0]))
        self.assertFalse(sensor.universal_switch_is_on)


class TestSensorReadStatusOfChannelsResponse(unittest.TestCase):
    """Opcode 0x0034 — channel status read in Sensor context.
    payload[0] = count; payload[channel_number] = status.
    Requires _channel_number set; logs warning if None.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_channel_status_updated(self):
        sensor = _make_sensor_channel(channel_number=2)
        # payload[0]=4 (count), payload[2]=1 (our channel)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                          [4, 0, 1, 0, 0]))
        self.assertEqual(sensor._channel_status, 1)

    def test_channel_number_exceeds_count_ignored(self):
        sensor = _make_sensor_channel(channel_number=5)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                          [3, 0, 0, 0]))
        sensor._call_device_updated.assert_not_called()

    def test_no_channel_number_ignored(self):
        buspro = MagicMock()
        buspro.client_address = CLIENT_ADDRESS
        with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
            sensor = Sensor(buspro, DEVICE_ADDRESS)
        sensor._call_device_updated = MagicMock()
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                          [4, 0, 1, 0, 0]))
        sensor._call_device_updated.assert_not_called()

    def test_channel_off(self):
        sensor = _make_sensor_channel(channel_number=1)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfChannelsResponse, [2, 0, 0]))
        self.assertEqual(sensor._channel_status, 0)
        self.assertFalse(sensor.single_channel_is_on)

    def test_channel_on(self):
        sensor = _make_sensor_channel(channel_number=1)
        sensor._handle_telegram(_telegram(OperateCode.ReadStatusOfChannelsResponse, [2, 100, 0]))
        self.assertTrue(sensor.single_channel_is_on)


class TestSensorSingleChannelControlResponse(unittest.TestCase):
    """Opcode 0x0032 — channel control echo in Sensor.
    payload[0] = channel_number, payload[2] = level.
    Guard: payload[0] == self._channel_number.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_updates_status(self):
        sensor = _make_sensor_channel(channel_number=2)
        sensor._handle_telegram(_telegram(OperateCode.SingleChannelControlResponse, [2, 0xF8, 75]))
        self.assertEqual(sensor._channel_status, 75)

    def test_non_matching_channel_ignored(self):
        sensor = _make_sensor_channel(channel_number=2)
        sensor._handle_telegram(_telegram(OperateCode.SingleChannelControlResponse, [3, 0xF8, 75]))
        sensor._call_device_updated.assert_not_called()

    def test_channel_on(self):
        sensor = _make_sensor_channel(channel_number=1)
        sensor._handle_telegram(_telegram(OperateCode.SingleChannelControlResponse, [1, 0xF8, 100]))
        self.assertTrue(sensor.single_channel_is_on)

    def test_channel_off(self):
        sensor = _make_sensor_channel(channel_number=1)
        sensor._handle_telegram(_telegram(OperateCode.SingleChannelControlResponse, [1, 0xF8, 0]))
        self.assertFalse(sensor.single_channel_is_on)


class TestSensorReadDryContactStatusResponse(unittest.TestCase):
    """Opcode 0x15CF — dry contact status in Sensor.
    payload[1] = switch_number (index 1, not 0!), payload[2] = status.
    Guard: payload[1] == self._switch_number.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_switch_updates_status(self):
        sensor = _make_sensor_switch(switch_number=1)
        # [ignored, switch_number, status]
        sensor._handle_telegram(_telegram(OperateCode.ReadDryContactStatusResponse, [0, 1, 1]))
        self.assertEqual(sensor._switch_status, 1)
        self.assertTrue(sensor.switch_status)

    def test_non_matching_switch_ignored(self):
        sensor = _make_sensor_switch(switch_number=1)
        sensor._handle_telegram(_telegram(OperateCode.ReadDryContactStatusResponse, [0, 2, 1]))
        sensor._call_device_updated.assert_not_called()

    def test_switch_off(self):
        sensor = _make_sensor_switch(switch_number=3)
        sensor._handle_telegram(_telegram(OperateCode.ReadDryContactStatusResponse, [0, 3, 0]))
        self.assertFalse(sensor.switch_status)

    def test_switch_number_at_payload_1_not_0(self):
        """Guard uses payload[1] for switch number, not payload[0]."""
        sensor = _make_sensor_switch(switch_number=1)
        # payload[0]=1 (would match if checked at [0]), payload[1]=2 (doesn't match at [1])
        sensor._handle_telegram(_telegram(OperateCode.ReadDryContactStatusResponse, [1, 2, 1]))
        sensor._call_device_updated.assert_not_called()


class TestSensorReadFloorHeatingStatusResponseInSensorContext(unittest.TestCase):
    """Opcode 0x1945 — floor heating response also handled by Sensor.
    Only sets temperature at payload[1].
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_temperature_at_payload_1(self):
        buspro = MagicMock()
        buspro.client_address = CLIENT_ADDRESS
        with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
            sensor = Sensor(buspro, DEVICE_ADDRESS)
        sensor._call_device_updated = MagicMock()
        sensor._handle_telegram(_telegram(OperateCode.ReadFloorHeatingStatusResponse, [0, 22]))
        self.assertEqual(sensor.temperature, 22)

    def test_device_updated_called(self):
        buspro = MagicMock()
        buspro.client_address = CLIENT_ADDRESS
        with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
            sensor = Sensor(buspro, DEVICE_ADDRESS)
        sensor._call_device_updated = MagicMock()
        sensor._handle_telegram(_telegram(OperateCode.ReadFloorHeatingStatusResponse, [0, 28]))
        sensor._call_device_updated.assert_called_once()


if __name__ == "__main__":
    unittest.main()
