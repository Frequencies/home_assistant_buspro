"""Fan device with optional command confirmation.

This module extends the Fan device with confirmation capability for
fan speed control, useful for ventilation systems that need reliable
state changes.

Configuration:

    fan = Fan(
        hdl,
        (1, 80),
        1,
        name="Bathroom Ventilation",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    if await fan.set_speed_with_confirmation(50):
        print("Fan speed confirmed")
"""

import asyncio
from .confirmable import ConfirmableDevice
from .control import _SingleChannelControl
from .device import Device, startup_read_delay
from ..helpers.enums import OperateCode


class Fan(ConfirmableDevice, Device):
    """A fan with variable speed and optional confirmation."""

    def __init__(
        self,
        buspro,
        device_address,
        channel_number,
        name="",
        enable_confirmation=False,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    ):
        """
        Initialize a fan with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            channel_number: Fan channel number.
            name: Human-readable name.
            enable_confirmation: Enable confirmation waiting.
            confirmation_timeout: Seconds to wait for response.
            confirmation_retries: Retry attempts on timeout.
        """
        # Initialize ConfirmableDevice first
        ConfirmableDevice.__init__(
            self,
            enable_confirmation=enable_confirmation,
            confirmation_timeout=confirmation_timeout,
            confirmation_retries=confirmation_retries,
        )

        # Initialize Device
        Device.__init__(self, buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._channel = channel_number
        self._speed = 0
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status(run_from_init=True)

    def close(self):
        """Detach from the bus and cancel pending tasks."""
        if self._closed:
            return
        self._closed = True
        self._cleanup_confirmation_state()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams."""
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            if len(telegram.payload) < 3:
                return
            channel = int(telegram.payload[0])
            if channel != self._channel:
                return

            speed = int(telegram.payload[2])
            self._speed = speed
            self._call_device_updated()

            # Mark confirmation for speed change
            self.mark_confirmed(f"fan_{self._channel}_speed")

        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if len(telegram.payload) > self._channel:
                self._speed = int(telegram.payload[self._channel])
                self._call_device_updated()

    # Traditional fire-and-forget methods
    async def set_speed(self, speed: int):
        """
        Set fan speed (fire-and-forget).

        Args:
            speed: Speed 0-100 (0=off, 100=full speed).
        """
        speed = max(0, min(100, int(speed)))
        self._speed = speed
        await self._send_command(speed)

    async def turn_on(self, speed: int = 100):
        """Turn fan on at specified speed (fire-and-forget)."""
        await self.set_speed(speed)

    async def turn_off(self):
        """Turn fan off (fire-and-forget)."""
        await self.set_speed(0)

    # Confirmation-aware methods
    async def set_speed_with_confirmation(self, speed: int) -> bool:
        """
        Set fan speed with confirmation.

        Args:
            speed: Speed 0-100 (0=off, 100=full speed).

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """
        speed = max(0, min(100, int(speed)))

        async def _send():
            await self._send_command(speed)

        success = await self.send_and_confirm(
            command_id=f"fan_{self._channel}_speed",
            command_fn=_send,
        )

        if success:
            self._speed = speed
            self._call_device_updated()
        return success

    async def turn_on_with_confirmation(self, speed: int = 100) -> bool:
        """Turn fan on with confirmation."""
        return await self.set_speed_with_confirmation(speed)

    async def turn_off_with_confirmation(self) -> bool:
        """Turn fan off with confirmation."""
        return await self.set_speed_with_confirmation(0)

    async def read_status(self):
        """Request current fan speed status."""
        from .control import _ReadStatusOfChannels

        rsc = _ReadStatusOfChannels(self._buspro)
        rsc.subnet_id, rsc.device_id = self._device_address
        await rsc.send()

    def _call_read_current_status(self, run_from_init=False):
        """Schedule a status read."""

        async def read_current_status():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_status())

    async def _send_command(self, speed: int):
        """Send fan control command."""
        scc = _SingleChannelControl(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        scc.channel_number = self._channel
        scc.channel_level = speed
        scc.running_time_minutes = 0
        scc.running_time_seconds = 0
        await scc.send()

    @property
    def channel_number(self):
        """Get channel number."""
        return self._channel

    @property
    def speed(self):
        """Get current fan speed (0-100)."""
        return self._speed

    @property
    def is_on(self):
        """Return True if fan is running."""
        return self._speed > 0

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}-{self._channel}"
