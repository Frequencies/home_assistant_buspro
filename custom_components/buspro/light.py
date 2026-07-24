"""
This component provides light support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
import time
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.event as event
import voluptuous as vol
from homeassistant.components.light import (
    LightEntity, 
    ColorMode, 
    PLATFORM_SCHEMA, 
    ATTR_BRIGHTNESS
)
from homeassistant.const import (CONF_NAME, CONF_DEVICES)
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_RUNNING_TIME = 0
DEFAULT_PLATFORM_RUNNING_TIME = 0
DEFAULT_DIMMABLE = True
DEFAULT_OBJECT_ID = ""

CONF_OBJECT_ID = "object_id"

DEVICE_SCHEMA = vol.Schema({
    vol.Optional("running_time", default=DEFAULT_DEVICE_RUNNING_TIME): cv.positive_int,
    vol.Optional("dimmable", default=DEFAULT_DIMMABLE): cv.boolean,
    vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
    vol.Required(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("running_time", default=DEFAULT_PLATFORM_RUNNING_TIME): cv.positive_int,
    vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro light devices."""
    # noinspection PyUnresolvedReferences
    from .pybuspro.devices import Light

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []
    platform_running_time = int(config["running_time"])

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        device_running_time = int(device_config["running_time"])
        dimmable = bool(device_config["dimmable"])

        if device_running_time == 0:
            device_running_time = platform_running_time
        if dimmable:
            device_running_time = 0

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))
        channel_number = int(address2[2])
        _LOGGER.debug("Adding light '{}' with address {} and channel number {}".format(name, device_address, channel_number))

        light = Light(hdl, device_address, channel_number, name)

        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name

        devices.append(BusproLight(hass, light, device_running_time, dimmable, object_id))

    async_add_entites(devices)


# noinspection PyAbstractClass
class BusproLight(LightEntity):
    """Representation of a Buspro light."""

    def __init__(self, hass, device, running_time, dimmable, object_id):
        self._hass = hass
        self._device = device
        self._running_time = running_time
        self._dimmable = dimmable
        self._object_id = object_id
        self._optimistic_brightness = None
        self._optimistic_timeout = 0.0
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self.async_register_callbacks()
        self.entity_id = generate_entity_id("light.{}", object_id, None, hass)

        self._polling_interval = timedelta(minutes=60)
        stagger = hash(str(self._device._device_address)) % 300

        @callback
        def _start_polling(_now):
            event.async_track_time_interval(hass, self.async_update, self._polling_interval)

        event.async_call_later(hass, stagger, _start_polling)

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
            self.async_write_ha_state()

        self._device.register_device_updated_cb(after_update_callback)

    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return False

    async def async_update(self, *args):
        await self._device.read_status()

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return self._hass.data[DATA_BUSPRO].connected

    @property
    def brightness(self):
        """Return the brightness of the light."""
        if self._optimistic_brightness is not None:
            if time.time() <= self._optimistic_timeout:
                return self._optimistic_brightness
            self._optimistic_brightness = None
        brightness = self._device.current_brightness / 100 * 255
        return brightness

    @property
    def is_on(self):
        """Return true if light is on."""
        if self._optimistic_brightness is not None:
            if time.time() <= self._optimistic_timeout:
                return self._optimistic_brightness > 0
            self._optimistic_brightness = None
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        brightness = int(kwargs.get(ATTR_BRIGHTNESS, 255) / 255 * 100)

        if not self.is_on and self._device.previous_brightness is not None and brightness == 100:
            brightness = self._device.previous_brightness

        self._optimistic_brightness = int(brightness / 100 * 255)
        self._optimistic_timeout = time.time() + 2.0
        await self._device.set_brightness(brightness, self._running_time)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        self._optimistic_brightness = 0
        self._optimistic_timeout = time.time() + 2.0
        await self._device.set_off(self._running_time)
        self.async_write_ha_state()

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._device.device_identifier
