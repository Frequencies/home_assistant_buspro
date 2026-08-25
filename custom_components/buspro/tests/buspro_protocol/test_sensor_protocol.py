"""Regression tests for Buspro compound sensor protocol handling."""

import asyncio
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[2]))

from pybuspro.core.telegram import Telegram  # noqa: E402
from pybuspro.devices.sensor import Sensor  # noqa: E402
from pybuspro.helpers.enums import OperateCode  # noqa: E402


class _Network:
    def __init__(self):
        self.telegrams = []

    async def send_telegram(self, telegram):
        self.telegrams.append(telegram)


class _Bus:
    def __init__(self, loop):
        self.loop = loop
        self.client_address = (200, 200)
        self.network_interface = _Network()
        self.callbacks = []

    def register_telegram_received_device_cb(self, callback, address, postfix=None):
        self.callbacks.append((callback, address, postfix))

    def unregister_telegram_received_device_cb(self, callback, address, postfix=None):
        self.callbacks.remove((callback, address, postfix))


class SensorProtocolTest(unittest.IsolatedAsyncioTestCase):
    async def test_standard_status_decodes_all_values(self):
        bus = _Bus(asyncio.get_running_loop())
        sensor = Sensor(bus, (2, 13))
        telegram = Telegram()
        telegram.operate_code = OperateCode.ReadSensorStatusResponse
        telegram.target_address = bus.client_address
        telegram.payload = [0xF8, 23, 0x01, 0x2C, 1, 0, 1, 0]

        sensor._telegram_received_cb(telegram)
        await asyncio.sleep(0)

        self.assertEqual(sensor.temperature, 23)
        self.assertEqual(sensor.brightness, 300)
        self.assertTrue(sensor.movement)
        self.assertTrue(sensor.dry_contact_1_is_on)
        self.assertFalse(sensor.dry_contact_2_is_on)
        sensor.close()

    async def test_standard_and_sensors_in_one_use_distinct_queries(self):
        loop = asyncio.get_running_loop()
        standard_bus = _Bus(loop)
        standard = Sensor(standard_bus, (2, 13))
        sensors_in_one_bus = _Bus(loop)
        sensors_in_one = Sensor(sensors_in_one_bus, (2, 14), device="sensors_in_one")

        await standard.read_sensor_status()
        await sensors_in_one.read_sensor_status()

        self.assertEqual(
            standard_bus.network_interface.telegrams[-1].operate_code,
            OperateCode.ReadSensorStatus,
        )
        self.assertEqual(
            sensors_in_one_bus.network_interface.telegrams[-1].operate_code,
            OperateCode.ReadSensorsInOneStatus,
        )
        standard.close()
        sensors_in_one.close()

    async def test_sensors_in_one_decodes_humidity_and_contacts(self):
        bus = _Bus(asyncio.get_running_loop())
        sensor = Sensor(bus, (2, 10), device="sensors_in_one")
        telegram = Telegram()
        telegram.operate_code = OperateCode.ReadSensorsInOneStatusResponse
        telegram.target_address = bus.client_address
        # payload[1] carries temperature with a +20 offset (41 -> 21 C).
        telegram.payload = [0xF8, 41, 0x00, 0x7B, 46, 0, 0, 1, 0, 1]

        sensor._telegram_received_cb(telegram)
        await asyncio.sleep(0)

        self.assertEqual(sensor.temperature, 21)
        self.assertEqual(sensor.brightness, 123)
        self.assertEqual(sensor.humidity, 46)
        self.assertTrue(sensor.movement)
        self.assertFalse(sensor.dry_contact_1_is_on)
        self.assertTrue(sensor.dry_contact_2_is_on)
        sensor.close()

    async def test_sensors_in_one_decodes_real_msp02_frame(self):
        """Regression for the captured HDL-MSP02.4C 0x1605 response.

        Real frame observed while polling 2/14 with ReadSensorsInOneStatus:
        temperature raw 49 -> 29 C (matches the device's 0xE3E5 broadcast),
        lux in payload[2..3], motion in payload[7], and 0xFF humidity because
        this model has no humidity sensor.
        """
        bus = _Bus(asyncio.get_running_loop())
        sensor = Sensor(bus, (2, 14), device="sensors_in_one")
        telegram = Telegram()
        telegram.operate_code = OperateCode.ReadSensorsInOneStatusResponse
        telegram.target_address = bus.client_address
        telegram.payload = [248, 49, 0, 6, 255, 255, 255, 1, 0, 0, 0, 0, 255]

        sensor._telegram_received_cb(telegram)
        await asyncio.sleep(0)

        self.assertEqual(sensor.temperature, 29)
        self.assertEqual(sensor.brightness, 6)
        self.assertIsNone(sensor.humidity)
        self.assertTrue(sensor.movement)
        sensor.close()


if __name__ == "__main__":
    unittest.main()
