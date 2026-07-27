"""Buspro climate platform."""

import logging
import asyncio
from typing import Optional, List
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.event as event
import voluptuous as vol
from homeassistant.components.climate import (
    PLATFORM_SCHEMA,
    ClimateEntity,
    ClimateEntityFeature,
    HVACMode,
    HVACAction,
)
from homeassistant.const import (
    CONF_NAME,
    CONF_DEVICES,
    CONF_ADDRESS,
    UnitOfTemperature,
    ATTR_TEMPERATURE,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO
from .pybuspro.devices.climate import ControlFloorHeatingStatus, ControlPanelAC
from .pybuspro.helpers.enums import (
    OnOffStatus,
    ClimateDeviceType,
    FloorHeatingDeviceType,
    WorkType,
)

_LOGGER = logging.getLogger(__name__)

PRESET_NONE = "none"
PRESET_AWAY = "away"
PRESET_HOME = "home"
PRESET_SLEEP = "sleep"

HA_PRESET_TO_HDL = {
    PRESET_NONE: 1,
    PRESET_HOME: 2,
    PRESET_SLEEP: 3,
    PRESET_AWAY: 4,
}
HDL_TO_HA_PRESET = {
    1: PRESET_NONE,
    2: PRESET_HOME,
    3: PRESET_SLEEP,
    4: PRESET_AWAY,
}

DEFAULT_OBJECT_ID = ""
CONF_PRESET_MODES = "preset_modes"
CONF_RELAY_ADDRESS = "relay_address"
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"
CONF_CHANNEL = "channel"
CONF_TYPE = "type"
CONF_FH_DEVICE_TYPE = "floor_heating_device_type"
CONF_MIN_TEMP = "min_temp"
CONF_MAX_TEMP = "max_temp"
CONF_PRECISION = "precision"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): vol.All(
        cv.ensure_list,
        [
            vol.All(
                {
                    vol.Required(CONF_ADDRESS): cv.string,
                    vol.Required(CONF_NAME): cv.string,
                    vol.Optional(CONF_TYPE, default=ClimateDeviceType.FloorHeating.value): vol.In(
                        [x.value for x in ClimateDeviceType]
                    ),
                    vol.Optional(CONF_FH_DEVICE_TYPE): vol.In([x.value for x in FloorHeatingDeviceType]),
                    vol.Optional(CONF_PRESET_MODES, default=[]): vol.All(
                        cv.ensure_list, [vol.In(HA_PRESET_TO_HDL)]
                    ),
                    vol.Optional(CONF_RELAY_ADDRESS, default=""): cv.string,
                    vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
                    vol.Optional(CONF_UNIQUE_ID): cv.string,
                    vol.Optional(CONF_CHANNEL): vol.All(vol.Coerce(int), vol.Range(min=1, max=6)),
                    vol.Optional(CONF_MIN_TEMP): vol.Coerce(float),
                    vol.Optional(CONF_MAX_TEMP): vol.Coerce(float),
                    vol.Optional(CONF_PRECISION): vol.In([1, 0.5, 0.1]),
                }
            )
        ],
    )
})


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    from .pybuspro.devices import Climate, FloorHeating, Sensor

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        preset_modes = device_config[CONF_PRESET_MODES]
        climate_type = device_config[CONF_TYPE]
        channel_number = device_config.get(CONF_CHANNEL)

        address2 = address.split(".")
        device_address = (int(address2[0]), int(address2[1]))

        relay_sensor = None
        relay_address = device_config[CONF_RELAY_ADDRESS]
        if relay_address:
            relay_address2 = relay_address.split(".")
            relay_device_address = (int(relay_address2[0]), int(relay_address2[1]))
            relay_channel_number = int(relay_address2[2])
            relay_sensor = Sensor(hdl, relay_device_address, channel_number=relay_channel_number)

        object_id = device_config[CONF_OBJECT_ID] or name
        unique_id = device_config.get(CONF_UNIQUE_ID)
        min_temp = device_config.get(CONF_MIN_TEMP)
        max_temp = device_config.get(CONF_MAX_TEMP)
        precision = device_config.get(CONF_PRECISION)

        if climate_type == ClimateDeviceType.AC.value:
            device = Climate(hdl, device_address, name)
            devices.append(
                BusproACClimate(
                    hass, device, relay_sensor, object_id, unique_id, min_temp, max_temp, precision
                )
            )
            continue

        fh_type_raw = device_config.get(CONF_FH_DEVICE_TYPE)
        if fh_type_raw:
            fh_type = FloorHeatingDeviceType(fh_type_raw)
        else:
            fh_type = FloorHeatingDeviceType.Module if channel_number is not None else FloorHeatingDeviceType.DLP

        if fh_type == FloorHeatingDeviceType.Module and channel_number is None:
            _LOGGER.error("Missing 'channel' for floor heating module '%s'", name)
            continue

        device = FloorHeating(hdl, device_address, name, channel_number=channel_number, device_type=fh_type)
        devices.append(BusproFloorHeatingClimate(
            hass, device, preset_modes, relay_sensor, object_id, unique_id, min_temp, max_temp, precision
        ))

    async_add_entities(devices)
    if devices:
        sem = asyncio.Semaphore(5)

        async def _refresh(device):
            async with sem:
                await device.async_update()

        await asyncio.gather(*(_refresh(device) for device in devices))


class _BusproClimateBase(ClimateEntity):
    def __init__(
        self,
        hass,
        device,
        relay_sensor,
        object_id,
        unique_id=None,
        min_temp=None,
        max_temp=None,
        precision=None,
    ):
        self._hass = hass
        self._device = device
        self._relay_sensor = relay_sensor
        self._relay_sensor_is_on = relay_sensor.single_channel_is_on if relay_sensor is not None else None
        self._device_update_cb = None
        self._relay_sensor_update_cb = None
        self._unsub_start_poll = None
        self._unsub_poll_interval = None
        self._configured_unique_id = unique_id
        self._configured_min_temp = min_temp
        self._configured_max_temp = max_temp
        self._configured_precision = precision
        self.async_register_callbacks()
        self.entity_id = generate_entity_id("climate.{}", object_id, None, hass)

        self._polling_interval = timedelta(minutes=60)
        stagger = hash(str(self._device._device_address)) % 300

        @callback
        def _start_polling(_now):
            self._unsub_poll_interval = event.async_track_time_interval(
                self._hass, self.async_update, self._polling_interval
            )

        self._unsub_start_poll = event.async_call_later(self._hass, stagger, _start_polling)

    @callback
    def async_register_callbacks(self):
        async def after_update_callback(device):
            self._device = device
            self.async_write_ha_state()

        self._device_update_cb = after_update_callback
        self._device.register_device_updated_cb(after_update_callback)

        if self._relay_sensor is not None:
            async def after_relay_sensor_update_callback(device):
                self._relay_sensor_is_on = device.single_channel_is_on
                self.async_write_ha_state()

            self._relay_sensor_update_cb = after_relay_sensor_update_callback
            self._relay_sensor.register_device_updated_cb(after_relay_sensor_update_callback)

    async def async_will_remove_from_hass(self):
        if self._unsub_start_poll is not None:
            self._unsub_start_poll()
            self._unsub_start_poll = None
        if self._unsub_poll_interval is not None:
            self._unsub_poll_interval()
            self._unsub_poll_interval = None
        if self._device_update_cb is not None:
            try:
                self._device.unregister_device_updated_cb(self._device_update_cb)
            except ValueError:
                pass
            self._device_update_cb = None
        if self._relay_sensor is not None and self._relay_sensor_update_cb is not None:
            try:
                self._relay_sensor.unregister_device_updated_cb(self._relay_sensor_update_cb)
            except ValueError:
                pass
            self._relay_sensor_update_cb = None
        await super().async_will_remove_from_hass()

    @property
    def should_poll(self):
        return False

    async def async_update(self, *args):
        await self._device.read_status()
        if self._relay_sensor is not None:
            await self._relay_sensor.read_sensor_status()

    @property
    def name(self):
        return self._device.name

    @property
    def available(self):
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self._device.temperature

    @property
    def target_temperature_step(self):
        return self._configured_precision if self._configured_precision is not None else 1

    @property
    def min_temp(self):
        if self._configured_min_temp is not None:
            return self._configured_min_temp
        return super().min_temp

    @property
    def max_temp(self):
        if self._configured_max_temp is not None:
            return self._configured_max_temp
        return super().max_temp

    @property
    def precision(self):
        if self._configured_precision is not None:
            return self._configured_precision
        return super().precision

    @property
    def unique_id(self):
        return self._configured_unique_id or self._device.device_identifier


class BusproACClimate(_BusproClimateBase):
    def __init__(
        self, hass, device, relay_sensor, object_id, unique_id=None, min_temp=None, max_temp=None, precision=None
    ):
        super().__init__(hass, device, relay_sensor, object_id, unique_id, min_temp, max_temp, precision)
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )

    @property
    def hvac_action(self):
        if self._device.is_on:
            return HVACAction.COOLING if (self._relay_sensor_is_on is None or self._relay_sensor_is_on) else HVACAction.IDLE
        return HVACAction.OFF

    @property
    def hvac_mode(self):
        return HVACMode.COOL if self._device.is_on else HVACMode.OFF

    @property
    def hvac_modes(self):
        return [HVACMode.COOL, HVACMode.OFF]

    @property
    def target_temperature(self):
        return self._device.target_temperature

    async def async_turn_off(self) -> None:
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_turn_on(self) -> None:
        await self.async_set_hvac_mode(HVACMode.COOL)

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        control = ControlPanelAC()
        if hvac_mode == HVACMode.OFF:
            control.status = OnOffStatus.OFF.value
        elif hvac_mode == HVACMode.COOL:
            control.status = OnOffStatus.ON.value
        else:
            _LOGGER.error("Unsupported AC hvac mode: %s", hvac_mode)
            return

        await self._device.control_ac_status(control)
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return
        control = ControlPanelAC()
        control.normal_temperature = int(temperature)
        await self._device.control_ac_temperature(control)
        self.async_write_ha_state()


class BusproFloorHeatingClimate(_BusproClimateBase):
    def __init__(
        self,
        hass,
        device,
        preset_modes,
        relay_sensor,
        object_id,
        unique_id=None,
        min_temp=None,
        max_temp=None,
        precision=None,
    ):
        super().__init__(hass, device, relay_sensor, object_id, unique_id, min_temp, max_temp, precision)
        self._preset_modes = preset_modes
        self._attr_supported_features = (
            ClimateEntityFeature.TARGET_TEMPERATURE
            | ClimateEntityFeature.PRESET_MODE
            | ClimateEntityFeature.TURN_OFF
            | ClimateEntityFeature.TURN_ON
        )

    @property
    def target_temperature(self):
        return self._device.target_temperature

    @property
    def preset_mode(self) -> Optional[str]:
        return HDL_TO_HA_PRESET.get(self._device.mode, PRESET_NONE)

    @property
    def preset_modes(self) -> Optional[List[str]]:
        if len(self._preset_modes) == 0:
            return None
        keys = HA_PRESET_TO_HDL.keys() & self._preset_modes
        return list({k: HA_PRESET_TO_HDL[k] for k in keys})

    async def async_set_preset_mode(self, preset_mode: str) -> None:
        if preset_mode not in HA_PRESET_TO_HDL:
            preset_mode = PRESET_NONE
        control = ControlFloorHeatingStatus()
        control.mode = HA_PRESET_TO_HDL[preset_mode]
        await self._device.control_heating_status(control)
        self.async_write_ha_state()

    @property
    def hvac_action(self):
        if not self._device.is_on:
            return HVACAction.OFF
        if self._relay_sensor_is_on is None:
            return HVACAction.HEATING
        return HVACAction.HEATING if self._relay_sensor_is_on else HVACAction.IDLE

    @property
    def hvac_mode(self):
        if not self._device.is_on:
            return HVACMode.OFF
        if self._device.work_type in (WorkType.Cooling, WorkType.CoolingPower):
            return HVACMode.COOL
        return HVACMode.HEAT

    @property
    def hvac_modes(self):
        if self._device._device_type == FloorHeatingDeviceType.Module:
            return [HVACMode.HEAT, HVACMode.COOL, HVACMode.OFF]
        return [HVACMode.HEAT, HVACMode.OFF]

    async def async_turn_off(self) -> None:
        await self.async_set_hvac_mode(HVACMode.OFF)

    async def async_turn_on(self) -> None:
        await self.async_set_hvac_mode(HVACMode.HEAT)

    async def async_set_hvac_mode(self, hvac_mode: str) -> None:
        control = ControlFloorHeatingStatus()

        if hvac_mode == HVACMode.OFF:
            control.status = OnOffStatus.OFF.value
        elif hvac_mode == HVACMode.HEAT:
            control.status = OnOffStatus.ON.value
            control.work_type = WorkType.Heating
        elif hvac_mode == HVACMode.COOL and self._device._device_type == FloorHeatingDeviceType.Module:
            control.status = OnOffStatus.ON.value
            control.work_type = WorkType.Cooling
        else:
            _LOGGER.error("Unsupported floor heating hvac mode: %s", hvac_mode)
            return

        await self._device.control_heating_status(control)
        self.async_write_ha_state()

    async def async_set_temperature(self, **kwargs):
        temperature = kwargs.get(ATTR_TEMPERATURE)
        if temperature is None:
            return

        control = ControlFloorHeatingStatus()
        target_temperature = int(temperature)
        preset = HDL_TO_HA_PRESET.get(self._device.mode, PRESET_NONE)

        if preset == PRESET_NONE:
            control.normal_temperature = target_temperature
        elif preset == PRESET_HOME:
            control.day_temperature = target_temperature
        elif preset == PRESET_SLEEP:
            control.night_temperature = target_temperature
        elif preset == PRESET_AWAY:
            control.away_temperature = target_temperature
        else:
            control.normal_temperature = target_temperature

        await self._device.control_heating_status(control)
        self.async_write_ha_state()
