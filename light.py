"""
This component provides light support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
import time
import asyncio
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import homeassistant.helpers.event as event
import voluptuous as vol
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_TRANSITION,
    ColorMode,
    LightEntity,
    LightEntityFeature,
    PLATFORM_SCHEMA,
)
from homeassistant.const import (CONF_NAME, CONF_DEVICES)
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id
from homeassistant.helpers.restore_state import (
    ExtraStoredData,
    RestoreEntity,
    RestoredExtraData,
)

from ..buspro import DATA_BUSPRO
from .entity_helpers import attach_entity_to_physical_device, device_info_for_address
from .const import (
    CONF_CHANNELS,
    CONF_CHANNEL_NUMBER,
    CONF_DEVICE_TYPE,
    CONF_MANAGED_DEVICES,
    DATA_BUSPRO_CONFIG,
    DEVICE_TYPE_DIMMER,
)
from .managed_devices import managed_device_info

_LOGGER = logging.getLogger(__name__)

DEFAULT_DEVICE_RUNNING_TIME = 0
DEFAULT_PLATFORM_RUNNING_TIME = 0
DEFAULT_DIMMABLE = True
DEFAULT_OBJECT_ID = ""
DEFAULT_ACK_RETRY = True

CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"
CONF_ACK_RETRY = "ack_retry_enabled"

DEVICE_SCHEMA = vol.Schema({
    vol.Optional("running_time", default=DEFAULT_DEVICE_RUNNING_TIME): cv.positive_int,
    vol.Optional("dimmable", default=DEFAULT_DIMMABLE): cv.boolean,
    vol.Optional(CONF_ACK_RETRY, default=DEFAULT_ACK_RETRY): cv.boolean,
    vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
    vol.Optional(CONF_UNIQUE_ID): cv.string,
    vol.Required(CONF_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional("running_time", default=DEFAULT_PLATFORM_RUNNING_TIME): cv.positive_int,
    vol.Optional(CONF_ACK_RETRY, default=DEFAULT_ACK_RETRY): cv.boolean,
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
    platform_ack_retry = bool(config[CONF_ACK_RETRY])

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]
        device_running_time = int(device_config["running_time"])
        dimmable = bool(device_config["dimmable"])
        ack_retry_enabled = bool(device_config.get(CONF_ACK_RETRY, platform_ack_retry))

        if device_running_time == 0:
            device_running_time = platform_running_time

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))
        channel_number = int(address2[2])
        _LOGGER.debug("Adding light '{}' with address {} and channel number {}".format(name, device_address, channel_number))

        light = Light(
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

        devices.append(BusproLight(hass, light, device_running_time, dimmable, object_id, unique_id))

    async_add_entites(devices)
    if devices:
        sem = asyncio.Semaphore(5)

        async def _refresh(device):
            async with sem:
                await device.async_update()

        await asyncio.gather(*(_refresh(device) for device in devices))


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up UI-managed Buspro dimmer channels."""
    from .pybuspro.devices import Light

    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    entities = []
    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        if device_config[CONF_DEVICE_TYPE] != DEVICE_TYPE_DIMMER:
            continue
        address = tuple(int(part) for part in device_config["address"].split("."))
        info = managed_device_info(device_config)
        for channel in device_config[CONF_CHANNELS]:
            device = Light(
                module.hdl,
                address,
                int(channel[CONF_CHANNEL_NUMBER]),
                channel[CONF_NAME],
            )
            entities.append(
                BusproLight(
                    hass,
                    device,
                    0,
                    True,
                    channel[CONF_OBJECT_ID],
                    channel[CONF_UNIQUE_ID],
                    device_info=info,
                )
            )
    async_add_entities(entities)


# noinspection PyAbstractClass
class BusproLight(RestoreEntity, LightEntity):
    """Representation of a Buspro light."""

    def __init__(
        self,
        hass,
        device,
        running_time,
        dimmable,
        object_id,
        unique_id=None,
        device_info=None,
    ):
        self._hass = hass
        self._device = device
        self._running_time = running_time
        self._dimmable = dimmable
        self._object_id = object_id
        self._configured_unique_id = unique_id
        self._attr_device_info = device_info or device_info_for_address(
            hass, device.device_address
        )
        self._optimistic_brightness = None
        self._optimistic_timeout = 0.0
        self._attr_color_mode = ColorMode.BRIGHTNESS
        self._attr_supported_color_modes = {ColorMode.BRIGHTNESS}
        self._attr_supported_features = LightEntityFeature.TRANSITION
        self._device_update_cb = None
        self._unsub_start_poll = None
        self._unsub_poll_interval = None
        self._polling_interval = timedelta(minutes=60)
        self.entity_id = generate_entity_id("light.{}", object_id, None, hass)

    @callback
    def async_register_callbacks(self):
        """Register callbacks to update hass after device was changed."""

        # noinspection PyUnusedLocal
        async def after_update_callback(device):
            """Call after device was updated."""
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
        # Detach the device from the bus so its telegram callback and any
        # pending tasks (ack watch, init read) are released on removal.
        self._device.close()
        await super().async_will_remove_from_hass()

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
        brightness = int(round(self._device.current_brightness / 100 * 255))
        return max(0, min(255, brightness))

    @property
    def is_on(self):
        """Return true if light is on."""
        if self._optimistic_brightness is not None:
            if time.time() <= self._optimistic_timeout:
                return self._optimistic_brightness > 0
            self._optimistic_brightness = None
        return self._device.is_on

    async def async_added_to_hass(self):
        """Restore last known brightness so turn_on after restart keeps previous level."""
        await super().async_added_to_hass()
        attach_entity_to_physical_device(
            self._hass, self, self._device.device_address
        )

        # Register bus/update callbacks and the staggered poll timer only once
        # the entity is actually added to hass (not from __init__).
        self.async_register_callbacks()
        stagger = hash(str(self._device._device_address)) % 300

        @callback
        def _start_polling(_now):
            self._unsub_poll_interval = event.async_track_time_interval(
                self._hass, self.async_update, self._polling_interval
            )

        self._unsub_start_poll = event.async_call_later(self._hass, stagger, _start_polling)

        last_state = await self.async_get_last_state()
        if last_state:
            brightness_255 = last_state.attributes.get(ATTR_BRIGHTNESS)
            if brightness_255 is not None:
                brightness_100 = max(1, min(100, int(brightness_255 / 255 * 100)))
                self._device.restore_previous_brightness(brightness_100)
                return

        extra_data = await self.async_get_last_extra_data()
        if extra_data:
            brightness_100 = int(extra_data.as_dict().get("previous_brightness") or 0)
            if brightness_100 > 0:
                self._device.restore_previous_brightness(brightness_100)

    @property
    def extra_restore_state_data(self) -> ExtraStoredData | None:
        """Persist previous non-zero brightness to survive off-state restarts."""
        if self._device.previous_brightness is None:
            return None
        return RestoredExtraData({"previous_brightness": self._device.previous_brightness})

    async def async_turn_on(self, **kwargs):
        """Instruct the light to turn on."""
        has_explicit_brightness = ATTR_BRIGHTNESS in kwargs
        if has_explicit_brightness:
            # Round rather than truncate, and never let an explicit on-request
            # collapse to 0 (which would read as "off").
            brightness = max(1, int(round(kwargs[ATTR_BRIGHTNESS] / 255 * 100)))
        elif self.is_on:
            brightness = max(1, self._device.current_brightness)
        elif self._device.previous_brightness is not None:
            brightness = self._device.previous_brightness
        else:
            brightness = 100

        brightness = max(0, min(100, int(brightness)))
        running_time = self._transition_seconds(kwargs)

        self._optimistic_brightness = int(brightness / 100 * 255)
        self._optimistic_timeout = time.time() + max(2.0, running_time + 2.0)
        await self._device.set_brightness(brightness, running_time)
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Instruct the light to turn off."""
        running_time = self._transition_seconds(kwargs)
        self._optimistic_brightness = 0
        self._optimistic_timeout = time.time() + max(2.0, running_time + 2.0)
        await self._device.set_off(running_time)
        self.async_write_ha_state()

    def _transition_seconds(self, kwargs):
        """Return a Buspro-compatible transition duration."""
        transition = kwargs.get(ATTR_TRANSITION, self._running_time)
        return max(0, min(15359, int(round(float(transition)))))

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._configured_unique_id or self._device.device_identifier
