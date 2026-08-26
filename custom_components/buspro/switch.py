"""
This component provides switch support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.switch import SwitchEntity, PLATFORM_SCHEMA
from homeassistant.const import (CONF_NAME, CONF_DEVICES)
from homeassistant.core import callback
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO
from .helpers.entity import (
    attach_entity_to_physical_device,
    device_info_for_address,
)
from .const import (
    CONF_CHANNELS,
    CONF_CHANNEL_ENABLED,
    CONF_CHANNEL_NUMBER,
    CONF_DEVICE_TYPE,
    CONF_MANAGED_DEVICES,
    DATA_BUSPRO_CONFIG,
    DEVICE_TYPE_RELAY,
    DOMAIN,
    CONF_ENABLE_CONFIRMATION,
    CONF_CONFIRMATION_TIMEOUT,
    CONF_CONFIRMATION_RETRIES,
    DEFAULT_ENABLE_CONFIRMATION,
    DEFAULT_CONFIRMATION_TIMEOUT,
    DEFAULT_CONFIRMATION_RETRIES,
)
from .managed import managed_device_info, is_runtime_channel, registry_disabled_update
from homeassistant.helpers import entity_registry as er

_LOGGER = logging.getLogger(__name__)

DEFAULT_OBJECT_ID = ""
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"

DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_NAME): cv.string,
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
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES): {cv.string: DEVICE_SCHEMA},
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    # noinspection PyUnresolvedReferences
    from .pybuspro.devices import Switch

    hdl = hass.data[DATA_BUSPRO].hdl
    devices = []

    for address, device_config in config[CONF_DEVICES].items():
        name = device_config[CONF_NAME]

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))
        channel_number = int(address2[2])
        _LOGGER.debug("Adding switch '{}' with address {} and channel number {}".format(name, device_address, channel_number))

        switch = Switch(hdl, device_address, channel_number, name)

        # Pass confirmation configuration to device
        switch.enable_confirmation = device_config.get(
            CONF_ENABLE_CONFIRMATION,
            DEFAULT_ENABLE_CONFIRMATION
        )
        switch.confirmation_timeout = device_config.get(
            CONF_CONFIRMATION_TIMEOUT,
            DEFAULT_CONFIRMATION_TIMEOUT
        )
        switch.confirmation_retries = device_config.get(
            CONF_CONFIRMATION_RETRIES,
            DEFAULT_CONFIRMATION_RETRIES
        )

        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name
        unique_id = device_config.get(CONF_UNIQUE_ID)

        devices.append(BusproSwitch(hass, switch, object_id, unique_id))

    async_add_entites(devices)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up UI-managed Buspro relay channels."""
    from .pybuspro.devices import RelayModule

    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    entity_registry = er.async_get(hass)
    entities = []
    relay_modules = {}
    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        if device_config[CONF_DEVICE_TYPE] != DEVICE_TYPE_RELAY:
            continue
        address = tuple(int(part) for part in device_config["address"].split("."))
        info = managed_device_info(device_config)
        for channel in device_config[CONF_CHANNELS]:
            channel_enabled = is_runtime_channel(channel)
            runtime_enabled = _sync_registry_enabled_state(
                entity_registry,
                channel[CONF_UNIQUE_ID],
                channel_enabled,
            )
            if not runtime_enabled and channel_enabled:
                continue
            relay_module = relay_modules.get(address)
            if relay_module is None:
                relay_module = RelayModule(module.hdl, address)
                relay_modules[address] = relay_module
            device = relay_module.channel(
                channel[CONF_CHANNEL_NUMBER],
                channel[CONF_NAME] or f"Channel {channel[CONF_CHANNEL_NUMBER]}",
            )
            entities.append(
                BusproSwitch(
                    hass,
                    device,
                    channel[CONF_OBJECT_ID],
                    channel[CONF_UNIQUE_ID],
                    device_info=info,
                    channel_enabled=channel_enabled,
                    module=module,
                )
            )
    async_add_entities(entities)


def _sync_registry_enabled_state(entity_registry, unique_id, channel_enabled):
    """Disable empty managed channels and re-enable configured channels."""
    entity_id = entity_registry.async_get_entity_id(
        "switch", DOMAIN, unique_id
    )
    if entity_id is None:
        return channel_enabled

    entry = entity_registry.async_get(entity_id)
    should_update, disabled_by = registry_disabled_update(
        channel_enabled, entry.disabled_by
    )
    if should_update:
        entry = entity_registry.async_update_entity(
            entity_id,
            disabled_by=(
                er.RegistryEntryDisabler.INTEGRATION
                if disabled_by == "integration"
                else None
            ),
        )
    return channel_enabled and entry.disabled_by is None


# noinspection PyAbstractClass
class BusproSwitch(SwitchEntity):
    """Representation of a Buspro switch."""

    def __init__(
        self,
        hass,
        device,
        object_id,
        unique_id=None,
        device_info=None,
        channel_enabled=True,
        module=None,
    ):
        self._hass = hass
        self._device = device
        self._module = module
        self._configured_unique_id = unique_id
        self._attr_device_info = device_info or device_info_for_address(
            hass, device.device_address
        )
        self._attr_extra_state_attributes = {
            "channel_number": device.channel_number,
            "channel_configured": channel_enabled,
        }
        self._channel_enabled = channel_enabled
        self._attr_entity_registry_enabled_default = channel_enabled
        self._device_update_cb = None
        self.entity_id = generate_entity_id("switch.{}", object_id, None, hass)

    async def async_added_to_hass(self):
        """Attach this YAML entity to its physical Buspro device."""
        await super().async_added_to_hass()
        self.async_register_callbacks()
        attach_entity_to_physical_device(
            self._hass, self, self._device.device_address
        )

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
        if self._device_update_cb is not None:
            try:
                self._device.unregister_device_updated_cb(self._device_update_cb)
            except ValueError:
                pass
            self._device_update_cb = None
        close = getattr(self._device, "close", None)
        if close is not None:
            close()
        await super().async_will_remove_from_hass()

    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return False

    @property
    def name(self):
        """Return the display name of this light."""
        return self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        connected = bool(
            self._module.connected if self._module is not None
            else self._hass.data[DATA_BUSPRO].connected
        )
        return self._channel_enabled and connected

    @property
    def is_on(self):
        """Return true if light is on."""
        return self._device.is_on

    async def async_turn_on(self, **kwargs):
        """Instruct the switch to turn on."""
        if not self._channel_enabled:
            raise HomeAssistantError("Buspro channel is not configured")
        await self._device.set_on()
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Instruct the switch to turn off."""
        if not self._channel_enabled:
            raise HomeAssistantError("Buspro channel is not configured")
        await self._device.set_off()
        self.async_write_ha_state()

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._configured_unique_id or self._device.device_identifier
