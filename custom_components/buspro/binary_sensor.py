"""
This component provides binary sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.binary_sensor import (
    PLATFORM_SCHEMA, 
    BinarySensorEntity,
    BinarySensorDeviceClass,
)
from homeassistant.const import (
    CONF_NAME, 
    CONF_DEVICES, 
    CONF_ADDRESS, 
    CONF_TYPE, 
    CONF_DEVICE_CLASS, 
    CONF_SCAN_INTERVAL,
    EntityCategory,
)
from homeassistant.core import callback
from homeassistant.helpers.entity import generate_entity_id

from ..buspro import DATA_BUSPRO
from .const import (
    CONF_CHANNELS,
    CONF_CHANNEL_NUMBER,
    CONF_DEVICE_TYPE,
    CONF_ENTITIES,
    CONF_MANAGED_DEVICES,
    CONF_PROFILE,
    DATA_BUSPRO_CONFIG,
    DEVICE_TYPE_DRY_CONTACT,
    DEVICE_TYPE_MULTISENSOR,
    DEVICE_TYPE_UNIVERSAL_SWITCH,
)
from .helpers.dimmer import dimmer_diagnostic_definitions
from .helpers.entity import (
    attach_entity_to_physical_device,
    build_device_info,
    device_info_for_address,
    parse_device_address,
)
from .catalog import DEVICE_CATALOG
from .managed import managed_device_info
from .helpers.logic_controller import (
    logic_controller_coordinator,
    logic_controller_definitions,
)

_LOGGER = logging.getLogger(__name__)

DEFAULT_CONF_DEVICE_CLASS = None
DEFAULT_CONF_SCAN_INTERVAL = 0
DEFAULT_OBJECT_ID = ""

CONF_MOTION = 'motion'
CONF_DRY_CONTACT_1 = 'dry_contact_1'
CONF_DRY_CONTACT_2 = 'dry_contact_2'
CONF_UNIVERSAL_SWITCH = 'universal_switch'
CONF_SINGLE_CHANNEL = 'single_channel'
CONF_DRY_CONTACT = 'dry_contact'
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"
CONF_DEVICE = "device"

SENSOR_TYPES = {
    CONF_MOTION,
    CONF_DRY_CONTACT_1,
    CONF_DRY_CONTACT_2,
    CONF_UNIVERSAL_SWITCH,
    CONF_SINGLE_CHANNEL,
    CONF_DRY_CONTACT,
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_DEVICE_CLASS, default=DEFAULT_CONF_DEVICE_CLASS): vol.Any(None, cv.string),
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_CONF_SCAN_INTERVAL): cv.positive_int,
                vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
                vol.Optional(CONF_UNIQUE_ID): cv.string,
                vol.Optional(CONF_DEVICE): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    module = hass.data[DATA_BUSPRO]

    if discovery_info is not None:
        async_add_entites(_compound_binary_sensor_entities(hass, module))
        return

    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        sensor_type = device_config[CONF_TYPE]
        device_class = device_config[CONF_DEVICE_CLASS]
        device = device_config.get(CONF_DEVICE)
        universal_switch_number = None
        channel_number = None
        switch_number = None

        scan_interval = device_config[CONF_SCAN_INTERVAL]
        interval = 0
        if scan_interval is not None:
            interval = int(scan_interval)
            

        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        if sensor_type == CONF_UNIVERSAL_SWITCH:
            universal_switch_number = int(address2[2])
            _LOGGER.debug("Adding binary sensor '{}' with address {}, universal_switch_number {}, sensor type '{}' "
                            "and device class '{}'".format(name, device_address, universal_switch_number, sensor_type,
                            device_class))
        elif sensor_type == CONF_SINGLE_CHANNEL:
            channel_number = int(address2[2])
            _LOGGER.debug("Adding binary sensor '{}' with address {}, channel_number {}, sensor type '{}' and "
                            "device class '{}'".format(name, device_address, channel_number, sensor_type, device_class))
        elif sensor_type == CONF_DRY_CONTACT:
            switch_number = int(address2[2])
            _LOGGER.debug("Adding binary sensor '{}' with address {}, switch_number '{}' and "
                            "device class '{}'".format(name, device_address, switch_number, device_class))
        else:
            _LOGGER.debug("Adding binary sensor '{}' with address {}, sensor type '{}' and device class '{}'".
                            format(name, device_address, sensor_type, device_class))

        sensor = module.get_sensor(
            device_address,
            profile=device,
            universal_switch_number=universal_switch_number,
            channel_number=channel_number,
            switch_number=switch_number,
            name=name,
        )
        
        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name
        unique_id = device_config.get(CONF_UNIQUE_ID)

        devices.append(
            BusproBinarySensor(
                hass,
                sensor,
                sensor_type,
                device_class,
                interval,
                object_id,
                unique_id,
                name=name,
            )
        )

    async_add_entites(devices)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up binary sensors generated from physical Buspro devices."""
    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    entities = _compound_binary_sensor_entities(hass, module)
    entities.extend(_managed_binary_sensor_entities(hass, module, config_entry))
    entities.extend(_dimmer_connectivity_entities(hass, module, config_entry))
    entities.extend(_logic_controller_connectivity_entities(hass, module, config_entry))
    async_add_entities(entities)


def _logic_controller_connectivity_entities(hass, module, config_entry):
    """Create connectivity diagnostics for registered logic controllers."""
    return [
        BusproLogicControllerConnectivitySensor(
            logic_controller_coordinator(module, address), address, device_info,
            module=module,
        )
        for address, device_info in logic_controller_definitions(
            hass, config_entry
        ).items()
    ]


class BusproLogicControllerConnectivitySensor(BinarySensorEntity):
    """Connectivity status of an HDL logic controller."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_name = "Connectivity"
    _attr_should_poll = False

    def __init__(self, coordinator, address, device_info, module=None):
        self._coordinator = coordinator
        self._module = module
        self._device_update_cb = None
        self._attr_device_info = device_info
        self._attr_unique_id = f"buspro-{address}-logic-connectivity"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        async def _updated(_device):
            self.async_write_ha_state()

        self._device_update_cb = _updated
        self._coordinator.register_device_updated_cb(_updated)

    async def async_will_remove_from_hass(self):
        if self._device_update_cb is not None:
            self._coordinator.unregister_device_updated_cb(
                self._device_update_cb
            )
            self._device_update_cb = None
        await super().async_will_remove_from_hass()

    @property
    def available(self):
        connected = self._module.connected if self._module is not None else True
        return connected and self._coordinator.online is not None

    @property
    def is_on(self):
        return self._coordinator.online


def _dimmer_connectivity_entities(hass, module, config_entry):
    """Create device-connectivity diagnostics for supported dimmers."""
    entities = []
    for address, (channel_count, device_info) in dimmer_diagnostic_definitions(
        hass, config_entry
    ).items():
        diagnostics = module.get_dimmer_diagnostics(
            parse_device_address(address), channel_count
        )
        entities.append(
            BusproDimmerConnectivitySensor(
                hass, diagnostics, address, device_info, module=module,
            )
        )
    return entities


class BusproDimmerConnectivitySensor(BinarySensorEntity):
    """Connectivity status reported by an HDL dimmer."""

    _attr_device_class = BinarySensorDeviceClass.CONNECTIVITY
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_name = "Connectivity"
    _attr_should_poll = False

    def __init__(self, hass, diagnostics, address, device_info, module=None):
        self._hass = hass
        self._diagnostics = diagnostics
        self._module = module
        self._device_update_cb = None
        self._attr_device_info = device_info
        self._attr_unique_id = f"buspro-{address}-dimmer-connectivity"

    async def async_added_to_hass(self):
        await super().async_added_to_hass()

        async def _updated(_device):
            self.async_write_ha_state()

        self._device_update_cb = _updated
        self._diagnostics.register_device_updated_cb(_updated)

    async def async_will_remove_from_hass(self):
        if self._device_update_cb is not None:
            self._diagnostics.unregister_device_updated_cb(self._device_update_cb)
            self._device_update_cb = None
        await super().async_will_remove_from_hass()

    @property
    def available(self):
        connected = self._module.connected if self._module is not None else True
        return connected and self._diagnostics.online is not None

    @property
    def is_on(self):
        return self._diagnostics.online


def _compound_binary_sensor_entities(hass, module):
    devices = []
    for device_config in hass.data[DATA_BUSPRO_CONFIG].get("configured_devices", []):
        device_address = parse_device_address(device_config[CONF_ADDRESS])
        sensor = module.get_sensor(
            device_address,
            profile=device_config[CONF_PROFILE],
            name=device_config[CONF_NAME],
        )
        device_info = build_device_info(device_config)

        for entity_config in device_config[CONF_ENTITIES]:
            sensor_type = entity_config[CONF_TYPE]
            if sensor_type not in {CONF_MOTION, CONF_DRY_CONTACT_1, CONF_DRY_CONTACT_2}:
                continue

            devices.append(
                BusproBinarySensor(
                    hass,
                    sensor,
                    sensor_type,
                    entity_config.get(CONF_DEVICE_CLASS),
                    entity_config[CONF_SCAN_INTERVAL],
                    entity_config[CONF_OBJECT_ID],
                    entity_config.get(CONF_UNIQUE_ID),
                    name=entity_config[CONF_NAME],
                    device_info=device_info,
                    module=module,
                )
            )
    return devices


def _managed_binary_sensor_entities(hass, module, config_entry):
    """Create binary entities for UI-managed Buspro devices."""
    entities = []
    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        device_type = device_config[CONF_DEVICE_TYPE]
        address = parse_device_address(device_config["address"])
        info = managed_device_info(device_config)

        if device_type == DEVICE_TYPE_DRY_CONTACT:
            for channel in device_config[CONF_CHANNELS]:
                channel_number = int(channel[CONF_CHANNEL_NUMBER])
                sensor = module.get_sensor(
                    address,
                    switch_number=channel_number,
                    name=channel[CONF_NAME],
                )
                entities.append(
                    BusproBinarySensor(
                        hass,
                        sensor,
                        CONF_DRY_CONTACT,
                        None,
                        0,
                        channel[CONF_OBJECT_ID],
                        channel[CONF_UNIQUE_ID],
                        name=channel[CONF_NAME],
                        device_info=info,
                        module=module,
                    )
                )
            continue

        if device_type == DEVICE_TYPE_UNIVERSAL_SWITCH:
            for channel in device_config[CONF_CHANNELS]:
                switch_number = int(channel[CONF_CHANNEL_NUMBER])
                sensor = module.get_sensor(
                    address,
                    universal_switch_number=switch_number,
                    name=channel[CONF_NAME],
                )
                entities.append(
                    BusproBinarySensor(
                        hass,
                        sensor,
                        CONF_UNIVERSAL_SWITCH,
                        None,
                        0,
                        channel[CONF_OBJECT_ID],
                        channel[CONF_UNIQUE_ID],
                        name=channel[CONF_NAME],
                        device_info=info,
                        module=module,
                    )
                )
            continue

        if device_type != DEVICE_TYPE_MULTISENSOR:
            continue
        spec = DEVICE_CATALOG[device_config["model"]]
        sensor = module.get_sensor(
            address,
            profile=spec["profile"],
            name=device_config["name"],
        )
        for channel in device_config[CONF_CHANNELS]:
            sensor_type = channel[CONF_CHANNEL_NUMBER]
            if sensor_type not in {
                CONF_MOTION,
                CONF_DRY_CONTACT_1,
                CONF_DRY_CONTACT_2,
            }:
                continue
            entities.append(
                BusproBinarySensor(
                    hass,
                    sensor,
                    sensor_type,
                    None,
                    0,
                    channel[CONF_OBJECT_ID],
                    channel[CONF_UNIQUE_ID],
                    name=channel[CONF_NAME],
                    device_info=info,
                    module=module,
                )
            )
    return entities


# noinspection PyAbstractClass
class BusproBinarySensor(BinarySensorEntity):
    """Representation of a Buspro switch."""

    def __init__(
        self,
        hass,
        device,
        sensor_type,
        device_class,
        scan_interval,
        object_id,
        unique_id=None,
        name=None,
        device_info=None,
        module=None,
    ):
        self._hass = hass
        self._device = device
        self._module = module
        self._sensor_type = sensor_type
        self._configured_unique_id = unique_id
        self._configured_name = name
        self._attr_device_info = device_info or device_info_for_address(
            hass, device.device_address
        )
        self._device_update_cb = None
        self._attr_device_class = self._resolve_device_class(device_class)
        
        self._should_poll = False
        if scan_interval > 0:
            self._should_poll = True

        self.entity_id = generate_entity_id("binary_sensor.{}", object_id, None, hass)

    async def async_added_to_hass(self):
        """Attach this YAML entity to its physical Buspro device."""
        await super().async_added_to_hass()
        attach_entity_to_physical_device(
            self._hass, self, self._device.device_address
        )
        # Register the update callback only once added to hass.
        self.async_register_callbacks()

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
        await super().async_will_remove_from_hass()

    @staticmethod
    def _resolve_device_class(device_class):
        if not device_class:
            return None
        try:
            return BinarySensorDeviceClass(device_class)
        except ValueError:
            # Keep unknown values out of HA device_class enum.
            return None

    @property
    def should_poll(self):
        """No polling needed within Buspro."""
        return self._should_poll

    async def async_update(self):
        # Polling (when enabled by scan_interval) must refresh all binary sensor types.
        await self._device.read_sensor_status()

    @property
    def name(self):
        """Return the display name of this light."""
        return self._configured_name or self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        return bool(
            self._module.connected if self._module is not None
            else self._hass.data[DATA_BUSPRO].connected
        )

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return self._attr_device_class

    @property
    def unique_id(self):
        """Return the unique id."""
        if self._configured_unique_id:
            return self._configured_unique_id
        if self._sensor_type == CONF_MOTION:
            return self._device.device_identifier
        return f"{self._device.device_identifier}-{self._sensor_type}"

    @property
    def is_on(self):
        """Return true if the binary sensor is on."""
        if self._sensor_type == CONF_MOTION:
            # _LOGGER.info("----> {}".format(self._device.movement))
            return self._device.movement
        if self._sensor_type == CONF_DRY_CONTACT_1:
            # _LOGGER.info("----> {}".format(self._device.dry_contact_1_is_on))
            return self._device.dry_contact_1_is_on
        if self._sensor_type == CONF_DRY_CONTACT_2:
            return self._device.dry_contact_2_is_on
        if self._sensor_type == CONF_UNIVERSAL_SWITCH:
            return self._device.universal_switch_is_on
        if self._sensor_type == CONF_SINGLE_CHANNEL:
            return self._device.single_channel_is_on
        if self._sensor_type == CONF_DRY_CONTACT:
            return self._device.switch_status
        return None
