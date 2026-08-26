"""Shared protocol state for multi-channel Buspro relay modules."""

import asyncio

from .control import _ReadStatusOfChannels, _SingleChannelControl
from .device import Device
from ..helpers.enums import OperateCode


class RelayModule:
    """Coordinate one physical relay and fan status out to its channels."""

    def __init__(self, buspro, device_address, initial_refresh_delay=3):
        self._buspro = buspro
        self._device_address = tuple(device_address)
        self._channels = {}
        self._refresh_task = None
        self._closed = False
        self._buspro.register_telegram_received_device_cb(
            self._telegram_received_cb, self._device_address
        )
        self._schedule_refresh(initial_refresh_delay)

    def channel(self, channel_number, name=""):
        """Return the channel view for a physical relay output."""
        channel_number = int(channel_number)
        channel = self._channels.get(channel_number)
        if channel is None:
            channel = RelayChannel(self, channel_number, name)
            self._channels[channel_number] = channel
        return channel

    async def async_set_channel(self, channel_number, level):
        """Control one physical relay output."""
        control = _SingleChannelControl(self._buspro)
        control.subnet_id, control.device_id = self._device_address
        control.channel_number = int(channel_number)
        control.channel_level = int(level)
        control.running_time_minutes = 0
        control.running_time_seconds = 0
        await control.send()

    async def async_refresh(self):
        """Request all channel states with one module-level telegram."""
        control = _ReadStatusOfChannels(self._buspro)
        control.subnet_id, control.device_id = self._device_address
        await control.send()

    def remove_channel(self, channel_number):
        """Release a channel and stop listening when none remain."""
        self._channels.pop(int(channel_number), None)
        if not self._channels:
            self.close()

    def close(self):
        """Release the physical module callback and pending refresh."""
        if self._closed:
            return
        self._closed = True
        if self._refresh_task is not None and not self._refresh_task.done():
            self._refresh_task.cancel()
        self._buspro.unregister_telegram_received_device_cb(
            self._telegram_received_cb, self._device_address
        )

    def _schedule_refresh(self, delay=0):
        if self._closed or (
            self._refresh_task is not None and not self._refresh_task.done()
        ):
            return

        async def _refresh():
            try:
                if delay:
                    await asyncio.sleep(delay)
                await self.async_refresh()
            except asyncio.CancelledError:
                pass

        self._refresh_task = asyncio.ensure_future(_refresh())

    def _telegram_received_cb(self, telegram):
        payload = telegram.payload or []
        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            if len(payload) < 3:
                return
            channel = self._channels.get(int(payload[0]))
            if channel is not None:
                channel.update_level(payload[2])
            return

        if telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if not payload:
                return
            reported_count = int(payload[0])
            for number, channel in tuple(self._channels.items()):
                if number <= reported_count and number < len(payload):
                    channel.update_level(payload[number])
            return

        if telegram.operate_code == OperateCode.SceneControlResponse:
            self._schedule_refresh()


class RelayChannel(Device):
    """A single relay channel backed by a shared physical coordinator."""

    def __init__(self, module, channel_number, name=""):
        super().__init__(module._buspro, module._device_address, name)
        self._module = module
        self._channel = int(channel_number)
        self._brightness = 0
        self._closed = False

    def update_level(self, level):
        """Apply a level received by the physical module."""
        self._brightness = int(level)
        self._call_device_updated()

    async def set_on(self):
        self._brightness = 100
        await self._module.async_set_channel(self._channel, 100)

    async def set_off(self):
        self._brightness = 0
        await self._module.async_set_channel(self._channel, 0)

    def close(self):
        if self._closed:
            return
        self._closed = True
        self._module.remove_channel(self._channel)

    @property
    def supports_brightness(self):
        return False

    @property
    def channel_number(self):
        return self._channel

    @property
    def is_on(self):
        return self._brightness > 0

    @property
    def device_identifier(self):
        return f"{self._device_address}-{self._channel}"
