"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.helpers import device_registry as dr
from homeassistant.const import (
    CONF_ADDRESS,
    CONF_DEVICE_CLASS,
    CONF_DEVICES,
    CONF_HOST,
    CONF_NAME,
    CONF_PORT,
    CONF_SCAN_INTERVAL,
    CONF_TYPE,
    CONF_UNIT_OF_MEASUREMENT,
    Platform,
)
from .const import (
    COMPOUND_SENSOR_TYPES,
    CONF_ENTITIES,
    CONF_CLIENT_ADDRESS,
    CONF_MANUFACTURER,
    CONF_MODEL,
    CONF_MANAGED_DEVICES,
    CONF_OBJECT_ID,
    CONF_OFFSET,
    CONF_PROFILE,
    CONF_SEND_PORT,
    CONF_RECEIVE_PORT,
    CONF_UNIQUE_ID,
    CONF_CHANNELS,
    CONF_DEVICE_TYPE,
    CONF_CHANNEL_NUMBER,
    CONF_CHANNEL_ENABLED,
    DATA_BUSPRO_CONFIG,
    DEFAULT_MANUFACTURER,
    DEFAULT_CLIENT_ADDRESS,
    DEFAULT_SENSOR_MODEL,
    DEFAULT_SENSOR_PROFILE,
)
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from .network_helpers import local_ip_for_gateway
from .device_catalog import MODEL_NOTES
from .devices import DEVICE_CATALOG
from .entity_helpers import registry_device_definitions
from .model_notes import emit_model_support_notes
from .yaml_normalization import normalize_yaml_devices
from .dual_mode_yaml import normalize_dual_mode, is_device_centric

_LOGGER = logging.getLogger(__name__)

DOMAIN = "buspro"
DATA_BUSPRO = "buspro"
DEPENDENCIES = []

DEFAULT_CONF_NAME = ""

DEFAULT_SCENE_NAME = "BUSPRO SCENE"
DEFAULT_SEND_MESSAGE_NAME = "BUSPRO MESSAGE"

PLATFORMS = [Platform.SENSOR, Platform.BINARY_SENSOR]
ENTRY_PLATFORMS = [
    Platform.SWITCH,
    Platform.LIGHT,
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.COVER,
    Platform.EVENT,
    Platform.FAN,
]

SERVICE_BUSPRO_SEND_MESSAGE = "send_message"
SERVICE_BUSPRO_ACTIVATE_SCENE = "activate_scene"
SERVICE_BUSPRO_UNIVERSAL_SWITCH = "set_universal_switch"

SERVICE_BUSPRO_ATTR_OPERATE_CODE = "operate_code"
SERVICE_BUSPRO_ATTR_ADDRESS = "address"
SERVICE_BUSPRO_ATTR_PAYLOAD = "payload"
SERVICE_BUSPRO_ATTR_SCENE_ADDRESS = "scene_address"
SERVICE_BUSPRO_ATTR_SWITCH_NUMBER = "switch_number"
SERVICE_BUSPRO_ATTR_STATUS = "status"


def _parse_client_address(value):
    """Parse a Buspro subnet.device client identity."""
    parts = str(value).split(".")
    if len(parts) != 2:
        raise ValueError("Buspro client address must use subnet.device format")
    address = tuple(int(part) for part in parts)
    if any(part < 0 or part > 255 for part in address):
        raise ValueError("Buspro client address values must be between 0 and 255")
    return address


def _validate_client_address(value):
    """Validate while preserving the serializable subnet.device string."""
    _parse_client_address(value)
    return str(value)


"""{ "address": [1,74], "scene_address": [3,5] }"""
SERVICE_BUSPRO_ACTIVATE_SCENE_SCHEMA = vol.Schema({
    vol.Required(SERVICE_BUSPRO_ATTR_ADDRESS): vol.Any([cv.positive_int]),
    vol.Required(SERVICE_BUSPRO_ATTR_SCENE_ADDRESS): vol.Any([cv.positive_int]),
})

"""{ "address": [1,74], "operate_code": [4,12], "payload": [1,75,0,3] }"""
SERVICE_BUSPRO_SEND_MESSAGE_SCHEMA = vol.Schema({
    vol.Required(SERVICE_BUSPRO_ATTR_ADDRESS): vol.Any([cv.positive_int]),
    vol.Required(SERVICE_BUSPRO_ATTR_OPERATE_CODE): vol.Any([cv.positive_int]),
    vol.Required(SERVICE_BUSPRO_ATTR_PAYLOAD): vol.Any([cv.positive_int]),
})

"""{ "address": [1,100], "switch_number": 100, "status": 1 }"""
SERVICE_BUSPRO_UNIVERSAL_SWITCH_SCHEMA = vol.Schema({
    vol.Required(SERVICE_BUSPRO_ATTR_ADDRESS): vol.Any([cv.positive_int]),
    vol.Required(SERVICE_BUSPRO_ATTR_SWITCH_NUMBER): vol.Any(cv.positive_int),
    vol.Required(SERVICE_BUSPRO_ATTR_STATUS): vol.Any(cv.positive_int),
})

COMPOUND_ENTITY_SCHEMA = vol.Schema({
    vol.Required(CONF_TYPE): vol.In(COMPOUND_SENSOR_TYPES),
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_OBJECT_ID): cv.string,
    vol.Optional(CONF_UNIQUE_ID): cv.string,
    vol.Optional(CONF_DEVICE_CLASS): vol.Any(None, cv.string),
    vol.Optional(CONF_UNIT_OF_MEASUREMENT): cv.string,
    vol.Optional(CONF_SCAN_INTERVAL, default=0): cv.positive_int,
    vol.Optional(CONF_OFFSET, default="0"): cv.string,
})

COMPOUND_DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ADDRESS): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_MODEL, default=DEFAULT_SENSOR_MODEL): cv.string,
    vol.Optional(CONF_MANUFACTURER, default=DEFAULT_MANUFACTURER): cv.string,
    vol.Optional(CONF_PROFILE, default=DEFAULT_SENSOR_PROFILE): cv.string,
    vol.Required(CONF_ENTITIES): vol.All(cv.ensure_list, [COMPOUND_ENTITY_SCHEMA]),
})

# Device-centric format: single file per device with all its channels
CHANNEL_SCHEMA = vol.Schema({
    vol.Required(CONF_CHANNEL_NUMBER): vol.Any(cv.positive_int, cv.string),
    vol.Required(CONF_NAME): cv.string,
    vol.Optional(CONF_CHANNEL_ENABLED, default=True): cv.boolean,
    vol.Optional(CONF_OBJECT_ID): cv.string,
    vol.Optional(CONF_UNIQUE_ID): cv.string,
})

MANAGED_YAML_DEVICE_SCHEMA = vol.Schema({
    vol.Required(CONF_ADDRESS): cv.string,
    vol.Required(CONF_NAME): cv.string,
    vol.Required(CONF_MODEL): cv.string,
    vol.Required(CONF_DEVICE_TYPE): cv.string,
    vol.Optional(CONF_CHANNELS): vol.All(cv.ensure_list, [CHANNEL_SCHEMA]),
})


CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Optional(CONF_HOST): cv.string,
        vol.Optional(CONF_PORT): cv.port,
        vol.Optional(CONF_NAME, default=DEFAULT_CONF_NAME): cv.string,
        vol.Optional(CONF_SEND_PORT): cv.port,
        vol.Optional(CONF_RECEIVE_PORT): cv.port,
        vol.Optional(
            CONF_CLIENT_ADDRESS, default=DEFAULT_CLIENT_ADDRESS
        ): vol.All(cv.string, _validate_client_address),
        vol.Optional(CONF_DEVICES, default=[]): vol.All(cv.ensure_list, [
            vol.Any(COMPOUND_DEVICE_SCHEMA, MANAGED_YAML_DEVICE_SCHEMA)
        ]),
    })
}, extra=vol.ALLOW_EXTRA)


def _entry_modules(hass: HomeAssistant) -> dict:
    data = hass.data.setdefault(DATA_BUSPRO_CONFIG, {})
    return data.setdefault("entry_modules", {})


def _set_active_module(hass: HomeAssistant, module):
    if module is not None:
        hass.data[DATA_BUSPRO] = module
    elif DATA_BUSPRO in hass.data:
        del hass.data[DATA_BUSPRO]


def _get_any_module(hass: HomeAssistant):
    modules = _entry_modules(hass)
    if modules:
        return next(iter(modules.values()))
    return hass.data.get(DATA_BUSPRO_CONFIG, {}).get("yaml_module")


def _has_any_module(hass: HomeAssistant) -> bool:
    if _entry_modules(hass):
        return True
    return hass.data.get(DATA_BUSPRO_CONFIG, {}).get("yaml_module") is not None


async def async_setup(hass: HomeAssistant, config: dict):
    """Setup the Buspro component. """
    if DOMAIN not in config:
        return True

    domain_config = config[DOMAIN]
    runtime_data = hass.data.setdefault(DATA_BUSPRO_CONFIG, {})

    # Normalize both entity-centric and device-centric YAML formats
    raw_devices = domain_config.get(CONF_DEVICES, [])
    normalized_devices = normalize_dual_mode(
        raw_devices,
        DEVICE_CATALOG,
        _LOGGER,
    )

    runtime_data["configured_devices"] = normalized_devices
    runtime_data["device_config_source"] = "yaml"
    runtime_data["has_device_centric"] = any(
        is_device_centric(d) for d in normalized_devices
    )

    # A config entry may own the gateway while YAML only describes devices.
    if CONF_HOST not in domain_config or CONF_PORT not in domain_config:
        return True

    host = domain_config[CONF_HOST]
    port = domain_config[CONF_PORT]
    send_port = domain_config.get(CONF_SEND_PORT, port)
    receive_port = domain_config.get(CONF_RECEIVE_PORT, port)
    client_address = _parse_client_address(
        domain_config.get(CONF_CLIENT_ADDRESS, DEFAULT_CLIENT_ADDRESS)
    )

    module = BusproModule(
        hass, host, port, send_port, receive_port, client_address
    )
    runtime_data["yaml_module"] = module
    _set_active_module(hass, module)
    await module.start()
    module.register_services(force=True)

    if domain_config.get(CONF_DEVICES):
        from homeassistant.helpers import discovery

        for platform in PLATFORMS:
            hass.async_create_task(
                discovery.async_load_platform(hass, platform, DOMAIN, {}, config)
            )

    return True


async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Setup the Buspro component. """
    if (
        CONF_CLIENT_ADDRESS not in config_entry.data
        and CONF_CLIENT_ADDRESS not in config_entry.options
    ):
        migrated_data = dict(config_entry.data)
        migrated_data[CONF_CLIENT_ADDRESS] = DEFAULT_CLIENT_ADDRESS
        hass.config_entries.async_update_entry(config_entry, data=migrated_data)

    cfg = {**config_entry.data, **config_entry.options}
    if CONF_HOST not in cfg or CONF_PORT not in cfg:
        _LOGGER.error("Buspro config entry is missing host or port")
        return False
    host = cfg[CONF_HOST]
    port = cfg[CONF_PORT]
    send_port = cfg.get(CONF_SEND_PORT, port)
    receive_port = cfg.get(CONF_RECEIVE_PORT, port)
    client_address = _parse_client_address(
        cfg.get(CONF_CLIENT_ADDRESS, DEFAULT_CLIENT_ADDRESS)
    )

    module = BusproModule(
        hass, host, port, send_port, receive_port, client_address
    )
    _entry_modules(hass)[config_entry.entry_id] = module
    _set_active_module(hass, module)
    await module.start()
    module.register_services(force=True)

    _set_device_addresses(hass, config_entry)
    _log_model_support_notes(hass, config_entry)

    await hass.config_entries.async_forward_entry_setups(
        config_entry, ENTRY_PLATFORMS
    )
    config_entry.async_on_unload(
        config_entry.add_update_listener(_async_reload_entry)
    )

    return True


def _log_model_support_notes(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Log configured models with explicit support-level notes."""
    model_addresses: dict[str, set[str]] = {}

    for device in registry_device_definitions(hass, config_entry):
        model = device.get("model")
        address = device.get("address")
        if not model:
            continue
        model_addresses.setdefault(model, set())
        if address:
            model_addresses[model].add(address)

    for device in config_entry.options.get(CONF_MANAGED_DEVICES, []):
        model = device.get(CONF_MODEL)
        address = device.get(CONF_ADDRESS)
        if not model:
            continue
        model_addresses.setdefault(model, set())
        if address:
            model_addresses[model].add(address)

    emit_model_support_notes(_LOGGER, model_addresses, MODEL_NOTES)


def _set_device_addresses(hass: HomeAssistant, config_entry: ConfigEntry) -> None:
    """Expose each Buspro physical address in Device Registry metadata."""
    registry = dr.async_get(hass)
    for device in registry.devices.values():
        if config_entry.entry_id not in device.config_entries:
            continue
        address = next(
            (
                identifier[1]
                for identifier in device.identifiers
                if len(identifier) >= 2 and identifier[0] == DOMAIN
            ),
            None,
        )
        if address is not None and device.serial_number != address:
            registry.async_get_or_create(
                config_entry_id=config_entry.entry_id,
                identifiers=device.identifiers,
                connections=device.connections,
                serial_number=address,
            )

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    unload_ok = await hass.config_entries.async_unload_platforms(
        config_entry, ENTRY_PLATFORMS
    )
    if not unload_ok:
        return False

    module = _entry_modules(hass).pop(config_entry.entry_id, None)
    if module is not None:
        await module.stop(None)

    next_module = _get_any_module(hass)
    _set_active_module(hass, next_module)

    if not _has_any_module(hass):
        BusproModule.unregister_services(hass)
    elif next_module is not None:
        next_module.register_services(force=True)

    return True


async def _async_reload_entry(hass: HomeAssistant, config_entry: ConfigEntry):
    """Reload Buspro after options change."""
    await hass.config_entries.async_reload(config_entry.entry_id)

class BusproModule:
    """Representation of Buspro Object."""

    def __init__(
        self,
        hass,
        host,
        port,
        send_port=None,
        receive_port=None,
        client_address=None,
    ):
        """Initialize of Buspro module."""
        self.hass = hass
        self.connected = False
        self.hdl = None
        if send_port is None:
            send_port = port
        if receive_port is None:
            receive_port = port
        self.gateway_address_send_receive = ((host, send_port), ('', receive_port))
        self._gateway_host = host
        self._gateway_port = send_port
        if client_address is None:
            raise ValueError("Buspro client_address is required")
        self._client_address = tuple(client_address)
        self._stop_listener = None
        self._sensor_devices = {}
        self._dimmer_diagnostics = {}
        self._logic_controllers = {}
        self._diagnostics = None  # Initialize diagnostics
        self.init_hdl()

    def get_sensor(
        self,
        device_address,
        *,
        profile=None,
        universal_switch_number=None,
        channel_number=None,
        switch_number=None,
        name="",
    ):
        """Return one shared protocol object for a physical sensor endpoint."""
        from .pybuspro.devices import Sensor

        protocol_profile = None if profile in (None, "12in1", "sensor_status") else profile
        key = (
            tuple(device_address),
            protocol_profile,
            universal_switch_number,
            channel_number,
            switch_number,
        )
        if key not in self._sensor_devices:
            self._sensor_devices[key] = Sensor(
                self.hdl,
                tuple(device_address),
                universal_switch_number=universal_switch_number,
                channel_number=channel_number,
                device=protocol_profile,
                switch_number=switch_number,
                name=name,
            )
        return self._sensor_devices[key]

    def get_dimmer_diagnostics(self, device_address, channel_count=6):
        """Return shared diagnostics for a physical dimmer."""
        from .pybuspro.devices import DimmerDiagnostics

        key = tuple(device_address)
        if key not in self._dimmer_diagnostics:
            self._dimmer_diagnostics[key] = DimmerDiagnostics(
                self.hdl,
                key,
                channel_count,
            )
        return self._dimmer_diagnostics[key]

    def get_logic_controller(self, device_address):
        """Return shared diagnostics for a physical logic controller."""
        from .pybuspro.devices import LogicControllerDiagnostics

        key = tuple(device_address)
        if key not in self._logic_controllers:
            self._logic_controllers[key] = LogicControllerDiagnostics(
                self.hdl, key
            )
        return self._logic_controllers[key]

    def init_hdl(self):
        """Initialize of Buspro object with diagnostics."""
        # noinspection PyUnresolvedReferences
        from .pybuspro.buspro import Buspro
        from .pybuspro.diagnostics import (
            DiagnosticCapture,
            RelayDecoder,
            DimmerDecoder,
            ClimateDecoder,
            SensorDecoder,
            CoverDecoder,
            LogicControllerDecoder,
        )

        self.hdl = Buspro(
            self.gateway_address_send_receive,
            self.hass.loop,
            client_address=self._client_address,
        )

        # Initialize diagnostic system
        self._diagnostics = DiagnosticCapture(
            max_records=5000,
            address_aliases={},
        )

        # Register all decoders
        self._diagnostics.register_decoder("relay", RelayDecoder())
        self._diagnostics.register_decoder("dimmer", DimmerDecoder())
        self._diagnostics.register_decoder("climate", ClimateDecoder())
        self._diagnostics.register_decoder("sensor", SensorDecoder())
        self._diagnostics.register_decoder("cover", CoverDecoder())
        self._diagnostics.register_decoder("logic_controller", LogicControllerDecoder())

        # Attach to buspro instance
        self.hdl.set_diagnostics(self._diagnostics)
        # self.hdl.register_telegram_received_all_messages_cb(self.telegram_received_cb)

    def get_diagnostics(self):
        """Return diagnostic capture instance."""
        return self._diagnostics

    async def start(self):
        """Start Buspro object. Connect to tunneling device."""
        self.hdl.advertised_ip = await self.hass.async_add_executor_job(
            local_ip_for_gateway, self._gateway_host, self._gateway_port
        )
        await self.hdl.start(state_updater=False)
        self._stop_listener = self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)
        self.connected = True

    # noinspection PyUnusedLocal
    async def stop(self, event):
        """Stop Buspro object. Disconnect from tunneling device."""
        if self._stop_listener is not None:
            self._stop_listener()
            self._stop_listener = None
        # A single failing close() must not leave the remaining devices attached
        # or, worse, skip the gateway shutdown and leak the UDP socket.
        try:
            for collection in (
                self._sensor_devices,
                self._dimmer_diagnostics,
                self._logic_controllers,
            ):
                for device in collection.values():
                    try:
                        device.close()
                    except Exception:
                        _LOGGER.exception("Error closing Buspro device on stop")
                collection.clear()
        finally:
            await self.hdl.stop()
            self.connected = False

    async def service_activate_scene(self, call):
        """Service for activatign a __scene"""
        # noinspection PyUnresolvedReferences
        from .pybuspro.devices.scene import Scene

        attr_address = call.data.get(SERVICE_BUSPRO_ATTR_ADDRESS)
        attr_scene_address = call.data.get(SERVICE_BUSPRO_ATTR_SCENE_ADDRESS)
        scene = Scene(self.hdl, attr_address, attr_scene_address, DEFAULT_SCENE_NAME)
        await scene.run()

    async def service_send_message(self, call):
        """Service for send an arbitrary message"""
        # noinspection PyUnresolvedReferences
        from .pybuspro.devices.generic import Generic

        attr_address = call.data.get(SERVICE_BUSPRO_ATTR_ADDRESS)
        attr_payload = call.data.get(SERVICE_BUSPRO_ATTR_PAYLOAD)
        attr_operate_code = call.data.get(SERVICE_BUSPRO_ATTR_OPERATE_CODE)
        generic = Generic(self.hdl, attr_address, attr_payload, attr_operate_code, DEFAULT_SEND_MESSAGE_NAME)
        await generic.run()

    async def service_set_universal_switch(self, call):
        # noinspection PyUnresolvedReferences
        from .pybuspro.devices.universal_switch import UniversalSwitch

        attr_address = call.data.get(SERVICE_BUSPRO_ATTR_ADDRESS)
        attr_switch_number = call.data.get(SERVICE_BUSPRO_ATTR_SWITCH_NUMBER)
        universal_switch = UniversalSwitch(self.hdl, attr_address, attr_switch_number)

        try:
            status = call.data.get(SERVICE_BUSPRO_ATTR_STATUS)
            if status == 1:
                await universal_switch.set_on()
            else:
                await universal_switch.set_off()
        finally:
            # This is a throwaway device; detach its bus callback so each
            # service call does not leak a registered listener.
            universal_switch.close()

    def register_services(self, force=False):
        if force:
            self.unregister_services(self.hass)
        elif self.hass.services.has_service(DOMAIN, SERVICE_BUSPRO_ACTIVATE_SCENE):
            return

        """ activate_scene """
        self.hass.services.async_register(
            DOMAIN, SERVICE_BUSPRO_ACTIVATE_SCENE,
            self.service_activate_scene,
            schema=SERVICE_BUSPRO_ACTIVATE_SCENE_SCHEMA)

        """ send_message """
        self.hass.services.async_register(
            DOMAIN, SERVICE_BUSPRO_SEND_MESSAGE,
            self.service_send_message,
            schema=SERVICE_BUSPRO_SEND_MESSAGE_SCHEMA)

        """ universal_switch """
        self.hass.services.async_register(
            DOMAIN, SERVICE_BUSPRO_UNIVERSAL_SWITCH,
            self.service_set_universal_switch,
            schema=SERVICE_BUSPRO_UNIVERSAL_SWITCH_SCHEMA)

    @staticmethod
    def unregister_services(hass: HomeAssistant):
        for service in (
            SERVICE_BUSPRO_ACTIVATE_SCENE,
            SERVICE_BUSPRO_SEND_MESSAGE,
            SERVICE_BUSPRO_UNIVERSAL_SWITCH,
        ):
            if hass.services.has_service(DOMAIN, service):
                hass.services.async_remove(DOMAIN, service)

    '''
    def telegram_received_cb(self, telegram):
        #     """Call invoked after a KNX telegram was received."""
        #     self.hass.bus.fire('knx_event', {
        #         'address': str(telegram.group_address),
        #         'data': telegram.payload.value
        #     })
        # _LOGGER.info(f"Callback: '{telegram}'")
        return False
    '''
