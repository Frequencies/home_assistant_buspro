"""
Support for Buspro devices.

For more details about this component, please refer to the documentation at
https://home-assistant.io/...
"""

import logging

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.const import (
    CONF_HOST, 
    CONF_PORT, 
    CONF_NAME,
)
from .const import (
    CONF_SEND_PORT,
    CONF_RECEIVE_PORT,
)
from homeassistant.const import (
    EVENT_HOMEASSISTANT_STOP,
)
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

_LOGGER = logging.getLogger(__name__)

DOMAIN = "buspro"
DATA_BUSPRO = "buspro"
DEPENDENCIES = []

DEFAULT_CONF_NAME = ""

DEFAULT_SCENE_NAME = "BUSPRO SCENE"
DEFAULT_SEND_MESSAGE_NAME = "BUSPRO MESSAGE"

SERVICE_BUSPRO_SEND_MESSAGE = "send_message"
SERVICE_BUSPRO_ACTIVATE_SCENE = "activate_scene"
SERVICE_BUSPRO_UNIVERSAL_SWITCH = "set_universal_switch"

SERVICE_BUSPRO_ATTR_OPERATE_CODE = "operate_code"
SERVICE_BUSPRO_ATTR_ADDRESS = "address"
SERVICE_BUSPRO_ATTR_PAYLOAD = "payload"
SERVICE_BUSPRO_ATTR_SCENE_ADDRESS = "scene_address"
SERVICE_BUSPRO_ATTR_SWITCH_NUMBER = "switch_number"
SERVICE_BUSPRO_ATTR_STATUS = "status"

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

CONFIG_SCHEMA = vol.Schema({
    DOMAIN: vol.Schema({
        vol.Required(CONF_HOST): cv.string,
        vol.Required(CONF_PORT): cv.port,
        vol.Optional(CONF_NAME, default=DEFAULT_CONF_NAME): cv.string,
        vol.Optional(CONF_SEND_PORT): cv.port,
        vol.Optional(CONF_RECEIVE_PORT): cv.port,
    })
}, extra=vol.ALLOW_EXTRA)


def _entry_modules(hass: HomeAssistant) -> dict:
    data = hass.data.setdefault(DOMAIN, {})
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
    return hass.data.get(DOMAIN, {}).get("yaml_module")


def _has_any_module(hass: HomeAssistant) -> bool:
    if _entry_modules(hass):
        return True
    return hass.data.get(DOMAIN, {}).get("yaml_module") is not None


async def async_setup(hass: HomeAssistant, config: dict):
    """Setup the Buspro component. """
    if DOMAIN not in config:
        return True

    host = config[DOMAIN][CONF_HOST]
    port = config[DOMAIN][CONF_PORT]
    send_port = config[DOMAIN].get(CONF_SEND_PORT, port)
    receive_port = config[DOMAIN].get(CONF_RECEIVE_PORT, port)

    module = BusproModule(hass, host, port, send_port, receive_port)
    hass.data.setdefault(DOMAIN, {})["yaml_module"] = module
    _set_active_module(hass, module)
    await module.start()
    module.register_services(force=True)

    return True

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Setup the Buspro component. """
    host = config_entry.data.get(CONF_HOST, "")
    port = config_entry.data.get(CONF_PORT, 1)
    send_port = config_entry.data.get(CONF_SEND_PORT, port)
    receive_port = config_entry.data.get(CONF_RECEIVE_PORT, port)

    module = BusproModule(hass, host, port, send_port, receive_port)
    _entry_modules(hass)[config_entry.entry_id] = module
    _set_active_module(hass, module)
    await module.start()
    module.register_services(force=True)

    return True

async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
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

class BusproModule:
    """Representation of Buspro Object."""

    def __init__(self, hass, host, port, send_port=None, receive_port=None):
        """Initialize of Buspro module."""
        self.hass = hass
        self.connected = False
        self.hdl = None
        if send_port is None:
            send_port = port
        if receive_port is None:
            receive_port = port
        self.gateway_address_send_receive = ((host, send_port), ('', receive_port))
        self._stop_listener = None
        self.init_hdl()

    def init_hdl(self):
        """Initialize of Buspro object."""
        # noinspection PyUnresolvedReferences
        from .pybuspro.buspro import Buspro
        self.hdl = Buspro(self.gateway_address_send_receive, self.hass.loop)
        # self.hdl.register_telegram_received_all_messages_cb(self.telegram_received_cb)

    async def start(self):
        """Start Buspro object. Connect to tunneling device."""
        await self.hdl.start(state_updater=False)
        self._stop_listener = self.hass.bus.async_listen_once(EVENT_HOMEASSISTANT_STOP, self.stop)
        self.connected = True

    # noinspection PyUnusedLocal
    async def stop(self, event):
        """Stop Buspro object. Disconnect from tunneling device."""
        if self._stop_listener is not None:
            self._stop_listener()
            self._stop_listener = None
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

        status = call.data.get(SERVICE_BUSPRO_ATTR_STATUS)
        if status == 1:
            await universal_switch.set_on()
        else:
            await universal_switch.set_off()

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
