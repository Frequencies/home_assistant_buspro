import asyncio

from .control import _ReadStatusOfChannels, _SingleChannelControl
from .device import Device, startup_read_delay
from ..helpers.enums import *
from ..helpers.generics import Generics


class Light(Device):
    def __init__(
        self,
        buspro,
        device_address,
        channel_number,
        name="",
        delay_read_current_state_seconds=0,
        ack_retry_enabled=True,
    ):
        super().__init__(buspro, device_address, name)
        # device_address = (subnet_id, device_id, channel_number)

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
        """Detach from the bus and cancel pending tasks (called on removal)."""
        if self._closed:
            return
        self._closed = True
        if self._ack_task is not None and not self._ack_task.done():
            self._ack_task.cancel()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):

        # if telegram.target_address[1] == 72:
        #    print("==== {}".format(str(telegram)))

        if telegram.operate_code == OperateCode.SingleChannelControlResponse:
            channel = telegram.payload[0]
            # success = telegram.payload[1]
            brightness = telegram.payload[2]
            if channel == self._channel:
                self._awaiting_ack = False
                self._brightness = brightness
                self._set_previous_brightness(self._brightness)
                self._call_device_updated()
        elif telegram.operate_code == OperateCode.ReadStatusOfChannelsResponse:
            if self._channel <= telegram.payload[0]:
                self._brightness = telegram.payload[self._channel]
                self._set_previous_brightness(self._brightness)
                self._call_device_updated()
        elif telegram.operate_code == OperateCode.SceneControlResponse:
            self._call_read_current_status_of_channels()

    async def set_on(self, running_time_seconds=0):
        intensity = 100
        await self._set(intensity, running_time_seconds)

    async def set_off(self, running_time_seconds=0):
        intensity = 0
        await self._set(intensity, running_time_seconds)

    async def set_brightness(self, intensity, running_time_seconds=0):
        await self._set(intensity, running_time_seconds)

    async def read_status(self):
        scc = _ReadStatusOfChannels(self._buspro)
        scc.subnet_id, scc.device_id = self._device_address
        await scc.send()

    @property
    def device_identifier(self):
        return f"{self._device_address}-{self._channel}"

    @property
    def supports_brightness(self):
        return True

    @property
    def previous_brightness(self):
        return self._previous_brightness

    @property
    def current_brightness(self):
        return self._brightness

    @property
    def is_on(self):
        if self._brightness == 0:
            return False
        else:
            return True

    async def _set(self, intensity, running_time_seconds):
        self._brightness = intensity
        self._set_previous_brightness(self._brightness)

        await self._send_single_channel_control(intensity, running_time_seconds)
        if self._ack_retry_enabled:
            self._start_ack_watch(intensity, running_time_seconds)

    async def _send_single_channel_control(self, intensity, running_time_seconds):
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
        if self.supports_brightness and brightness > 0:
            self._previous_brightness = brightness

    def restore_previous_brightness(self, brightness):
        self._set_previous_brightness(brightness)

    def _call_read_current_status_of_channels(self, run_from_init=False):
        async def read_current_status_of_channels():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_status_of_channels())
