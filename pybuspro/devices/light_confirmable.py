"""Light/Dimmer device with optional command confirmation.

This module extends the Light device with confirmation capability for
brightness control. Users can enable per-device confirmation for lights
that need acknowledgment of state changes, especially useful for slow
dimmer modules that may miss commands.

Configuration:

    light = Light(
        hdl,
        (1, 50),
        1,
        name="Living Room Dimmer",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    # Fire-and-forget (traditional)
    await light.set_brightness(128)

    # Confirmation-aware
    if await light.set_brightness_with_confirmation(128):
        print("Brightness confirmed")
    else:
        print("Failed to confirm brightness change")
"""

import asyncio
from .confirmable import ConfirmableDevice
from .control import _ReadStatusOfChannels, _SingleChannelControl
from .device import Device, startup_read_delay
from ..helpers.enums import OperateCode
from ..helpers.generics import Generics


class Light(ConfirmableDevice, Device):
    """A dimmable light/brightness control with optional confirmation."""

    def __init__(
        self,
        buspro,
        device_address,
        channel_number,
        name="",
        delay_read_current_state_seconds=0,
        ack_retry_enabled=True,
        enable_confirmation=False,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    ):
        """
        Initialize a light with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            channel_number: Light channel number.
            name: Human-readable name.
            delay_read_current_state_seconds: Delay before initial status read.
            ack_retry_enabled: Enable legacy ACK retry (separate from confirmation).
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
        self._previous_brightness = None
        self._ack_retry_enabled = bool(ack_retry_enabled)
        self._ack_task = None
        self._awaiting_ack = False
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status_of_channels(run_from_init=True)

    def close(self):
        """Detach from the bus and cancel pending tasks."""
        if self._closed:
            return
        self._closed = True
        self._cleanup_confirmation_state()
        if self._ack_task is not None and not self._ack_task.done():
            self._ack_task.cancel()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams."""
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel = telegram.payload[0]
            brightness = telegram.payload[2]
            if channel == self._channel:
                self._awaiting_ack = False
                self._brightness = brightness
                self._set_previous_brightness(self._brightness)
                self._call_device_updated()

                # Mark confirmation for brightness change
                self.mark_confirmed(f"light_{self._channel}_brightness")

        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                self._brightness = telegram.payload[self._channel]
                self._set_previous_brightness(self._brightness)
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.SceneControlResponse:
            self._call_read_current_status_of_channels()

    # Traditional fire-and-forget methods
    async def set_on(self, running_time_seconds=0):
        """Turn light on (fire-and-forget)."""
        await self._set(100, running_time_seconds)

    async def set_off(self, running_time_seconds=0):
        """Turn light off (fire-and-forget)."""
        await self._set(0, running_time_seconds)

    async def set_brightness(self, intensity, running_time_seconds=0):
        """Set brightness (fire-and-forget)."""
        await self._set(intensity, running_time_seconds)

    # Confirmation-aware methods
    async def set_brightness_with_confirmation(
        self, intensity, running_time_seconds=0
    ) -> bool:
        """
        Set brightness with confirmation.

        Args:
            intensity: Brightness 0-100.
            running_time_seconds: Transition time.

        Returns:
            True if confirmation received or confirmation disabled.
            False if timeout/failed after retries.
        """

        async def _send():
            await self._send_single_channel_control(intensity, running_time_seconds)

        success = await self.send_and_confirm(
            command_id=f"light_{self._channel}_brightness",
            command_fn=_send,
        )

        if success:
            self._brightness = intensity
            self._set_previous_brightness(self._brightness)
            self._call_device_updated()
        return success

    async def set_on_with_confirmation(self, running_time_seconds=0) -> bool:
        """Turn light on with confirmation."""
        return await self.set_brightness_with_confirmation(100, running_time_seconds)

    async def set_off_with_confirmation(self, running_time_seconds=0) -> bool:
        """Turn light off with confirmation."""
        return await self.set_brightness_with_confirmation(0, running_time_seconds)

    async def read_status(self):
        """Request current brightness status."""
        scc = _ReadStatusOfChannels(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        await scc.send()

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}-{self._channel}"

    @property
    def supports_brightness(self):
        """Light supports brightness control."""
        return True

    @property
    def previous_brightness(self):
        """Get previous non-zero brightness."""
        return self._previous_brightness

    @property
    def current_brightness(self):
        """Get current brightness."""
        return self._brightness

    @property
    def is_on(self):
        """Return True if light is on."""
        return self._brightness > 0

    # Private methods
    async def _set(self, intensity, running_time_seconds):
        """Internal method for setting brightness (fire-and-forget)."""
        self._brightness = intensity
        self._set_previous_brightness(self._brightness)

        await self._send_single_channel_control(intensity, running_time_seconds)
        if self._ack_retry_enabled:
            self._start_ack_watch(intensity, running_time_seconds)

    async def _send_single_channel_control(self, intensity, running_time_seconds):
        """Send single channel control telegram."""
        generics = Generics()
        (minutes, seconds) = generics.calculate_minutes_seconds(running_time_seconds)

        scc = _SingleChannelControl(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        scc.channel_number = self._channel
        scc.channel_level = intensity
        scc.running_time_minutes = minutes
        scc.running_time_seconds = seconds
        await scc.send()

    def _start_ack_watch(self, intensity, running_time_seconds):
        """Start watching for ACK (legacy retry mechanism)."""
        if self._ack_task is not None and not self._ack_task.done():
            self._ack_task.cancel()
        self._awaiting_ack = True

        async def _watch():
            try:
                await asyncio.sleep(0.8)
                if not self._awaiting_ack:
                    return
                self._awaiting_ack = False
                if self._brightness != intensity:
                    return
                await self._send_single_channel_control(intensity, running_time_seconds)
            except asyncio.CancelledError:
                pass

        self._ack_task = self._spawn(_watch())

    def _set_previous_brightness(self, brightness):
        """Update previous brightness memory."""
        if self.supports_brightness and brightness > 0:
            self._previous_brightness = brightness

    def restore_previous_brightness(self, brightness):
        """Restore previous brightness value."""
        self._set_previous_brightness(brightness)

    def _call_read_current_status_of_channels(self, run_from_init=False):
        """Schedule a status read."""

        async def read_current_status_of_channels():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_status_of_channels())
