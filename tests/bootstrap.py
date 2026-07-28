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

    ha_const = types.ModuleType('homeassistant.const')
    ha_const.CONF_HOST = 'host'
    ha_const.CONF_PORT = 'port'
    ha_const.CONF_NAME = 'name'
    ha_const.EVENT_HOMEASSISTANT_STOP = 'homeassistant_stop'

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

    ha_config_entries.ConfigFlow = ConfigFlow
    ha_config_entries.OptionsFlow = OptionsFlow

    class ConfigEntry:  # pragma: no cover - stub
        pass
    ha_config_entries.ConfigEntry = ConfigEntry

    vol = types.ModuleType('voluptuous')
    vol.ALLOW_EXTRA = object()
    vol.Required = lambda key, default=None: key
    vol.Optional = lambda key, default=None: key
    vol.Any = lambda *args, **kwargs: args[0] if args else None
    vol.All = lambda *args, **kwargs: args[0] if args else None
    vol.Length = lambda *args, **kwargs: None
    vol.Schema = lambda *args, **kwargs: dict

    sys.modules['homeassistant'] = ha
    sys.modules['homeassistant.helpers'] = ha_helpers
    sys.modules['homeassistant.helpers.config_validation'] = ha_cv
    sys.modules['homeassistant.const'] = ha_const
    sys.modules['homeassistant.core'] = ha_core
    sys.modules['homeassistant.config_entries'] = ha_config_entries
    sys.modules['voluptuous'] = vol
