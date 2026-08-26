import sys
import types


def ensure_homeassistant_stubs():
    if 'homeassistant' in sys.modules:
        return

    ha = types.ModuleType('homeassistant')
    ha_helpers = types.ModuleType('homeassistant.helpers')
    ha_cv = types.ModuleType('homeassistant.helpers.config_validation')
    ha_cv.string = lambda v: v
    ha_cv.port = lambda v: v
    ha_cv.positive_int = int
    ha_cv.positive_float = float
    ha_cv.boolean = bool
    ha_cv.ensure_list = lambda v: v if isinstance(v, list) else [v]

    ha_const = types.ModuleType('homeassistant.const')
    ha_const.CONF_HOST = 'host'
    ha_const.CONF_PORT = 'port'
    ha_const.CONF_NAME = 'name'
    ha_const.CONF_ADDRESS = 'address'
    ha_const.CONF_DEVICE_CLASS = 'device_class'
    ha_const.CONF_DEVICES = 'devices'
    ha_const.CONF_MODEL = 'model'
    ha_const.CONF_SCAN_INTERVAL = 'scan_interval'
    ha_const.CONF_TYPE = 'type'
    ha_const.CONF_UNIT_OF_MEASUREMENT = 'unit_of_measurement'
    ha_const.EVENT_HOMEASSISTANT_STOP = 'homeassistant_stop'

    class _Platform:  # pragma: no cover - stub
        LIGHT = 'light'
        SWITCH = 'switch'
        SENSOR = 'sensor'
        BINARY_SENSOR = 'binary_sensor'
        COVER = 'cover'
        CLIMATE = 'climate'
        FAN = 'fan'
        EVENT = 'event'
    ha_const.Platform = _Platform

    ha_core = types.ModuleType('homeassistant.core')
    ha_core.callback = lambda func: func
    class HomeAssistant:  # pragma: no cover - stub
        pass
    ha_core.HomeAssistant = HomeAssistant

    ha_config_entries = types.ModuleType('homeassistant.config_entries')
    ha_config_entries.CONN_CLASS_LOCAL_POLL = 'local_polling'

    class ConfigFlow:  # pragma: no cover - stub
        def __init__(self):
            self.hass = None
            self.context = {}

        async def async_set_unique_id(self, unique_id):
            self._unique_id = unique_id

        def _abort_if_unique_id_configured(self):
            existing = getattr(self.hass, 'existing_unique_ids', set())
            if getattr(self, '_unique_id', None) in existing:
                raise RuntimeError('already_configured')

        def async_create_entry(self, title, data):
            return {'type': 'create_entry', 'title': title, 'data': data}

        def async_show_form(self, step_id, data_schema=None, errors=None):
            return {'type': 'form', 'step_id': step_id, 'data_schema': data_schema, 'errors': errors or {}}

        def async_abort(self, reason):
            return {'type': 'abort', 'reason': reason}

        def __init_subclass__(cls, **kwargs):
            return super().__init_subclass__()

    class OptionsFlow:  # pragma: no cover - stub
        def __init__(self, config_entry=None):
            self.hass = None
            self.config_entry = config_entry

        def async_create_entry(self, title, data):
            return {'type': 'create_entry', 'title': title, 'data': data}

        def async_show_form(self, step_id, data_schema=None, errors=None):
            return {'type': 'form', 'step_id': step_id, 'data_schema': data_schema, 'errors': errors or {}}

        def async_show_menu(self, step_id, menu_options=None):
            return {'type': 'menu', 'step_id': step_id, 'menu_options': menu_options or []}

    ha_config_entries.ConfigFlow = ConfigFlow
    ha_config_entries.OptionsFlow = OptionsFlow

    class ConfigEntry:  # pragma: no cover - stub
        pass
    ha_config_entries.ConfigEntry = ConfigEntry

    class ConfigEntryState:  # pragma: no cover - stub
        LOADED = 'loaded'
        NOT_LOADED = 'not_loaded'
    ha_config_entries.ConfigEntryState = ConfigEntryState

    class ConfigEntryNotReady(Exception):  # pragma: no cover - stub
        pass
    ha_config_entries.ConfigEntryNotReady = ConfigEntryNotReady

    vol = types.ModuleType('voluptuous')
    vol.ALLOW_EXTRA = object()
    vol.Required = lambda key, default=None: key
    vol.Optional = lambda key, default=None: key
    vol.Any = lambda *args, **kwargs: args[0] if args else None
    vol.All = lambda *args, **kwargs: args[0] if args else None
    vol.In = lambda values: values
    vol.Length = lambda *args, **kwargs: None
    vol.Coerce = lambda t: t
    vol.Range = lambda *args, **kwargs: None
    vol.Match = lambda pattern: pattern
    vol.Schema = lambda *args, **kwargs: dict

    ha_dr = types.ModuleType('homeassistant.helpers.device_registry')
    class _FakeRegistry:  # pragma: no cover - stub
        def __init__(self):
            self.devices = {}
        def async_get_or_create(self, **kwargs):
            return None
    ha_dr.async_get = lambda hass: _FakeRegistry()
    class DeviceInfo(dict):  # pragma: no cover - stub
        pass
    ha_dr.DeviceInfo = DeviceInfo
    ha_er = types.ModuleType('homeassistant.helpers.entity_registry')
    class _FakeEntityRegistry:  # pragma: no cover - stub
        def __init__(self):
            self.entities = {}
    ha_er.async_get = lambda hass: _FakeEntityRegistry()
    ha_selector = types.ModuleType('homeassistant.helpers.selector')
    ha_selector.selector = lambda cfg: cfg
    ha_selector.TextSelector = lambda cfg=None: None
    ha_selector.TextSelectorConfig = lambda **kw: kw
    ha_selector.SelectSelector = lambda cfg=None: None
    ha_selector.SelectSelectorConfig = lambda **kw: kw

    ha_translation = types.ModuleType('homeassistant.helpers.translation')

    async def _stub_get_translations(hass, language, category, integrations=None):
        return {}

    ha_translation.async_get_translations = _stub_get_translations
    ha_helpers.translation = ha_translation

    sys.modules['homeassistant'] = ha
    sys.modules['homeassistant.helpers'] = ha_helpers
    sys.modules['homeassistant.helpers.config_validation'] = ha_cv
    sys.modules['homeassistant.helpers.device_registry'] = ha_dr
    sys.modules['homeassistant.helpers.entity_registry'] = ha_er
    sys.modules['homeassistant.helpers.selector'] = ha_selector
    sys.modules['homeassistant.helpers.translation'] = ha_translation
    sys.modules['homeassistant.const'] = ha_const
    sys.modules['homeassistant.core'] = ha_core
    sys.modules['homeassistant.config_entries'] = ha_config_entries
    sys.modules['voluptuous'] = vol
