"""
This component provides fan support for Buspro.
"""

import logging
import time
import asyncio
from datetime import timedelta
from typing import Any, Optional

import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.event as event
import voluptuous as vol
from homeassistant.components.fan import FanEntity, FanEntityFeature, PLATFORM_SCHEMA
from homeassistant.const import CONF_DEVICES, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_RUNNING_TIME = 0
DEFAULT_PLATFORM_RUNNING_TIME = 0
DEFAULT_DIMMABLE = True
DEFAULT_ACK_RETRY = True
DEFAULT_OBJECT_ID = ""
CONF_ACK_RETRY = "ack_retry_enabled"
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Optional("running_time", default=DEFAULT_DEVICE_RUNNING_TIME): cv.positive_int,
        vol.Optional("dimmable", default=DEFAULT_DIMMABLE): cv.boolean,
        vol.Optional(CONF_ACK_RETRY, default=DEFAULT_ACK_RETRY): cv.boolean,
        vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
        vol.Required(CONF_NAME): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional("running_time", default=DEFAULT_PLATFORM_RUNNING_TIME): cv.positive_int,
        vol.Optional(CONF_ACK_RETRY, default=DEFAULT_ACK_RETRY): cv.boolean,
        vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
    }
)


async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro fan devices."""
    from .pybuspro.devices import Light

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []
    platform_running_time = int(config["running_time"])
    platform_ack_retry = bool(config[CONF_ACK_RETRY])

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        device_running_time = int(device_config["running_time"])
        dimmable = bool(device_config["dimmable"])
        ack_retry_enabled = bool(device_config.get(CONF_ACK_RETRY, platform_ack_retry))

        if device_running_time == 0:
            device_running_time = platform_running_time
        if dimmable:
            device_running_time = 0

        address_parts = address.split(".")
        device_address = (int(address_parts[0]), int(address_parts[1]))
        channel_number = int(address_parts[2])
        _LOGGER.debug(
            "Adding fan '%s' with address %s and channel number %s",
            name,
            device_address,
            channel_number,
        )

        fan_device = Light(
            hdl,
            device_address,
            channel_number,
            name,
            ack_retry_enabled=ack_retry_enabled,
        )
        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name
        unique_id = device_config.get(CONF_UNIQUE_ID)
        devices.append(BusproFan(hass, fan_device, device_running_time, dimmable, object_id, unique_id))

    async_add_entites(devices)
    if devices:
        sem = asyncio.Semaphore(5)

        async def _refresh(device):
            async with sem:
                await device.async_update()

        await asyncio.gather(*(_refresh(device) for device in devices))


class BusproFan(FanEntity):
    """Representation of a Buspro fan."""

    def __init__(self, hass, device, running_time, dimmable, object_id, unique_id=None):
        self._hass = hass
        self._device = device
        self._running_time = running_time
        self._dimmable = dimmable
        self._configured_unique_id = unique_id
        self._optimistic_percentage = None
        self._optimistic_timeout = 0.0
        self._device_update_cb = None
        self._unsub_start_poll = None
        self._unsub_poll_interval = None

        if self._dimmable:
            self._attr_supported_features = (
                FanEntityFeature.SET_SPEED
                | FanEntityFeature.TURN_ON
                | FanEntityFeature.TURN_OFF
            )
        else:
            self._attr_supported_features = (
                FanEntityFeature.TURN_ON | FanEntityFeature.TURN_OFF
            )

        self.async_register_callbacks()
        self.entity_id = generate_entity_id("fan.{}", object_id, None, hass)

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
        """Register callbacks to update state after device changes."""

        async def after_update_callback(device):
            self.async_write_ha_state()

        self._device_update_cb = after_update_callback
        self._device.register_device_updated_cb(after_update_callback)

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
        await super().async_will_remove_from_hass()

    @property
    def should_poll(self):
        return False

    async def async_update(self, *args):
        await self._device.read_status()

    @property
    def name(self):
        return self._device.name

    @property
    def available(self):
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def percentage(self) -> Optional[int]:
        if self._optimistic_percentage is not None:
            if time.time() <= self._optimistic_timeout:
                return self._optimistic_percentage
            self._optimistic_percentage = None
        return self._device.current_brightness

    @property
    def is_on(self):
        if self._optimistic_percentage is not None:
            if time.time() <= self._optimistic_timeout:
                return self._optimistic_percentage > 0
            self._optimistic_percentage = None
        return self._device.is_on

    async def async_set_percentage(self, percentage: int) -> None:
        if not self._dimmable:
            return
        brightness = max(0, min(100, int(percentage)))
        self._optimistic_percentage = brightness
        self._optimistic_timeout = time.time() + 2.0
        await self._device.set_brightness(brightness, self._running_time)
        self.async_write_ha_state()

    async def async_turn_on(
        self,
        percentage: Optional[int] = None,
        preset_mode: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        brightness = 100 if percentage is None else max(0, min(100, int(percentage)))

        if (
            not self.is_on
            and self._device.previous_brightness is not None
            and brightness == 100
        ):
            brightness = self._device.previous_brightness

        self._optimistic_percentage = brightness
        self._optimistic_timeout = time.time() + 2.0
        await self._device.set_brightness(brightness, self._running_time)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._optimistic_percentage = 0
        self._optimistic_timeout = time.time() + 2.0
        await self._device.set_off(self._running_time)
        self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._configured_unique_id or self._device.device_identifier
