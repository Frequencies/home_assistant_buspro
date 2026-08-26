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
from .helpers.entity import attach_entity_to_physical_device, device_info_for_address
from .const import (
    CONF_CHANNELS,
    CONF_CHANNEL_NUMBER,
    CONF_DEVICE_TYPE,
    CONF_MANAGED_DEVICES,
    DATA_BUSPRO_CONFIG,
    DEVICE_TYPE_COVER,
    CONF_ENABLE_CONFIRMATION,
    CONF_CONFIRMATION_TIMEOUT,
    CONF_CONFIRMATION_RETRIES,
    DEFAULT_ENABLE_CONFIRMATION,
    DEFAULT_CONFIRMATION_TIMEOUT,
    DEFAULT_CONFIRMATION_RETRIES,
)
from .managed import managed_device_info

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
        vol.Optional(
            CONF_ENABLE_CONFIRMATION,
            default=DEFAULT_ENABLE_CONFIRMATION
        ): cv.boolean,
        vol.Optional(
            CONF_CONFIRMATION_TIMEOUT,
            default=DEFAULT_CONFIRMATION_TIMEOUT
        ): vol.All(cv.positive_float, vol.Range(min=0.1, max=60)),
        vol.Optional(
            CONF_CONFIRMATION_RETRIES,
            default=DEFAULT_CONFIRMATION_RETRIES
        ): vol.All(cv.positive_int, vol.Range(min=0, max=10)),
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

        # Pass confirmation configuration to device
        cover.enable_confirmation = device_config.get(
            CONF_ENABLE_CONFIRMATION,
            DEFAULT_ENABLE_CONFIRMATION
        )
        cover.confirmation_timeout = device_config.get(
            CONF_CONFIRMATION_TIMEOUT,
            DEFAULT_CONFIRMATION_TIMEOUT
        )
        cover.confirmation_retries = device_config.get(
            CONF_CONFIRMATION_RETRIES,
            DEFAULT_CONFIRMATION_RETRIES
        )

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


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up UI-managed Buspro curtain channels."""
    from .pybuspro.devices import Cover

    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    entities = []
    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        if device_config[CONF_DEVICE_TYPE] != DEVICE_TYPE_COVER:
            continue
        address = tuple(int(part) for part in device_config["address"].split("."))
        info = managed_device_info(device_config)
        for channel in device_config[CONF_CHANNELS]:
            device = Cover(
                module.hdl,
                address,
                int(channel[CONF_CHANNEL_NUMBER]),
                channel[CONF_NAME],
            )
            entities.append(
                BusproCover(
                    hass,
                    device,
                    False,
                    channel[CONF_OBJECT_ID],
                    channel[CONF_UNIQUE_ID],
                    device_info=info,
                    module=module,
                )
            )
    async_add_entities(entities)


class BusproCover(CoverEntity):
    """Representation of a Buspro curtain/cover."""

    def __init__(
        self,
        hass,
        device,
        invert,
        object_id,
        unique_id=None,
        device_info=None,
        module=None,
    ):
        self._hass = hass
        self._device = device
        self._module = module
        self._invert = invert
        self._configured_unique_id = unique_id
        self._attr_device_info = device_info or device_info_for_address(
            hass, device.device_address
        )
        self._device_update_cb = None
        self._unsub_start_poll = None
        self._unsub_poll_interval = None
        self._polling_interval = timedelta(minutes=60)
        self._attr_supported_features = (
            CoverEntityFeature.OPEN
            | CoverEntityFeature.CLOSE
            | CoverEntityFeature.STOP
        )
        self.entity_id = generate_entity_id("cover.{}", object_id, None, hass)

    @callback
    def async_register_callbacks(self):
        async def after_update_callback(device):
            self.async_write_ha_state()

        self._device_update_cb = after_update_callback
        self._device.register_device_updated_cb(after_update_callback)

    async def async_added_to_hass(self):
        """Attach this YAML entity to its physical Buspro device."""
        await super().async_added_to_hass()
        attach_entity_to_physical_device(
            self._hass, self, self._device.device_address
        )

        # Register update callback and staggered poll timer only once added.
        self.async_register_callbacks()
        stagger = hash(str(self._device.device_address)) % 300

        @callback
        def _start_polling(_now):
            self._unsub_poll_interval = event.async_track_time_interval(
                self._hass, self.async_update, self._polling_interval
            )

        self._unsub_start_poll = event.async_call_later(self._hass, stagger, _start_polling)

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
        # Detach from the bus so telegram callbacks and pending tasks are freed.
        self._device.close()
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
        return bool(
            self._module.connected if self._module is not None
            else self._hass.data[DATA_BUSPRO].connected
        )

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
