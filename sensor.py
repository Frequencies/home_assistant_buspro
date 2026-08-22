"""
This component provides sensor support for Buspro.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/...
"""

import logging
from datetime import timedelta

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import (
    PLATFORM_SCHEMA,
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import (
    CONF_NAME, 
    CONF_DEVICES, 
    CONF_ADDRESS, 
    CONF_TYPE, 
    CONF_UNIT_OF_MEASUREMENT,
    ILLUMINANCE, 
    TEMPERATURE, 
    CONF_DEVICE_CLASS, 
    CONF_SCAN_INTERVAL,
    EntityCategory,
    PERCENTAGE,
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
    DEVICE_TYPE_MULTISENSOR,
)
from .dimmer_entities import dimmer_diagnostic_definitions
from .entity_helpers import (
    attach_entity_to_physical_device,
    build_device_info,
    device_info_for_address,
    parse_device_address,
)
from .device_catalog import DEVICE_CATALOG
from .managed_devices import managed_device_info
from .logic_controller import (
    logic_controller_coordinator,
    logic_controller_definitions,
)

DEFAULT_CONF_UNIT_OF_MEASUREMENT = ""
DEFAULT_CONF_DEVICE_CLASS = None
DEFAULT_CONF_SCAN_INTERVAL = 0
DEFAULT_CONF_OFFSET = 0
DEFAULT_OBJECT_ID = ""

CONF_DEVICE = "device"
CONF_OFFSET = "offset"
CONF_OBJECT_ID = "object_id"
CONF_UNIQUE_ID = "unique_id"

SCAN_INTERVAL = timedelta(minutes=2)

_LOGGER = logging.getLogger(__name__)

SENSOR_TYPES = {
    ILLUMINANCE,
    TEMPERATURE,
    "humidity",
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_DEVICES):
        vol.All(cv.ensure_list, [
            vol.All({
                vol.Required(CONF_ADDRESS): cv.string,
                vol.Required(CONF_NAME): cv.string,
                vol.Required(CONF_TYPE): vol.In(SENSOR_TYPES),
                vol.Optional(CONF_UNIT_OF_MEASUREMENT, default=DEFAULT_CONF_UNIT_OF_MEASUREMENT): cv.string,
                vol.Optional(CONF_DEVICE_CLASS, default=DEFAULT_CONF_DEVICE_CLASS): vol.Any(None, cv.string),
                vol.Optional(CONF_DEVICE): cv.string,
                vol.Optional(CONF_SCAN_INTERVAL, default=DEFAULT_CONF_SCAN_INTERVAL): cv.positive_int,
                vol.Optional(CONF_OFFSET, default=DEFAULT_CONF_OFFSET): cv.string,
                vol.Optional(CONF_OBJECT_ID, default=DEFAULT_OBJECT_ID): cv.string,
                vol.Optional(CONF_UNIQUE_ID): cv.string,
            })
        ])
})


# noinspection PyUnusedLocal
async def async_setup_platform(hass, config, async_add_entites, discovery_info=None):
    """Set up Buspro switch devices."""
    module = hass.data[DATA_BUSPRO]

    if discovery_info is not None:
        async_add_entites(_compound_sensor_entities(hass, module))
        return

    devices = []

    for device_config in config[CONF_DEVICES]:
        address = device_config[CONF_ADDRESS]
        name = device_config[CONF_NAME]
        sensor_type = device_config[CONF_TYPE]
        device = device_config.get(CONF_DEVICE)
        offset = device_config[CONF_OFFSET]
        unit_of_measurement = device_config[CONF_UNIT_OF_MEASUREMENT]
        device_class = device_config[CONF_DEVICE_CLASS]
        
        scan_interval = device_config[CONF_SCAN_INTERVAL]
        interval = 0
        if scan_interval is not None:
            interval = int(scan_interval)
            
        address2 = address.split('.')
        device_address = (int(address2[0]), int(address2[1]))

        _LOGGER.debug("Adding sensor '{}' with address {}, sensor type '{}'".format(
            name, device_address, sensor_type))

        sensor = module.get_sensor(device_address, profile=device, name=name)
        object_id = device_config[CONF_OBJECT_ID]
        if object_id == DEFAULT_OBJECT_ID:
            object_id = name
        unique_id = device_config.get(CONF_UNIQUE_ID)

        devices.append(
            BusproSensor(
                hass,
                sensor,
                sensor_type,
                interval,
                offset,
                object_id,
                unique_id,
                unit_of_measurement,
                device_class,
                name=name,
            )
        )

    async_add_entites(devices)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up sensors generated from physical Buspro devices."""
    from .event import BusproPanelLastActionSensor, panel_definitions

    module = hass.data[DATA_BUSPRO_CONFIG]["entry_modules"][config_entry.entry_id]
    entities = _compound_sensor_entities(hass, module)
    entities.extend(_managed_sensor_entities(hass, module, config_entry))
    entities.extend(_dimmer_diagnostic_entities(hass, module, config_entry))
    entities.extend(_logic_controller_diagnostic_entities(hass, module, config_entry))
    for address, (_name, _button_count, device_info) in panel_definitions(
        hass, config_entry
    ).items():
        device_address = tuple(int(part) for part in address.split("."))
        entities.append(
            BusproPanelLastActionSensor(
                hass,
                module.hdl,
                device_address,
                address,
                device_info,
            )
        )
    async_add_entities(entities)


def _logic_controller_diagnostic_entities(hass, module, config_entry):
    """Create firmware and last-seen diagnostics for logic controllers."""
    entities = []
    for address, device_info in logic_controller_definitions(
        hass, config_entry
    ).items():
        coordinator = logic_controller_coordinator(module, address)
        entities.extend(
            (
                BusproLogicControllerDiagnosticSensor(
                    coordinator,
                    address,
                    "firmware",
                    "Firmware version",
                    device_info,
                ),
                BusproLogicControllerDiagnosticSensor(
                    coordinator,
                    address,
                    "last_seen",
                    "Last seen",
                    device_info,
                ),
            )
        )
    return entities


class BusproLogicControllerDiagnosticSensor(SensorEntity):
    """Read-only logic-controller diagnostic value."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(self, coordinator, address, sensor_type, name, device_info):
        self._coordinator = coordinator
        self._sensor_type = sensor_type
        self._device_update_cb = None
        self._attr_name = name
        self._attr_device_info = device_info
        self._attr_unique_id = f"buspro-{address}-logic-{sensor_type}"
        if sensor_type == "last_seen":
            self._attr_device_class = SensorDeviceClass.TIMESTAMP

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
        return self.native_value is not None

    @property
    def native_value(self):
        if self._sensor_type == "firmware":
            return self._coordinator.firmware_version
        return self._coordinator.last_seen

    @property
    def extra_state_attributes(self):
        if self._sensor_type != "firmware":
            return None
        return {"raw_payload": self._coordinator.firmware_payload}


def _dimmer_diagnostic_entities(hass, module, config_entry):
    """Create read-only configuration diagnostics for supported dimmers."""
    entities = []
    for address, (channel_count, device_info) in dimmer_diagnostic_definitions(
        hass, config_entry
    ).items():
        device_address = parse_device_address(address)
        diagnostics = module.get_dimmer_diagnostics(device_address, channel_count)
        entities.append(
            BusproDimmerDiagnosticSensor(
                hass,
                diagnostics,
                address,
                "minimum_brightness",
                "Minimum brightness",
                device_info,
            )
        )
        for channel in range(1, channel_count + 1):
            entities.append(
                BusproDimmerDiagnosticSensor(
                    hass,
                    diagnostics,
                    address,
                    "maximum_brightness",
                    f"Channel {channel} maximum brightness",
                    device_info,
                    channel,
                )
            )
            entities.append(
                BusproDimmerDiagnosticSensor(
                    hass,
                    diagnostics,
                    address,
                    "load_type",
                    f"Channel {channel} load type",
                    device_info,
                    channel,
                )
            )
    return entities


class BusproDimmerDiagnosticSensor(SensorEntity):
    """Read-only dimmer configuration value."""

    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_has_entity_name = True
    _attr_should_poll = False

    def __init__(
        self,
        hass,
        diagnostics,
        address,
        sensor_type,
        name,
        device_info,
        channel=None,
    ):
        self._hass = hass
        self._diagnostics = diagnostics
        self._sensor_type = sensor_type
        self._channel = channel
        self._device_update_cb = None
        self._attr_name = name
        self._attr_device_info = device_info
        suffix = sensor_type if channel is None else f"channel-{channel}-{sensor_type}"
        self._attr_unique_id = f"buspro-{address}-dimmer-{suffix}"
        if sensor_type != "load_type":
            self._attr_native_unit_of_measurement = PERCENTAGE

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
        return self.native_value is not None

    @property
    def native_value(self):
        if self._sensor_type == "minimum_brightness":
            return self._diagnostics.minimum_brightness
        if self._sensor_type == "maximum_brightness":
            return self._diagnostics.maximum_brightness(self._channel)
        load_type = self._diagnostics.load_type(self._channel)
        if load_type is None:
            return None
        return "not reported" if load_type == 255 else str(load_type)

    @property
    def extra_state_attributes(self):
        if self._sensor_type != "load_type":
            return None
        return {"raw_load_type": self._diagnostics.load_type(self._channel)}


def _compound_sensor_entities(hass, module):
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
            if sensor_type not in SENSOR_TYPES:
                continue

            devices.append(
                BusproSensor(
                    hass,
                    sensor,
                    sensor_type,
                    entity_config[CONF_SCAN_INTERVAL],
                    entity_config[CONF_OFFSET],
                    entity_config[CONF_OBJECT_ID],
                    entity_config.get(CONF_UNIQUE_ID),
                    entity_config.get(CONF_UNIT_OF_MEASUREMENT),
                    entity_config.get(CONF_DEVICE_CLASS),
                    name=entity_config[CONF_NAME],
                    device_info=device_info,
                )
            )
    return devices


def _managed_sensor_entities(hass, module, config_entry):
    """Create measurement entities for UI-managed multisensors."""
    entities = []
    for device_config in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        if device_config[CONF_DEVICE_TYPE] != DEVICE_TYPE_MULTISENSOR:
            continue
        spec = DEVICE_CATALOG[device_config["model"]]
        address = parse_device_address(device_config["address"])
        sensor = module.get_sensor(
            address,
            profile=spec["profile"],
            name=device_config["name"],
        )
        info = managed_device_info(device_config)
        for channel in device_config[CONF_CHANNELS]:
            sensor_type = channel[CONF_CHANNEL_NUMBER]
            if sensor_type not in SENSOR_TYPES:
                continue
            entities.append(
                BusproSensor(
                    hass,
                    sensor,
                    sensor_type,
                    0,
                    "0",
                    channel[CONF_OBJECT_ID],
                    channel[CONF_UNIQUE_ID],
                    name=channel[CONF_NAME],
                    device_info=info,
                )
            )
    return entities


# noinspection PyAbstractClass
class BusproSensor(SensorEntity):
    """Representation of a Buspro switch."""

    def __init__(
        self,
        hass,
        device,
        sensor_type,
        scan_interval,
        offset,
        object_id,
        unique_id=None,
        configured_unit_of_measurement=None,
        configured_device_class=None,
        name=None,
        device_info=None,
    ):
        self._hass = hass
        self._device = device
        self._sensor_type = sensor_type
        self._configured_unique_id = unique_id
        self._configured_unit_of_measurement = configured_unit_of_measurement
        self._configured_device_class = configured_device_class
        self._configured_name = name
        self._attr_device_info = device_info or device_info_for_address(
            hass, device.device_address
        )
        self._device_update_cb = None
        self._offset = offset
        self._temperature = None
        self._brightness = None
        self._humidity = None

        self._should_poll = False
        if scan_interval > 0:
            self._should_poll = True
        self.entity_id = generate_entity_id("sensor.{}", object_id, None, hass)

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
            if self._hass is not None:
                self._temperature = self._device.temperature
                self._brightness = self._device.brightness
                self._humidity = self._device.humidity
                self.async_write_ha_state()

        self._device_update_cb = after_update_callback
        self._device.register_device_updated_cb(after_update_callback)

    async def async_will_remove_from_hass(self):
        if self._device_update_cb is not None:
            self._device.unregister_device_updated_cb(self._device_update_cb)
            self._device_update_cb = None
        await super().async_will_remove_from_hass()

    @property
    def should_poll(self):
        """No polling needed within Buspro unless explicitly set."""
        return self._should_poll or self.native_value is None

    async def async_update(self):
        await self._device.read_sensor_status()

    @property
    def name(self):
        """Return the display name of this light."""
        return self._configured_name or self._device.name

    @property
    def available(self):
        """Return True if entity is available."""
        connected = self._hass.data[DATA_BUSPRO].connected

        if self._sensor_type == TEMPERATURE:
            return connected and self._current_temperature is not None

        if self._sensor_type == ILLUMINANCE:
            return connected and self._brightness is not None
        
        if self._sensor_type == "humidity":
            return connected and self._humidity is not None

    @property
    def state(self):
        """Return the state of the sensor."""
        return self.native_value

    @property
    def native_value(self):
        """Return the native value of the sensor."""
        if self._sensor_type == TEMPERATURE:
            return self._current_temperature

        if self._sensor_type == ILLUMINANCE:
            return self._brightness
        
        if self._sensor_type == "humidity":
            return self._humidity

    @property
    def _current_temperature(self):
        if self._temperature is None:
            return None

        temperature = self._temperature
        if self._offset is not None and temperature != 0:
            temperature = temperature + int(self._offset)

        return temperature

    @property
    def device_class(self):
        """Return the class of this sensor."""
        if self._configured_device_class:
            return self._configured_device_class
        if self._sensor_type == TEMPERATURE:
            return "temperature"
        if self._sensor_type == ILLUMINANCE:
            return "illuminance"
        if self._sensor_type == "humidity":
            return "humidity"
        return None

    @property
    def unit_of_measurement(self):
        """Return the configured unit for backward compatibility."""
        return self.native_unit_of_measurement

    @property
    def native_unit_of_measurement(self):
        """Return the unit this state is expressed in."""
        if self._configured_unit_of_measurement:
            return self._configured_unit_of_measurement
        if self._sensor_type == TEMPERATURE:
            return "°C"
        if self._sensor_type == ILLUMINANCE:
            return "lux"
        if self._sensor_type == "humidity":
            return "%"
        return ""

    @property
    def state_class(self):
        """All Buspro sensor readings are point-in-time measurements."""
        if self._sensor_type in (TEMPERATURE, ILLUMINANCE, "humidity"):
            return SensorStateClass.MEASUREMENT
        return None

    @property
    def extra_state_attributes(self):
        """Return the state attributes."""
        attributes = {}
        if self._humidity is not None:
            attributes['humidity'] = self._humidity
        if self._device.movement is not None:
            attributes['movement'] = self._device.movement
        if self._device._sonic is not None:
            attributes['sonic'] = self._device._sonic
        if self._device._dry_contact_1_status is not None:
            attributes['dry_contact_1'] = self._device.dry_contact_1_is_on
        if self._device._dry_contact_2_status is not None:
            attributes['dry_contact_2'] = self._device.dry_contact_2_is_on
        return attributes

    @property
    def unique_id(self):
        """Return the unique id."""
        return self._configured_unique_id or f"{self._device.device_identifier}-{self._sensor_type}"
