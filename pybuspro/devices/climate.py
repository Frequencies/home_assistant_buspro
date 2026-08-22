import asyncio
import struct

from .control import (
    _ReadFloorHeatingStatus,
    _ControlFloorHeatingStatus,
    _ReadFloorHeatingModuleStatus,
    _ControlFloorHeatingModuleStatus,
    _ReadFloorHeatingTemperatureNew,
    _ReadFloorHeatingTemperatureLegacy,
    _ReadPanelAC,
    _ControlPanelAC,
)
from .device import Device, startup_read_delay
from ..helpers.enums import (
    OperateCode,
    SuccessOrFailure,
    TemperatureType,
    TemperatureMode,
    WorkType,
    FloorHeatingDeviceType,
)
from ..helpers.generics import Generics

# Valid WorkType enum values, precomputed for O(1) membership checks on the
# per-telegram hot path (was rebuilt as a list on every frame).
_WORK_TYPE_VALUES = frozenset(w.value for w in WorkType)


class ControlFloorHeatingStatus:
    def __init__(self):
        self.temperature_type = None
        self.status = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None
        self.work_type = None


class ControlPanelAC:
    def __init__(self):
        self.status = None
        self.mode = None
        self.normal_temperature = None


class Climate(Device):
    """Panel AC climate using E3DA/E3D8 opcodes."""

    def __init__(self, buspro, device_address, name=""):
        super().__init__(buspro, device_address, name)
        self._buspro = buspro
        self._device_address = device_address

        self._status = None
        self._mode = None
        self._current_temperature = None
        self._normal_temperature = None

        self._closed = False
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_panel_status(run_from_init=True)
        self._call_read_current_panel_temp(run_from_init=True)

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
        if telegram.operate_code in (OperateCode.ReadPanelACResponse, OperateCode.ControlPanelACResponse):
            if len(telegram.payload) < 2:
                return
            command = telegram.payload[0]
            value = telegram.payload[1]

            if command == 3:
                self._status = value
                self._mode = value
                self._call_device_updated()
            elif command == 4:
                self._current_temperature = value
                self._normal_temperature = value
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.BroadcastTemperatureResponse:
            if len(telegram.payload) >= 2:
                self._current_temperature = telegram.payload[1]
                self._call_device_updated()

    async def read_status(self):
        req = _ReadPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 3
        await req.send()

    async def read_temperature(self):
        req = _ReadPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 4
        await req.send()

    async def control_ac_status(self, panel_status: ControlPanelAC):
        req = _ControlPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 3
        req.mode = panel_status.status if panel_status.status is not None else panel_status.mode
        await req.send()

    async def control_ac_temperature(self, panel_status: ControlPanelAC):
        req = _ControlPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 4
        req.mode = panel_status.normal_temperature
        await req.send()

    def _call_read_current_panel_status(self, run_from_init=False):
        async def read_current_panel_status():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_panel_status())

    def _call_read_current_panel_temp(self, run_from_init=False):
        async def read_current_panel_temp():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_temperature()

        self._spawn(read_current_panel_temp())

    @property
    def is_on(self):
        return self._status == 1

    @property
    def mode(self):
        return self._mode

    @property
    def temperature(self):
        return self._current_temperature

    @property
    def target_temperature(self):
        return self._normal_temperature

    @property
    def device_identifier(self):
        return f"{self._device_address}"


class FloorHeating(Device):
    def __init__(self, buspro, device_address, name="", channel_number=None, device_type=FloorHeatingDeviceType.DLP):
        super().__init__(buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._channel_number = channel_number
        self._device_type = device_type

        self._temperature_type = None
        self._status = None
        self._mode = None
        self._current_temperature = None
        self._normal_temperature = None
        self._day_temperature = None
        self._night_temperature = None
        self._away_temperature = None
        self._work_type = WorkType.Heating
        self._valve = None
        self._watering_time = None

        self._closed = False
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status(run_from_init=True)

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
        if telegram.operate_code == OperateCode.ReadFloorHeatingStatusResponse:
            if len(telegram.payload) < 8:
                return
            self._temperature_type = telegram.payload[0]
            self._current_temperature = telegram.payload[1]
            self._status = telegram.payload[2]
            self._mode = telegram.payload[3]
            self._normal_temperature = telegram.payload[4]
            self._day_temperature = telegram.payload[5]
            self._night_temperature = telegram.payload[6]
            self._away_temperature = telegram.payload[7]
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.ControlFloorHeatingStatusResponse:
            if len(telegram.payload) < 8:
                return
            success_or_fail = telegram.payload[0]
            self._temperature_type = telegram.payload[1]
            self._status = telegram.payload[2]
            self._mode = telegram.payload[3]
            self._normal_temperature = telegram.payload[4]
            self._day_temperature = telegram.payload[5]
            self._night_temperature = telegram.payload[6]
            self._away_temperature = telegram.payload[7]
            if success_or_fail == SuccessOrFailure.Success.value[0]:
                self._call_device_updated()

        elif telegram.operate_code == OperateCode.ReadFloorHeatingModuleStatusResponse:
            if len(telegram.payload) < 13:
                return
            if self._channel_number is not None and telegram.payload[0] != self._channel_number:
                return

            work = telegram.payload[1]
            self._status = 1 if (work & 0x0F) else 0
            work_raw = (work >> 4) & 0x0F
            self._work_type = WorkType(work_raw) if work_raw in _WORK_TYPE_VALUES else WorkType.Heating
            self._temperature_type = telegram.payload[2]
            self._mode = telegram.payload[3]
            self._normal_temperature = telegram.payload[4]
            self._day_temperature = telegram.payload[5]
            self._night_temperature = telegram.payload[6]
            self._away_temperature = telegram.payload[7]
            self._valve = telegram.payload[9]
            self._watering_time = telegram.payload[12]
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.ControlFloorHeatingModuleStatusResponse:
            if len(telegram.payload) < 10:
                return
            if self._channel_number is not None and telegram.payload[0] != self._channel_number:
                return

            work = telegram.payload[1]
            self._status = 1 if (work & 0x0F) else 0
            work_raw = (work >> 4) & 0x0F
            self._work_type = WorkType(work_raw) if work_raw in _WORK_TYPE_VALUES else WorkType.Heating
            self._temperature_type = telegram.payload[2]
            self._mode = telegram.payload[3]
            self._normal_temperature = telegram.payload[4]
            self._day_temperature = telegram.payload[5]
            self._night_temperature = telegram.payload[6]
            self._away_temperature = telegram.payload[7]
            self._valve = telegram.payload[8]
            self._watering_time = telegram.payload[9]
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.ReadFloorHeatingTemperatureNewResponse:
            if len(telegram.payload) < 5:
                return
            if self._channel_number is not None and telegram.payload[0] != self._channel_number:
                return
            try:
                self._current_temperature = struct.unpack("<f", bytes(telegram.payload[1:5]))[0]
                self._call_device_updated()
            except Exception:
                pass

        elif telegram.operate_code == OperateCode.ReadFloorHeatingTemperatureLegacyResponse:
            if len(telegram.payload) < 2:
                return
            if self._channel_number is not None and telegram.payload[0] != self._channel_number:
                return
            raw_temp = telegram.payload[1]
            sign = -1 if (raw_temp >> 7) else 1
            self._current_temperature = sign * (raw_temp & 0x7F)
            self._call_device_updated()

        elif telegram.operate_code == OperateCode.BroadcastTemperatureResponse:
            if len(telegram.payload) >= 2:
                self._current_temperature = telegram.payload[1]
                self._call_device_updated()

    async def read_status(self):
        if self._device_type == FloorHeatingDeviceType.Module:
            req = _ReadFloorHeatingModuleStatus(self._buspro)
            req.subnet_id, req.device_id = self._device_address
            req.channel_number = self._channel_number
            await req.send()

            req_new_temp = _ReadFloorHeatingTemperatureNew(self._buspro)
            req_new_temp.subnet_id, req_new_temp.device_id = self._device_address
            req_new_temp.channel_number = self._channel_number
            await req_new_temp.send()

            req_legacy_temp = _ReadFloorHeatingTemperatureLegacy(self._buspro)
            req_legacy_temp.subnet_id, req_legacy_temp.device_id = self._device_address
            req_legacy_temp.channel_number = self._channel_number
            await req_legacy_temp.send()
        else:
            req = _ReadFloorHeatingStatus(self._buspro)
            req.subnet_id, req.device_id = self._device_address
            await req.send()

    async def control_heating_status(self, floor_heating_status: ControlFloorHeatingStatus):
        if self._device_type == FloorHeatingDeviceType.Module:
            self.register_telegram_received_cb(self._telegram_received_control_module_cb, floor_heating_status)
            req = _ReadFloorHeatingModuleStatus(self._buspro)
            req.subnet_id, req.device_id = self._device_address
            req.channel_number = self._channel_number
            await req.send()
        else:
            self.register_telegram_received_cb(self._telegram_received_control_dlp_cb, floor_heating_status)
            req = _ReadFloorHeatingStatus(self._buspro)
            req.subnet_id, req.device_id = self._device_address
            await req.send()

    def _telegram_received_control_dlp_cb(self, telegram, floor_heating_status):
        if telegram.operate_code != OperateCode.ReadFloorHeatingStatusResponse:
            return

        self.unregister_telegram_received_cb(self._telegram_received_control_dlp_cb, floor_heating_status)

        if len(telegram.payload) < 8:
            return

        temperature_type = telegram.payload[0]
        status = telegram.payload[2]
        mode = telegram.payload[3]
        normal_temperature = telegram.payload[4]
        day_temperature = telegram.payload[5]
        night_temperature = telegram.payload[6]
        away_temperature = telegram.payload[7]

        if floor_heating_status.temperature_type is not None:
            temperature_type = floor_heating_status.temperature_type
        if floor_heating_status.status is not None:
            status = floor_heating_status.status
        if floor_heating_status.mode is not None:
            mode = floor_heating_status.mode
        if floor_heating_status.normal_temperature is not None:
            normal_temperature = floor_heating_status.normal_temperature
        if floor_heating_status.day_temperature is not None:
            day_temperature = floor_heating_status.day_temperature
        if floor_heating_status.night_temperature is not None:
            night_temperature = floor_heating_status.night_temperature
        if floor_heating_status.away_temperature is not None:
            away_temperature = floor_heating_status.away_temperature

        ctrl = _ControlFloorHeatingStatus(self._buspro)
        ctrl.subnet_id, ctrl.device_id = self._device_address
        ctrl.temperature_type = temperature_type
        ctrl.status = status
        ctrl.mode = mode
        ctrl.normal_temperature = normal_temperature
        ctrl.day_temperature = day_temperature
        ctrl.night_temperature = night_temperature
        ctrl.away_temperature = away_temperature

        async def send_control():
            await ctrl.send()

        self._spawn(send_control())

    def _telegram_received_control_module_cb(self, telegram, floor_heating_status):
        if telegram.operate_code != OperateCode.ReadFloorHeatingModuleStatusResponse:
            return
        if len(telegram.payload) < 13:
            return
        if self._channel_number is not None and telegram.payload[0] != self._channel_number:
            return

        self.unregister_telegram_received_cb(self._telegram_received_control_module_cb, floor_heating_status)

        work = telegram.payload[1]
        temperature_type = telegram.payload[2]
        mode = telegram.payload[3]
        normal_temperature = telegram.payload[4]
        day_temperature = telegram.payload[5]
        night_temperature = telegram.payload[6]
        away_temperature = telegram.payload[7]
        valve = telegram.payload[9]
        watering_time = telegram.payload[12]

        status = 1 if (work & 0x0F) else 0
        work_raw = (work >> 4) & 0x0F
        current_work_type = WorkType(work_raw) if work_raw in _WORK_TYPE_VALUES else WorkType.Heating

        if floor_heating_status.temperature_type is not None:
            temperature_type = floor_heating_status.temperature_type
        if floor_heating_status.status is not None:
            status = floor_heating_status.status
        if floor_heating_status.mode is not None:
            mode = floor_heating_status.mode
        if floor_heating_status.normal_temperature is not None:
            normal_temperature = floor_heating_status.normal_temperature
        if floor_heating_status.day_temperature is not None:
            day_temperature = floor_heating_status.day_temperature
        if floor_heating_status.night_temperature is not None:
            night_temperature = floor_heating_status.night_temperature
        if floor_heating_status.away_temperature is not None:
            away_temperature = floor_heating_status.away_temperature

        target_work_type = floor_heating_status.work_type if floor_heating_status.work_type is not None else current_work_type

        ctrl = _ControlFloorHeatingModuleStatus(self._buspro)
        ctrl.subnet_id, ctrl.device_id = self._device_address
        ctrl.channel_number = self._channel_number
        ctrl.work = (target_work_type.value << 4) | (1 if status else 0)
        ctrl.temperature_type = temperature_type
        ctrl.mode = mode
        ctrl.normal_temperature = normal_temperature
        ctrl.day_temperature = day_temperature
        ctrl.night_temperature = night_temperature
        ctrl.away_temperature = away_temperature
        ctrl.valve = valve
        ctrl.watering_time = watering_time

        async def send_control():
            await ctrl.send()

        self._spawn(send_control())

    def _call_read_current_status(self, run_from_init=False):
        async def read_current_status():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_status())

    @property
    def unit_of_measurement(self):
        generics = Generics()
        return generics.get_enum_value(TemperatureType, self._temperature_type)

    @property
    def is_on(self):
        return self._status == 1

    @property
    def mode(self):
        return self._mode

    @property
    def work_type(self):
        return self._work_type

    @property
    def temperature(self):
        return self._current_temperature

    @property
    def device_identifier(self):
        channel = f".{self._channel_number}" if self._channel_number is not None else ""
        return f"{self._device_address}{channel}"

    @property
    def target_temperature(self):
        if self._mode == TemperatureMode.Normal.value:
            return self._normal_temperature
        if self._mode == TemperatureMode.Day.value:
            return self._day_temperature
        if self._mode == TemperatureMode.Away.value:
            return self._away_temperature
        if self._mode == TemperatureMode.Night.value:
            return self._night_temperature
        return self._normal_temperature
