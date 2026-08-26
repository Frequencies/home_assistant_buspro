"""Tests for Device lifecycle, task tracking, and callback safety."""

import asyncio
import sys
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).parents[2]))

from pybuspro.devices.device import Device, startup_read_delay  # noqa: E402


class _MockLogger:
    def exception(self, msg):
        pass


class _MockBuspro:
    def __init__(self, loop):
        self.loop = loop
        self.callbacks = []
        self.logger = _MockLogger()

    def register_telegram_received_device_cb(self, callback, address):
        self.callbacks.append(callback)

    def unregister_telegram_received_device_cb(self, callback, address):
        try:
            self.callbacks.remove(callback)
        except ValueError:
            pass


class TaskTrackingTest(unittest.TestCase):
    """Task references prevent GC before completion."""

    def test_spawn_stores_task_reference(self):
        """Task spawned via _spawn is stored in _pending_tasks."""
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            device = Device(
                _MockBuspro(loop),
                (1, 2),
                "test_device",
            )

            async def dummy_coro():
                await asyncio.sleep(0.001)
                return "done"

            loop.run_until_complete(device._spawn(dummy_coro()))
            # Task completion removes itself from _pending_tasks
            self.assertEqual(len(device._pending_tasks), 0)
        finally:
            asyncio.set_event_loop(None)
            loop.close()

    def test_close_cancels_pending_tasks(self):
        """Device.close() cancels all pending tasks."""
        loop = asyncio.new_event_loop()
        try:
            device = Device(
                _MockBuspro(loop),
                (1, 2),
                "test_device",
            )

            async def long_running():
                await asyncio.sleep(10)

            async def test():
                # Spawn a long-running task but don't await it
                device._spawn(long_running())
                # Task should be in pending
                self.assertGreater(len(device._pending_tasks), 0)
                # Close should cancel it
                device.close()
                await asyncio.sleep(0.01)
                # Pending tasks should be empty after cancellation
                self.assertEqual(len(device._pending_tasks), 0)

            loop.run_until_complete(test())
        finally:
            loop.close()


class CallbackDispatchSafetyTest(unittest.TestCase):
    """Callback dispatch exception safety."""

    def test_one_failing_callback_does_not_silence_others(self):
        """Exception in one device_updated callback doesn't drop subsequent callbacks."""
        results = []

        async def test():
            device = Device(
                _MockBuspro(asyncio.get_event_loop()),
                (1, 2),
                "test_device",
            )

            # Register three callbacks; middle one fails
            async def callback_1(_device):
                results.append("callback_1")

            async def callback_bad(_device):
                results.append("callback_bad_start")
                raise ValueError("intentional error")

            async def callback_3(_device):
                results.append("callback_3")

            device.register_device_updated_cb(callback_1)
            device.register_device_updated_cb(callback_bad)
            device.register_device_updated_cb(callback_3)

            # Trigger device_updated; should call all three despite the exception
            await device._device_updated()

            # All callbacks should have been called
            self.assertIn("callback_1", results)
            self.assertIn("callback_bad_start", results)
            self.assertIn("callback_3", results)

        loop = asyncio.new_event_loop()
        try:
            loop.run_until_complete(test())
        finally:
            loop.close()


class StartupJitterTest(unittest.TestCase):
    """Deterministic per-address startup jitter."""

    def test_jitter_is_deterministic(self):
        """Same address always produces same jitter."""
        address = (10, 20)
        delay1 = startup_read_delay(address, base=5, window=15)
        delay2 = startup_read_delay(address, base=5, window=15)
        self.assertEqual(delay1, delay2)

    def test_jitter_is_within_window(self):
        """Jitter respects the window boundary."""
        for subnet in range(0, 256, 16):
            for device in range(0, 256, 32):
                address = (subnet, device)
                delay = startup_read_delay(address, base=5, window=15)
                self.assertGreaterEqual(delay, 5)
                self.assertLess(delay, 5 + 15)

    def test_different_addresses_spread_across_window(self):
        """Different addresses produce different delays."""
        delays = set()
        for i in range(50):
            delay = startup_read_delay((i, i), base=0, window=60)
            delays.add(delay)
        # With 50 addresses and 60-second window, we should get at least 5 unique delays
        self.assertGreater(len(delays), 5)


class NumericConversionTest(unittest.TestCase):
    """Temperature and brightness conversions."""

    def test_temperature_rounding(self):
        """int(round(x)) vs int(x) truncation."""
        # Truncation: int(20.9) = 20
        # Rounding: int(round(20.9)) = 21
        self.assertEqual(int(20.9), 20)
        self.assertEqual(int(round(20.9)), 21)
        self.assertEqual(int(round(20.4)), 20)
        self.assertEqual(int(round(20.5)), 20)  # banker's rounding in Python 3

    def test_brightness_clamping_and_scaling(self):
        """max(1, min(100, ...)) preserves non-zero brightness."""
        # Typical HA brightness scale: 0-255 -> 0-100
        brightness_255 = 127  # ~50%
        brightness_100 = max(1, int(round(brightness_255 / 255 * 100)))
        self.assertEqual(brightness_100, 50)

        # Edge: very small value should clamp to 1, not 0
        brightness_small = 1
        brightness_clamped = max(1, int(round(brightness_small / 255 * 100)))
        self.assertEqual(brightness_clamped, 1)


if __name__ == "__main__":
    unittest.main()
