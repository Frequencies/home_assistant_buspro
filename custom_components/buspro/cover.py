"""
This component provides cover support for Buspro.
"""

import logging
import asyncio
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.event as event
import voluptuous as vol
from homeassistant.components.cover import (
    CoverEntity,
    CoverEntityFeature,
    PLATFORM_SCHEMA,
)
from homeassistant.const import CONF_DEVICES, CONF_NAME
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO

_LOGGER = logging.getLogger(__name__)

DEFAULT_INVERT = False
DEFAULT_OBJECT_ID = ""
CONF_INVERT = "invert"
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"

DEVICE_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_NAME): cv.string,
        vol.Optional(CONF_INVERT, default=DEFAULT_INVERT): cv.boolean,
        vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
        vol.Optional(CONF_UNIQUE_ID): cv.string,
    }
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up Buspro cover devices."""
    from .pybuspro.devices import Cover

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        invert = bool(device_config[CONF_INVERT])

        address2 = address.split(".")
        device_address = (int(address2[0]), int(address2[1]))
        channel_number = int(address2[2])
        _LOGGER.debug(
            "Adding cover '%s' with address %s and channel number %s (invert=%s)",
            name,
            device_address,
            channel_number,
            invert,
        )

        cover = Cover(hdl, device_address, channel_number, name)

        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name
        unique_id = device_config.get(CONF_UNIQUE_ID)

        devices.append(BusproCover(hass, cover, invert, object_id, unique_id))

    async_add_entities(devices)
    if devices:
        sem = asyncio.Semaphore(5)

        async def _refresh(device):
            async with sem:
                await device.async_update()

        await asyncio.gather(*(_refresh(device) for device in devices))


class BusproCover(CoverEntity):
    """Representation of a Buspro curtain/cover."""

    def __init__(self, hass, device, invert, object_id, unique_id=None):
        self._hass = hass
        self._device = device
        self._invert = invert
        self._configured_unique_id = unique_id
        self._device_update_cb = None
        self._unsub_start_poll = None
        self._unsub_poll_interval = None
        self.async_register_callbacks()
        self.entity_id = generate_entity_id("cover.{}", object_id, None, hass)

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
    def is_opening(self):
        return self._device.is_closing if self._invert else self._device.is_opening

    @property
    def is_closing(self):
        return self._device.is_opening if self._invert else self._device.is_closing

    @property
    def is_closed(self):
        # Buspro curtain status feedback does not expose absolute position/closed state.
        return None

    @property
    def supported_features(self):
        return (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
            | CoverEntityFeature.OPEN_TILT
            | CoverEntityFeature.CLOSE_TILT
            | CoverEntityFeature.STOP_TILT
        )

    async def async_open_cover(self, **kwargs):
        if self._invert:
            await self._device.close_cover()
        else:
            await self._device.open_cover()
        self.async_write_ha_state()

    async def async_close_cover(self, **kwargs):
        if self._invert:
            await self._device.open_cover()
        else:
            await self._device.close_cover()
        self.async_write_ha_state()

    async def async_stop_cover(self, **kwargs):
        await self._device.stop_cover()
        self.async_write_ha_state()

    async def async_open_cover_tilt(self, **kwargs):
        if self._invert:
            await self._device.close_cover_tilt()
        else:
            await self._device.open_cover_tilt()
        self.async_write_ha_state()

    async def async_close_cover_tilt(self, **kwargs):
        if self._invert:
            await self._device.open_cover_tilt()
        else:
            await self._device.close_cover_tilt()
        self.async_write_ha_state()

    async def async_stop_cover_tilt(self, **kwargs):
        await self._device.stop_cover_tilt()
        self.async_write_ha_state()

    @property
    def unique_id(self):
        return self._configured_unique_id or self._device.device_identifier
