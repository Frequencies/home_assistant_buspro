"""Tests for Climate and FloorHeating telegram parsing."""

import struct
import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode, SuccessOrFailure, WorkType
from custom_components.buspro.pybuspro.devices.climate import Climate, FloorHeating
from custom_components.buspro.pybuspro.devices.climate_confirmable import (
    FloorHeating as FloorHeatingConfirmable,
    PanelAC as PanelACConfirmable,
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


def _make_climate():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = Climate(buspro, DEVICE_ADDRESS)
    device._call_device_updated = MagicMock()
    return device


def _make_floor_heating(channel_number=None):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = FloorHeating(buspro, DEVICE_ADDRESS, channel_number=channel_number)
    device._call_device_updated = MagicMock()
    return device


def _make_floor_heating_confirmable(channel_number=None):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = FloorHeatingConfirmable(buspro, DEVICE_ADDRESS, channel_number=channel_number)
    device._call_device_updated = MagicMock()
    return device


def _make_panel_ac_confirmable():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = PanelACConfirmable(buspro, DEVICE_ADDRESS)
    device._call_device_updated = MagicMock()
    return device


class TestClimateReadPanelACResponse(unittest.TestCase):
    """Opcode 0xE3DB — panel AC status.
    command byte at payload[0]: 3 → status+mode; 4 → current+target temperature.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_command3_sets_status_and_mode(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [3, 1]))
        self.assertEqual(device._status, 1)
        self.assertEqual(device._mode, 1)
        self.assertTrue(device.is_on)

    def test_command3_off(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [3, 0]))
        self.assertEqual(device._status, 0)
        self.assertFalse(device.is_on)

    def test_command4_sets_temperature(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [4, 23]))
        self.assertEqual(device.temperature, 23)
        self.assertEqual(device.target_temperature, 23)

    def test_command_other_no_update(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [9, 50]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_no_update(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [3]))
        device._call_device_updated.assert_not_called()

    def test_control_opcode_same_parsing(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.ControlPanelACResponse, [3, 1]))
        self.assertEqual(device._status, 1)


class TestClimateBroadcastTemperatureResponse(unittest.TestCase):
    """Opcode 0xE3E5 — temperature broadcast for Climate (Panel AC)."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_temperature_at_payload_1(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.BroadcastTemperatureResponse, [0, 21]))
        self.assertEqual(device.temperature, 21)

    def test_short_payload_no_update(self):
        device = _make_climate()
        device._telegram_received_cb(_telegram(OperateCode.BroadcastTemperatureResponse, [0]))
        device._call_device_updated.assert_not_called()


class TestFloorHeatingReadStatusResponse(unittest.TestCase):
    """Opcode 0x1945 in FloorHeating (climate.py).
    Layout: [temp_type, current_temp, status, mode, normal, day, night, away] (8 bytes min).
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, temp_type=0, temp=22, status=1, mode=1,
                 normal=20, day=23, night=18, away=16):
        return [temp_type, temp, status, mode, normal, day, night, away]

    def test_all_fields_parsed(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload()))
        self.assertEqual(device.temperature, 22)
        self.assertEqual(device._status, 1)
        self.assertEqual(device._mode, 1)
        self.assertEqual(device._normal_temperature, 20)
        self.assertEqual(device._day_temperature, 23)
        self.assertEqual(device._night_temperature, 18)
        self.assertEqual(device._away_temperature, 16)

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               [0, 22, 1]))
        device._call_device_updated.assert_not_called()

    def test_is_on_when_status_1(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(status=1)))
        self.assertTrue(device.is_on)

    def test_is_off_when_status_0(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(status=0)))
        self.assertFalse(device.is_on)

    def test_temperature_type_parsed(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(temp_type=1)))
        self.assertEqual(device._temperature_type, 1)


class TestFloorHeatingControlStatusResponse(unittest.TestCase):
    """Opcode 0x1947 in FloorHeating (climate.py).
    payload[0] = success/fail; only fires update on success.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_success_updates_all_fields(self):
        device = _make_floor_heating()
        payload = [SuccessOrFailure.Success.value[0], 0, 1, 2, 20, 23, 18, 16]
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingStatusResponse, payload))
        self.assertEqual(device._status, 1)
        self.assertEqual(device._mode, 2)
        device._call_device_updated.assert_called_once()

    def test_failure_no_update(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingStatusResponse,
                                               [0x00, 0, 1, 2, 20, 23, 18, 16]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingStatusResponse,
                                               [SuccessOrFailure.Success.value[0], 0]))
        device._call_device_updated.assert_not_called()


class TestFloorHeatingModuleStatusResponse(unittest.TestCase):
    """Opcode 0x1C5F — module floor heating.
    work byte at payload[1]: lower nibble = on/off, upper nibble = work_type.
    valve at payload[9]; watering_time at payload[12]. Min 13 bytes.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, channel=0, work=0x01, temp_type=0, mode=1,
                 normal=20, day=23, night=18, away=16, p8=0, valve=1, p10=0, p11=0, watering=5):
        return [channel, work, temp_type, mode, normal, day, night, away, p8, valve, p10, p11, watering]

    def test_status_on_from_lower_nibble(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(work=0x01)))
        self.assertEqual(device._status, 1)
        self.assertTrue(device.is_on)

    def test_status_off_from_lower_nibble(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(work=0x10)))
        self.assertEqual(device._status, 0)
        self.assertFalse(device.is_on)

    def test_work_type_from_upper_nibble(self):
        device = _make_floor_heating()
        # work=0x11 → upper nibble = 1 → WorkType.Cooling
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(work=0x11)))
        self.assertEqual(device._work_type, WorkType.Cooling)

    def test_heating_work_type(self):
        device = _make_floor_heating()
        # upper nibble = 0 → WorkType.Heating
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(work=0x01)))
        self.assertEqual(device._work_type, WorkType.Heating)

    def test_valve_at_payload_9(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(valve=1)))
        self.assertEqual(device._valve, 1)

    def test_watering_time_at_payload_12(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(watering=7)))
        self.assertEqual(device._watering_time, 7)

    def test_channel_filter_match(self):
        device = _make_floor_heating(channel_number=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(channel=2, work=0x01)))
        self.assertEqual(device._status, 1)

    def test_channel_filter_mismatch_ignored(self):
        device = _make_floor_heating(channel_number=2)
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(channel=3, work=0x01)))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               [0, 0x01, 0]))
        device._call_device_updated.assert_not_called()

    def test_all_temperatures_parsed(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingModuleStatusResponse,
                                               self._payload(normal=21, day=25, night=17, away=15)))
        self.assertEqual(device._normal_temperature, 21)
        self.assertEqual(device._day_temperature, 25)
        self.assertEqual(device._night_temperature, 17)
        self.assertEqual(device._away_temperature, 15)


class TestFloorHeatingControlModuleStatusResponse(unittest.TestCase):
    """Opcode 0x1C5D — control response for module floor heating.
    valve at payload[8] and watering_time at payload[9] (different from ReadModule!).
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, channel=0, work=0x01, temp_type=0, mode=1,
                 normal=20, day=23, night=18, away=16, valve=1, watering=5):
        return [channel, work, temp_type, mode, normal, day, night, away, valve, watering]

    def test_valve_at_payload_8_not_9(self):
        """ControlModule puts valve at [8]; ReadModule puts it at [9]."""
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingModuleStatusResponse,
                                               self._payload(valve=1)))
        self.assertEqual(device._valve, 1)

    def test_watering_at_payload_9_not_12(self):
        """ControlModule puts watering_time at [9]; ReadModule puts it at [12]."""
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingModuleStatusResponse,
                                               self._payload(watering=3)))
        self.assertEqual(device._watering_time, 3)

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingModuleStatusResponse,
                                               [0, 0x01]))
        device._call_device_updated.assert_not_called()

    def test_status_parsed(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ControlFloorHeatingModuleStatusResponse,
                                               self._payload(work=0x01)))
        self.assertEqual(device._status, 1)


class TestFloorHeatingTemperatureNewResponse(unittest.TestCase):
    """Opcode 0x1949 — little-endian IEEE 754 float at payload[1:5]."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, temp_float, channel=0):
        raw = list(struct.pack("<f", temp_float))
        return [channel] + raw

    def test_positive_temperature(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               self._payload(22.5)))
        self.assertAlmostEqual(device.temperature, 22.5, places=3)

    def test_negative_temperature(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               self._payload(-5.0)))
        self.assertAlmostEqual(device.temperature, -5.0, places=3)

    def test_zero_temperature(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               self._payload(0.0)))
        self.assertAlmostEqual(device.temperature, 0.0, places=3)

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               [0, 1, 2]))
        device._call_device_updated.assert_not_called()

    def test_channel_filter_match(self):
        device = _make_floor_heating(channel_number=1)
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               self._payload(25.0, channel=1)))
        self.assertAlmostEqual(device.temperature, 25.0, places=3)

    def test_channel_filter_mismatch_ignored(self):
        device = _make_floor_heating(channel_number=1)
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureNewResponse,
                                               self._payload(25.0, channel=2)))
        device._call_device_updated.assert_not_called()


class TestFloorHeatingTemperatureLegacyResponse(unittest.TestCase):
    """Opcode 0xE3E8 — signed 7-bit temperature.
    raw >> 7 = sign bit (1 = negative); raw & 0x7F = magnitude.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, raw_temp, channel=0):
        return [channel, raw_temp]

    def test_positive_temperature(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(25)))
        self.assertEqual(device.temperature, 25)

    def test_negative_temperature(self):
        # 0x85 = 1000_0101b → sign=1, magnitude=5 → -5
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(0x85)))
        self.assertEqual(device.temperature, -5)

    def test_zero(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(0)))
        self.assertEqual(device.temperature, 0)

    def test_max_positive(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(0x7F)))  # sign=0, mag=127 → +127
        self.assertEqual(device.temperature, 127)

    def test_min_negative(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(0xFF)))  # sign=1, mag=127 → -127
        self.assertEqual(device.temperature, -127)

    def test_short_payload_ignored(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               [0]))
        device._call_device_updated.assert_not_called()

    def test_channel_filter_mismatch_ignored(self):
        device = _make_floor_heating(channel_number=1)
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingTemperatureLegacyResponse,
                                               self._payload(25, channel=2)))
        device._call_device_updated.assert_not_called()


class TestFloorHeatingBroadcastTemperature(unittest.TestCase):
    """Opcode 0xE3E5 — temperature broadcast for FloorHeating."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_temperature_at_payload_1(self):
        device = _make_floor_heating()
        device._telegram_received_cb(_telegram(OperateCode.BroadcastTemperatureResponse, [0, 19]))
        self.assertEqual(device.temperature, 19)


class TestFloorHeatingConfirmableReadStatusResponse(unittest.TestCase):
    """Opcode 0x1945 in FloorHeatingConfirmable (climate_confirmable.py).

    DIFFERENT layout from climate.py FloorHeating for the same opcode:
      climate.py:    [temp_type, current_temp, status, mode, ...]
      confirmable:   [temp_type, status, mode, current_temp, ...]
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def _payload(self, temp_type=0, status=1, mode=2, temp=23,
                 normal=21, day=25, night=18, away=16):
        return [temp_type, status, mode, temp, normal, day, night, away]

    def test_temperature_at_payload_3(self):
        device = _make_floor_heating_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(temp=23)))
        self.assertEqual(device.temperature, 23)

    def test_status_at_payload_1(self):
        device = _make_floor_heating_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(status=1)))
        self.assertTrue(device.is_on)

    def test_mode_at_payload_2(self):
        device = _make_floor_heating_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               self._payload(mode=3)))
        self.assertEqual(device._mode, 3)

    def test_short_payload_ignored(self):
        device = _make_floor_heating_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse,
                                               [0, 1, 2]))
        device._call_device_updated.assert_not_called()

    def test_layout_differs_from_nonconfirmable_for_same_payload(self):
        """With the same raw bytes, confirmable and non-confirmable parse different fields.
        climate.py: temp at [1]; confirmable: temp at [3].
        """
        payload = [0, 1, 2, 99, 20, 25, 18, 16]

        confirmable = _make_floor_heating_confirmable()
        confirmable._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse, payload))

        legacy = _make_floor_heating()
        legacy._telegram_received_cb(_telegram(OperateCode.ReadFloorHeatingStatusResponse, payload))

        # confirmable reads temp at [3]=99; legacy reads temp at [1]=1
        self.assertEqual(confirmable.temperature, 99)
        self.assertEqual(legacy.temperature, 1)


class TestPanelACConfirmableReadPanelACResponse(unittest.TestCase):
    """PanelAC (climate_confirmable.py) — same parsing as Climate plus mark_confirmed."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_command3_sets_status_and_mode(self):
        device = _make_panel_ac_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [3, 1]))
        self.assertEqual(device._status, 1)
        self.assertEqual(device._mode, 1)

    def test_command4_sets_temperature(self):
        device = _make_panel_ac_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [4, 24]))
        self.assertEqual(device.temperature, 24)

    def test_broadcast_temperature(self):
        device = _make_panel_ac_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.BroadcastTemperatureResponse, [0, 20]))
        self.assertEqual(device.temperature, 20)

    def test_short_payload_no_update(self):
        device = _make_panel_ac_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadPanelACResponse, [3]))
        device._call_device_updated.assert_not_called()


if __name__ == "__main__":
    unittest.main()
