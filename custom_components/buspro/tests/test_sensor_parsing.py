"""Tests for Sensor telegram parsing — temperature, illuminance, humidity, motion, dry contacts."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode, SuccessOrFailure
from custom_components.buspro.pybuspro.devices.sensor import Sensor

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)


def _no_op_ensure_future(coro):
    """Close the coroutine immediately so Python doesn't warn about it."""
    try:
        coro.close()
    except AttributeError:
        pass
    return MagicMock(done=lambda: True, cancel=lambda: None)


def _make_sensor():
    """Instantiate a Sensor with a minimal buspro stub and no event-loop side-effects."""
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        sensor = Sensor(buspro, DEVICE_ADDRESS)
    sensor._call_device_updated = MagicMock()
    return sensor


def _telegram(operate_code, payload, target_address=None, source_address=None):
    t = Telegram()
    t.operate_code = operate_code
    t.payload = payload
    t.target_address = target_address or (0, 0)
    t.source_address = source_address or DEVICE_ADDRESS
    return t


class TestReadSensorStatusResponse(unittest.TestCase):
    """Opcode 0x1646 — polled read, addressed unicast to client."""

    def _addressed_to_client(self, payload):
        return _telegram(
            OperateCode.ReadSensorStatusResponse,
            payload,
            target_address=CLIENT_ADDRESS,
        )

    def _not_addressed_to_client(self, payload):
        return _telegram(
            OperateCode.ReadSensorStatusResponse,
            payload,
            target_address=(9, 9),
        )

    def test_temperature_parsed_when_addressed_to_client(self):
        sensor = _make_sensor()
        # payload: [success, temp, bri_hi, bri_lo, motion, sonic, dc1, dc2]
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 23, 0, 0, 0, 0, 0, 0])
        )
        self.assertEqual(sensor.temperature, 23)

    def test_temperature_not_updated_when_not_addressed_to_client(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._not_addressed_to_client([SuccessOrFailure.Success.value[0], 25, 0, 0, 0, 0, 0, 0])
        )
        # temperature stays at default (0 via property)
        self.assertEqual(sensor.temperature, 0)

    def test_brightness_two_byte_big_endian(self):
        sensor = _make_sensor()
        # 500 lx = 0x01F4 → high=0x01, low=0xF4
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0x01, 0xF4, 0, 0, 0, 0])
        )
        self.assertEqual(sensor.brightness, 500)

    def test_brightness_max_value(self):
        sensor = _make_sensor()
        # 65535 lx = 0xFFFF
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0xFF, 0xFF, 0, 0, 0, 0])
        )
        self.assertEqual(sensor.brightness, 65535)

    def test_brightness_zero(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0, 0, 0, 0, 0, 0])
        )
        self.assertEqual(sensor.brightness, 0)

    def test_motion_detected(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0, 0, 1, 0, 0, 0])
        )
        self.assertTrue(sensor.movement)

    def test_no_motion(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0, 0, 0, 0, 0, 0])
        )
        self.assertFalse(sensor.movement)

    def test_dry_contact_1_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0, 0, 0, 0, 1, 0])
        )
        self.assertTrue(sensor.dry_contact_1_is_on)

    def test_dry_contact_2_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 0, 0, 0, 0, 0, 0, 1])
        )
        self.assertTrue(sensor.dry_contact_2_is_on)

    def test_failure_response_does_not_fire_device_updated(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([0x00, 25, 0, 100, 1, 0, 1, 1])  # 0x00 = not success
        )
        sensor._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            self._addressed_to_client([SuccessOrFailure.Success.value[0], 20])  # only 2 bytes
        )
        # Nothing should crash and temperature stays default
        self.assertEqual(sensor.temperature, 0)


class TestReadSensorsInOneStatusResponse(unittest.TestCase):
    """Opcode 0x1605 — polled sensors-in-one (MSP02.4C etc).
    Temperature is raw + 20 offset (raw 49 → 29 °C).
    Humidity 0xFF means no sensor → None.
    """

    def _telegram(self, payload):
        return _telegram(
            OperateCode.ReadSensorsInOneStatusResponse,
            payload,
            target_address=CLIENT_ADDRESS,
        )

    def _payload(self, raw_temp=49, bri_hi=0, bri_lo=0, humidity=0, motion=0, dc1=0, dc2=0):
        # Minimum 10 bytes: [?, raw_temp, bri_hi, bri_lo, humidity, ?, ?, motion, dc1, dc2]
        return [0, raw_temp, bri_hi, bri_lo, humidity, 0, 0, motion, dc1, dc2]

    def test_temperature_offset_subtracted(self):
        sensor = _make_sensor()
        # raw 49 → 29 °C (HDL-MSP02.4C confirmed value)
        sensor._handle_telegram(self._telegram(self._payload(raw_temp=49)))
        self.assertEqual(sensor.temperature, 29)

    def test_temperature_zero_celsius_raw_20(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(raw_temp=20)))
        self.assertEqual(sensor.temperature, 0)

    def test_temperature_negative(self):
        sensor = _make_sensor()
        # raw 15 → -5 °C
        sensor._handle_telegram(self._telegram(self._payload(raw_temp=15)))
        self.assertEqual(sensor.temperature, -5)

    def test_humidity_normal(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(humidity=65)))
        self.assertEqual(sensor.humidity, 65)

    def test_humidity_0xff_means_no_sensor(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(humidity=0xFF)))
        self.assertIsNone(sensor.humidity)

    def test_brightness_two_byte_big_endian(self):
        sensor = _make_sensor()
        # 1000 lx = 0x03E8
        sensor._handle_telegram(self._telegram(self._payload(bri_hi=0x03, bri_lo=0xE8)))
        self.assertEqual(sensor.brightness, 1000)

    def test_motion_detected(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(motion=1)))
        self.assertTrue(sensor.movement)

    def test_dry_contact_1_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(dc1=1)))
        self.assertTrue(sensor.dry_contact_1_is_on)

    def test_dry_contact_2_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram(self._payload(dc2=1)))
        self.assertTrue(sensor.dry_contact_2_is_on)

    def test_short_payload_ignored(self):
        sensor = _make_sensor()
        sensor._handle_telegram(
            _telegram(OperateCode.ReadSensorsInOneStatusResponse, [0, 49], target_address=CLIENT_ADDRESS)
        )
        self.assertEqual(sensor.temperature, 0)


class TestBroadcastSensorStatusResponse(unittest.TestCase):
    """Opcode 0x1644 — unsolicited broadcast from the sensor bus.
    Temperature is at payload[0] (no offset). Brightness at payload[1:3].
    """

    def _telegram(self, payload):
        return _telegram(OperateCode.BroadcastSensorStatusResponse, payload)

    def test_temperature_at_payload_0(self):
        sensor = _make_sensor()
        # payload: [temp, bri_hi, bri_lo, motion, sonic, dc1, dc2]
        sensor._handle_telegram(self._telegram([21, 0, 0, 0, 0, 0, 0]))
        self.assertEqual(sensor.temperature, 21)

    def test_brightness_two_byte_big_endian(self):
        sensor = _make_sensor()
        # 300 lx = 0x012C
        sensor._handle_telegram(self._telegram([0, 0x01, 0x2C, 0, 0, 0, 0]))
        self.assertEqual(sensor.brightness, 300)

    def test_motion_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0, 0, 1, 0, 0, 0]))
        self.assertTrue(sensor.movement)

    def test_sonic_triggers_movement(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0, 0, 0, 1, 0, 0]))
        self.assertTrue(sensor.movement)

    def test_no_motion_no_sonic(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0, 0, 0, 0, 0, 0]))
        self.assertFalse(sensor.movement)

    def test_dry_contact_1_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0, 0, 0, 0, 1, 0]))
        self.assertTrue(sensor.dry_contact_1_is_on)

    def test_dry_contact_2_on(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0, 0, 0, 0, 0, 1]))
        self.assertTrue(sensor.dry_contact_2_is_on)


class TestBroadcastSensorStatusAutoResponse(unittest.TestCase):
    """Opcode 0x1647 — same payload layout as 0x1644."""

    def _telegram(self, payload):
        return _telegram(OperateCode.BroadcastSensorStatusAutoResponse, payload)

    def test_temperature_parsed(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([18, 0, 0, 0, 0, 0, 0]))
        self.assertEqual(sensor.temperature, 18)

    def test_brightness_parsed(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 0x00, 0x96, 0, 0, 0, 0]))  # 150 lx
        self.assertEqual(sensor.brightness, 150)


class TestBroadcastLuminanceResponse(unittest.TestCase):
    """Opcode 0xE441 — periodic lux broadcast from sensors-in-one devices.
    Lux is at payload[2:4], other bytes ignored.
    """

    def _telegram(self, payload):
        return _telegram(OperateCode.BroadcastLuminanceResponse, payload)

    def test_brightness_at_offset_2_3(self):
        sensor = _make_sensor()
        # [?, 1, HIGH, LOW, ?, ?] — 750 lx = 0x02EE
        sensor._handle_telegram(self._telegram([0, 1, 0x02, 0xEE, 0, 0]))
        self.assertEqual(sensor.brightness, 750)

    def test_zero_brightness(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 1, 0x00, 0x00, 0, 0]))
        self.assertEqual(sensor.brightness, 0)

    def test_short_payload_ignored(self):
        """Fewer than 4 bytes → no update, no crash."""
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 1, 0x02]))
        # brightness stays None (not updated)
        self.assertIsNone(sensor.brightness)


class TestBroadcastTemperatureResponse(unittest.TestCase):
    """Opcode 0xE3E5 — temperature-only broadcast."""

    def _telegram(self, payload):
        return _telegram(OperateCode.BroadcastTemperatureResponse, payload)

    def test_temperature_at_payload_1(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 22]))
        self.assertEqual(sensor.temperature, 22)

    def test_temperature_does_not_affect_brightness(self):
        sensor = _make_sensor()
        sensor._handle_telegram(self._telegram([0, 22]))
        self.assertIsNone(sensor.brightness)


class TestMovementProperty(unittest.TestCase):
    """movement combines _motion_sensor and _sonic — both None means None, any non-zero means True."""

    def test_both_none_returns_none(self):
        sensor = _make_sensor()
        # Fresh sensor, neither field set → movement is None
        self.assertIsNone(sensor.movement)

    def test_motion_set_sonic_none(self):
        sensor = _make_sensor()
        sensor._motion_sensor = 1
        sensor._sonic = None
        self.assertTrue(sensor.movement)

    def test_sonic_set_motion_none(self):
        sensor = _make_sensor()
        sensor._motion_sensor = None
        sensor._sonic = 1
        self.assertTrue(sensor.movement)

    def test_both_zero_returns_false(self):
        sensor = _make_sensor()
        sensor._motion_sensor = 0
        sensor._sonic = 0
        self.assertFalse(sensor.movement)


if __name__ == "__main__":
    unittest.main()
