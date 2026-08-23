"""Cover/Curtain device with optional command confirmation.

This module extends the Cover device with confirmation capability for
controlling curtains and blinds. Confirmation is especially useful
for covers since movement takes time and network hiccups could cause
missed commands.

Configuration:

    cover = Cover(
        hdl,
        (1, 60),
        1,
        name="Living Room Curtains",
        enable_confirmation=True,
        confirmation_timeout=8.0,  # Longer timeout for movement
        confirmation_retries=3,
    )

    # Fire-and-forget (traditional)
    await cover.open_cover()

    # Confirmation-aware
    if await cover.open_cover_with_confirmation():
        print("Cover confirmed opening")
    else:
        print("Failed to confirm cover movement")
"""

import asyncio
from .confirmable import ConfirmableDevice
from .control import _GenericControl
from .device import Device, startup_read_delay
from ..helpers.enums import OperateCode


class Cover(ConfirmableDevice, Device):
    """A cover/curtain controller with optional confirmation."""

    def __init__(
        self,
        buspro,
        device_address,
        channel_number,
        name="",
        enable_confirmation=False,
        confirmation_timeout=8.0,  # Longer default for cover movement
        confirmation_retries=3,
    ):
        """
        Initialize a cover with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            channel_number: Cover channel number.
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
        self._state = 0  # 0=stop, 1=opening, 2=closing
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_status(run_from_init=True)

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
        if telegram.operate_code in (
            OperateCode.CurtainSwitchControlResponse,
            OperateCode.ReadStatusofCurtainSwitchResponse,
        ):
            if len(telegram.payload) < 2:
                return
            if telegram.payload[0] != self._channel:
                return

            state = telegram.payload[1]
            self._state = state
            self._call_device_updated()

            # Mark confirmation based on state change
            if state == 1:
                self.mark_confirmed(f"cover_{self._channel}_open")
            elif state == 2:
                self.mark_confirmed(f"cover_{self._channel}_close")
            elif state == 0:
                self.mark_confirmed(f"cover_{self._channel}_stop")

    # Traditional fire-and-forget methods
    async def open_cover(self):
        """Open the cover (fire-and-forget)."""
        await self._send_command(self._channel, 1)

    async def close_cover(self):
        """Close the cover (fire-and-forget)."""
        await self._send_command(self._channel, 2)

    async def stop_cover(self):
        """Stop the cover (fire-and-forget)."""
        await self._send_command(self._channel, 0)

    async def open_cover_tilt(self):
        """Open cover tilt (fire-and-forget)."""
        await self._send_command(self._channel + 2, 1)

    async def close_cover_tilt(self):
        """Close cover tilt (fire-and-forget)."""
        await self._send_command(self._channel + 2, 2)

    async def stop_cover_tilt(self):
        """Stop cover tilt (fire-and-forget)."""
        await self._send_command(self._channel + 2, 0)

    # Confirmation-aware methods
    async def open_cover_with_confirmation(self) -> bool:
        """
        Open the cover with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_command(self._channel, 1)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_open",
            command_fn=_send,
        )

        if success:
            self._state = 1
            self._call_device_updated()
        return success

    async def close_cover_with_confirmation(self) -> bool:
        """
        Close the cover with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_command(self._channel, 2)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_close",
            command_fn=_send,
        )

        if success:
            self._state = 2
            self._call_device_updated()
        return success

    async def stop_cover_with_confirmation(self) -> bool:
        """
        Stop the cover with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_command(self._channel, 0)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_stop",
            command_fn=_send,
        )

        if success:
            self._state = 0
            self._call_device_updated()
        return success

    async def open_cover_tilt_with_confirmation(self) -> bool:
        """Open tilt with confirmation."""

        async def _send():
            await self._send_command(self._channel + 2, 1)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_tilt_open",
            command_fn=_send,
        )

        if success:
            self._state = 1
            self._call_device_updated()
        return success

    async def close_cover_tilt_with_confirmation(self) -> bool:
        """Close tilt with confirmation."""

        async def _send():
            await self._send_command(self._channel + 2, 2)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_tilt_close",
            command_fn=_send,
        )

        if success:
            self._state = 2
            self._call_device_updated()
        return success

    async def stop_cover_tilt_with_confirmation(self) -> bool:
        """Stop tilt with confirmation."""

        async def _send():
            await self._send_command(self._channel + 2, 0)

        success = await self.send_and_confirm(
            command_id=f"cover_{self._channel}_tilt_stop",
            command_fn=_send,
        )

        if success:
            self._state = 0
            self._call_device_updated()
        return success

    async def read_status(self):
        """Request current cover status."""
        gc = _GenericControl(self._buspro)
        gc.subnet_id, gc.device_id = self._device_address
        gc.operate_code = OperateCode.ReadStatusofCurtainSwitch
        gc.payload = [self._channel]
        await gc.send()

    def _call_read_status(self, run_from_init=False):
        """Schedule a status read."""

        async def read_current_state():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=3))
            await self.read_status()

        self._spawn(read_current_state())

    async def _send_command(self, channel, command):
        """Send a cover control command."""
        gc = _GenericControl(self._buspro)
        gc.subnet_id, gc.device_id = self._device_address
        gc.operate_code = OperateCode.CurtainSwitchControl
        gc.payload = [channel, command]
        await gc.send()

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}-{self._channel}"

    @property
    def is_opening(self):
        """Return True if cover is opening."""
        return self._state == 1

    @property
    def is_closing(self):
        """Return True if cover is closing."""
        return self._state == 2

    @property
    def is_stopped(self):
        """Return True if cover is stopped."""
        return self._state == 0

    @property
    def state(self):
        """Return current state (0=stop, 1=open, 2=close)."""
        return self._state
