from .control import _GenericControl
from .device import Device
from ..helpers.enums import OperateCode


class Cover(Device):
    def __init__(self, buspro, device_address, channel_number, name=""):
        super().__init__(buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._channel = channel_number
        self._state = 0
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_status(run_from_init=True)

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
        await self._send_command(self._channel + 2, 1)

    async def close_cover_tilt(self):
        await self._send_command(self._channel + 2, 2)

    async def stop_cover_tilt(self):
        await self._send_command(self._channel + 2, 0)

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
        import asyncio

        async def read_current_state():
            if run_from_init:
                await asyncio.sleep(3)
            await self.read_status()

        asyncio.ensure_future(read_current_state(), loop=self._buspro.loop)

    @property
    def device_identifier(self):
        return f"{self._device_address}-{self._channel}"

    @property
    def is_opening(self):
        return self._state == 1

    @property
    def is_closing(self):
        return self._state == 2

