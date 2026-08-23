"""Relay module with optional command confirmation.

This module extends the basic RelayChannel with confirmation capability.
Users can enable per-device confirmation for critical relays that need
acknowledgment of state changes.

Configuration:

    relay = RelayModule(hdl, (1, 50))
    channel = relay.channel(
        1,
        name="Critical Load",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    # Fire-and-forget (traditional)
    await channel.set_on()

    # Confirmation-aware
    if await channel.set_on_with_confirmation():
        print("Relay confirmed ON")
    else:
        print("Relay failed to confirm")
"""

import asyncio
from .confirmable import ConfirmableDevice
from .control import _ReadStatusOfChannels, _SingleChannelControl
from .device import Device
from ..helpers.enums import OperateCode


class RelayChannel(ConfirmableDevice, Device):
    """A single relay channel with optional confirmation.

    This class combines ConfirmableDevice mixin with the basic Device
    to provide both traditional fire-and-forget and confirmation-based
    control.
    """

    def __init__(
        self,
        module,
        channel_number,
        name="",
        enable_confirmation=False,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    ):
        """
        Initialize a relay channel with confirmation support.

        Args:
            module: Parent RelayModule.
            channel_number: Relay channel number (1-based).
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
        Device.__init__(self, module._buspro, module._device_address, name)

        self._module = module
        self._channel = int(channel_number)
        self._brightness = 0
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)

    def update_level(self, level):
        """Apply a level received by the physical module."""
        self._brightness = int(level)
        self._call_device_updated()

    # Traditional fire-and-forget methods
    async def set_on(self):
        """Turn relay on (fire-and-forget)."""
        self._brightness = 100
        await self._module.async_set_channel(self._channel, 100)

    async def set_off(self):
        """Turn relay off (fire-and-forget)."""
        self._brightness = 0
        await self._module.async_set_channel(self._channel, 0)

    # Confirmation-aware methods
    async def set_on_with_confirmation(self) -> bool:
        """
        Turn relay on with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._module.async_set_channel(self._channel, 100)

        success = await self.send_and_confirm(
            command_id=f"relay_{self._channel}_on",
            command_fn=_send,
        )

        if success:
            self._brightness = 100
            self._call_device_updated()
        return success

    async def set_off_with_confirmation(self) -> bool:
        """
        Turn relay off with confirmation.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._module.async_set_channel(self._channel, 0)

        success = await self.send_and_confirm(
            command_id=f"relay_{self._channel}_off",
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
        self._module.remove_channel(self._channel)

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams and mark confirmations."""
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            if len(telegram.payload) < 3:
                return
            channel = int(telegram.payload[0])
            if channel != self._channel:
                return

            brightness = int(telegram.payload[2])
            self.update_level(brightness)

            # Mark confirmation for both on and off (check actual state)
            if brightness > 0:
                self.mark_confirmed(f"relay_{self._channel}_on")
            else:
                self.mark_confirmed(f"relay_{self._channel}_off")

        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if len(telegram.payload) > self._channel:
                self.update_level(telegram.payload[self._channel])

        elif telegram.operate_code == OperateCode.SceneControlResponse:
            # Scene changes don't wait for confirmation
            pass

    @property
    def supports_brightness(self):
        """Relays don't support brightness dimming."""
        return False

    @property
    def channel_number(self):
        """Get channel number."""
        return self._channel

    @property
    def is_on(self):
        """Return True if relay is on."""
        return self._brightness > 0

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}-{self._channel}"
