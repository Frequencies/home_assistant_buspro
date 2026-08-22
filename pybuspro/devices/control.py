import logging
import time

from ..core.telegram import Telegram
from ..helpers.enums import OperateCode

_LOGGER = logging.getLogger(__name__)
_last_queries = {}
_LAST_QUERIES_MAX = 4096
_LAST_QUERIES_PRUNE_INTERVAL = 60.0
_last_queries_prune_at = 0.0


class _Control:
    def __init__(self, buspro):
        self._buspro = buspro
        self.subnet_id = None
        self.device_id = None

    @staticmethod
    def build_telegram_from_control(control):

        if control is None:
            return None

        if type(control) == _SingleChannelControl:
            operate_code = OperateCode.SingleChannelControl
            payload = [control.channel_number, control.channel_level, control.running_time_minutes,
                       control.running_time_seconds]

        elif type(control) == _SceneControl:
            operate_code = OperateCode.SceneControl
            payload = [control.area_number, control.scene_number]

        elif type(control) == _ReadStatusOfChannels:
            operate_code = OperateCode.ReadStatusOfChannels
            payload = []

        elif type(control) == _GenericControl:
            operate_code = control.operate_code
            payload = control.payload

        elif type(control) == _UniversalSwitch:
            operate_code = OperateCode.UniversalSwitchControl
            payload = [control.switch_number, control.switch_status.value]

        elif type(control) == _ReadStatusOfUniversalSwitch:
            operate_code = OperateCode.ReadStatusOfUniversalSwitch
            payload = [control.switch_number]

        elif type(control) == _ReadSensorStatus:
            operate_code = OperateCode.ReadSensorStatus
            payload = []

        elif type(control) == _ReadSensorsInOneStatus:
            operate_code = OperateCode.ReadSensorsInOneStatus
            payload = []

        elif type(control) == _ReadFloorHeatingStatus:
            operate_code = OperateCode.ReadFloorHeatingStatus
            payload = []

        elif type(control) == _ReadFloorHeatingModuleStatus:
            operate_code = OperateCode.ReadFloorHeatingModuleStatus
            payload = [control.channel_number]

        elif type(control) == _ReadFloorHeatingTemperatureNew:
            operate_code = OperateCode.ReadFloorHeatingTemperatureNew
            payload = [control.channel_number]

        elif type(control) == _ReadFloorHeatingTemperatureLegacy:
            operate_code = OperateCode.ReadFloorHeatingTemperatureLegacy
            payload = [control.channel_number]

        elif type(control) == _ReadDryContactStatus:
            operate_code = OperateCode.ReadDryContactStatus
            payload = [1, control.switch_number]

        elif type(control) == _ControlFloorHeatingStatus:
            operate_code = OperateCode.ControlFloorHeatingStatus
            payload = [control.temperature_type, control.status, control.mode, control.normal_temperature,
                       control.day_temperature, control.night_temperature, control.away_temperature]
        elif type(control) == _ControlFloorHeatingModuleStatus:
            operate_code = OperateCode.ControlFloorHeatingModuleStatus
            payload = [control.channel_number, control.work, control.temperature_type, control.mode,
                       control.normal_temperature, control.day_temperature, control.night_temperature,
                       control.away_temperature, control.valve, control.watering_time]
        elif type(control) == _ReadPanelAC:
            operate_code = OperateCode.ReadPanelAC
            payload = [control.command]
        elif type(control) == _ControlPanelAC:
            operate_code = OperateCode.ControlPanelAC
            payload = [control.command, control.mode]

        else:
            return None

        telegram = Telegram()
        telegram.target_address = (control.subnet_id, control.device_id)
        telegram.operate_code = operate_code
        telegram.payload = payload
        return telegram

    @property
    def telegram(self):
        return self.build_telegram_from_control(self)

    async def send(self):
        global _last_queries_prune_at
        telegram = self.telegram
        if telegram is None:
            return

        query_codes = {
            OperateCode.ReadStatusOfChannels,
            OperateCode.ReadChannelLoadType,
            OperateCode.ReadLimitOfEveryChannel,
            OperateCode.ReadSafeguardTimeOfChannel,
            OperateCode.ReadDelayOfTurnOnChannel,
            OperateCode.IsDeviceOnline,
            OperateCode.ReadFirmwareVersion,
            OperateCode.ReadStatusOfUniversalSwitch,
            OperateCode.ReadSensorStatus,
            OperateCode.ReadSensorsInOneStatus,
            OperateCode.ReadFloorHeatingStatus,
            OperateCode.ReadFloorHeatingModuleStatus,
            OperateCode.ReadFloorHeatingTemperatureNew,
            OperateCode.ReadFloorHeatingTemperatureLegacy,
            OperateCode.ReadPanelAC,
            OperateCode.ReadDryContactStatus,
            OperateCode.ReadStatusofCurtainSwitch,
        }

        if telegram.operate_code in query_codes:
            now = time.time()
            if now >= _last_queries_prune_at:
                _last_queries_prune_at = now + _LAST_QUERIES_PRUNE_INTERVAL
                if len(_last_queries) > _LAST_QUERIES_MAX:
                    # Drop oldest entries to keep dedup memory bounded.
                    remove_count = len(_last_queries) - _LAST_QUERIES_MAX
                    for key, _ in sorted(_last_queries.items(), key=lambda item: item[1])[:remove_count]:
                        _last_queries.pop(key, None)
            key = (telegram.target_address, telegram.operate_code, tuple(telegram.payload or []))
            last_sent = _last_queries.get(key, 0.0)
            if now - last_sent < 4.0:
                _LOGGER.debug(
                    "DEDUPLICATOR: skip %s to %s payload=%s dt=%.2fs",
                    telegram.operate_code,
                    telegram.target_address,
                    telegram.payload,
                    now - last_sent,
                )
                return
            _last_queries[key] = now

        # if telegram.target_address[1] == 100:
        #     print("==== {}".format(str(telegram)))

        await self._buspro.network_interface.send_telegram(telegram)


class _GenericControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.payload = None
        self.operate_code = None


class _SingleChannelControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.channel_number = None
        self.channel_level = None
        self.running_time_minutes = None
        self.running_time_seconds = None


class _SceneControl(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.area_number = None
        self.scene_number = None


class _ReadStatusOfChannels(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _UniversalSwitch(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None
        self.switch_status = None


class _ReadStatusOfUniversalSwitch(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None


class _ReadSensorStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ReadSensorsInOneStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ReadFloorHeatingStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        # no more properties


class _ReadFloorHeatingModuleStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        self.channel_number = None


class _ReadFloorHeatingTemperatureNew(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        self.channel_number = None


class _ReadFloorHeatingTemperatureLegacy(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        self.channel_number = None


class _ControlFloorHeatingStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.temperature_type = None
        self.status = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None


class _ControlFloorHeatingModuleStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.channel_number = None
        self.work = None
        self.temperature_type = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None
        self.valve = None
        self.watering_time = None


class _ReadPanelAC(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        self.command = None


class _ControlPanelAC(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)
        self.command = None
        self.mode = None


class _ReadDryContactStatus(_Control):
    def __init__(self, buspro):
        super().__init__(buspro)

        self.switch_number = None
