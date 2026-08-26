import asyncio

from .control import _GenericControl
from .device import Device, startup_read_delay
from ..helpers.enums import OperateCode


class Cover(Device):
    def __init__(self, buspro, device_address, channel_number, name=""):
        super().__init__(buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._channel = channel_number
        self._state = 0
        self._closed = False
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_status(run_from_init=True)

    def close(self):
        """Detach from the bus and cancel pending tasks (called on removal)."""
        if self._closed:
            return
        self._closed = True
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        if telegram.operate_code in (
            OperateCode.CurtainSwitchControlResponse,
            OperateCode.ReadStatusofCurtainSwitchResponse,
        ):
            if len(telegram.payload) >= 2 and telegram.payload[0] == self._channel:
                self._state = telegram.payload[1]
                self._call_device_updated()

    async def open_cover(self):
        await self._send_command(self._channel, 1)

    async def close_cover(self):
        await self._send_command(self._channel, 2)

    async def stop_cover(self):
        await self._send_command(self._channel, 0)

    async def open_cover_tilt(self):
        await self._send_command(self._tilt_channel, 1)

    async def close_cover_tilt(self):
        await self._send_command(self._tilt_channel, 2)

    async def stop_cover_tilt(self):
        await self._send_command(self._tilt_channel, 0)

    @property
    def _tilt_channel(self):
        # HDL tilt control uses the paired channel (channel + 2 in the curtain bank).
        # Guard against out-of-range values; if the offset overflows, fall back to
        # the main channel so the command at least reaches the right device.
        tilt = self._channel + 2
        return tilt if tilt <= 0xFF else self._channel

    async def read_status(self):
        gc = _GenericControl(self._buspro)
        gc.subnet_id, gc.device_id = self._device_address
        gc.operate_code = OperateCode.ReadStatusofCurtainSwitch
        gc.payload = [self._channel]
        await gc.send()

    async def _send_command(self, channel, command):
        gc = _GenericControl(self._buspro)
        gc.subnet_id, gc.device_id = self._device_address
        gc.operate_code = OperateCode.CurtainSwitchControl
        gc.payload = [channel, command]
        await gc.send()

    def _call_read_status(self, run_from_init=False):
        async def read_current_state():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=3))
            await self.read_status()

        self._spawn(read_current_state())

    @property
    def device_identifier(self):
        return f"{self._device_address}-{self._channel}"

    @property
    def is_opening(self):
        return self._state == 1

    @property
    def is_closing(self):
        return self._state == 2

