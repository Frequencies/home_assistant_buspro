"""Protocol diagnostics for HDL Buspro dimmers."""

import asyncio
import time

from .control import _GenericControl
from .device import Device
from ..helpers.enums import OperateCode


class DimmerDiagnostics(Device):
    """Shared status and configuration reader for one dimmer module."""

    def __init__(self, buspro, device_address, channel_count):
        super().__init__(buspro, device_address)
        self._channel_count = channel_count
        self._minimum_brightness = None
        self._maximum_brightness = [None] * channel_count
        self._load_types = [None] * channel_count
        self._online = None
        self._last_online_response = 0.0
        self._closed = False
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._refresh_task = asyncio.ensure_future(self._refresh_loop())

    def _telegram_received_cb(self, telegram):
        payload = list(telegram.payload or ())
        if tuple(telegram.source_address or ()) == self._device_address:
            self._online = True
            self._last_online_response = time.monotonic()
        if telegram.operate_code == OperateCode.ReadLimitOfEveryChannelResponse:
            if len(payload) < self._channel_count + 1:
                return
            self._minimum_brightness = payload[0]
            self._maximum_brightness = payload[1 : self._channel_count + 1]
            self._call_device_updated()
        elif telegram.operate_code == OperateCode.ReadChannelLoadTypeResponse:
            if len(payload) < self._channel_count:
                return
            self._load_types = payload[: self._channel_count]
            self._call_device_updated()
        elif telegram.operate_code == OperateCode.IsDeviceOnlineResponse:
            self._call_device_updated()

    async def _send_query(self, operate_code, payload=None):
        control = _GenericControl(self._buspro)
        control.subnet_id, control.device_id = self._device_address
        control.operate_code = operate_code
        control.payload = payload or []
        await control.send()

    async def refresh(self):
        """Refresh supported diagnostics with bounded bus traffic."""
        if self._last_online_response and time.monotonic() - self._last_online_response > 150:
            self._online = False
            self._call_device_updated()
        await self._send_query(OperateCode.IsDeviceOnline)
        await asyncio.sleep(1)
        await self._send_query(OperateCode.ReadLimitOfEveryChannel)
        await asyncio.sleep(1)
        await self._send_query(OperateCode.ReadChannelLoadType)

    async def _refresh_loop(self):
        try:
            await asyncio.sleep(10)
            while not self._closed:
                await self.refresh()
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    @property
    def online(self):
        return self._online

    @property
    def minimum_brightness(self):
        return self._minimum_brightness

    def maximum_brightness(self, channel):
        return self._maximum_brightness[channel - 1]

    def load_type(self, channel):
        return self._load_types[channel - 1]

    def close(self):
        """Stop polling and detach from the bus."""
        self._closed = True
        if not self._refresh_task.done():
            self._refresh_task.cancel()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass
