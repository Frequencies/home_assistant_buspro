"""Switch device with optional command confirmation.

This module extends the basic Switch with confirmation capability.
Similar to Relay but for different device types.

Configuration:

    switch = Switch(
        hdl,
        (1, 70),
        1,
        name="Safety Switch",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    if await switch.set_on_with_confirmation():
        print("Switch confirmed ON")
"""

import asyncio
from .confirmable import ConfirmableDevice
from .control import _SingleChannelControl
from .device import Device
from ..helpers.enums import OperateCode


class Switch(ConfirmableDevice, Device):
    """A switch/power outlet with optional confirmation."""

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
        Initialize a switch with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            channel_number: Switch channel number.
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
        self._brightness = 0
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams."""
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            if len(telegram.payload) < 3:
                return
            channel = int(telegram.payload[0])
            if channel != self._channel:
                return

            brightness = int(telegram.payload[2])
            self._brightness = brightness

            # Mark confirmation for both on and off
            if brightness > 0:
                self.mark_confirmed(f"switch_{self._channel}_on")
            else:
                self.mark_confirmed(f"switch_{self._channel}_off")

            self._call_device_updated()

    # Traditional fire-and-forget methods
    async def set_on(self):
        """Turn switch on (fire-and-forget)."""
        self._brightness = 100
        await self._send_command(100)

    async def set_off(self):
        """Turn switch off (fire-and-forget)."""
        self._brightness = 0
        await self._send_command(0)

    # Confirmation-aware methods
    async def set_on_with_confirmation(self) -> bool:
        """
        Turn switch on with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_command(100)

        success = await self.send_and_confirm(
            command_id=f"switch_{self._channel}_on",
            command_fn=_send,
        )

        if success:
            self._brightness = 100
            self._call_device_updated()
        return success

    async def set_off_with_confirmation(self) -> bool:
        """
        Turn switch off with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_command(0)

        success = await self.send_and_confirm(
            command_id=f"switch_{self._channel}_off",
            command_fn=_send,
        )

        if success:
            self._brightness = 0
            self._call_device_updated()
        return success

    def close(self):
        """Clean up and close the device."""
        if self._closed:
            return
        self._closed = True
        self._cleanup_confirmation_state()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    async def _send_command(self, level):
        """Send switch control command."""
        scc = _SingleChannelControl(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        scc.channel_number = self._channel
        scc.channel_level = level
        scc.running_time_minutes = 0
        scc.running_time_seconds = 0
        await scc.send()

    @property
    def channel_number(self):
        """Get channel number."""
        return self._channel

    @property
    def is_on(self):
        """Return True if switch is on."""
        return self._brightness > 0

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}-{self._channel}"
