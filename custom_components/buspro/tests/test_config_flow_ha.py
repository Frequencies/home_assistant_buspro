import asyncio
import unittest

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro import config_flow as cf
from custom_components.buspro.const import (
    CONF_HOST,
    CONF_PORT,
    CONF_SEND_PORT,
    CONF_RECEIVE_PORT,
    CONF_CLIENT_ADDRESS,
    DEFAULT_CLIENT_ADDRESS,
)

_VALID_INPUT = {
    CONF_HOST: '192.168.1.10',
    CONF_PORT: 6000,
    CONF_SEND_PORT: 6000,
    CONF_RECEIVE_PORT: 6000,
    CONF_CLIENT_ADDRESS: DEFAULT_CLIENT_ADDRESS,
}


class _FakeEntry:
    def __init__(self, entry_id='e1', data=None, options=None):
        self.entry_id = entry_id
        self.data = data or {}
        self.options = options or {}
        self.state = None  # not ConfigEntryState.LOADED → probe_socket=True in reconfigure


class _FakeConfigEntries:
    def __init__(self):
        self.entries = {}
        self.updated = []
        self.reloaded = []

    def async_get_entry(self, entry_id):
        return self.entries.get(entry_id)

    def async_update_entry(self, entry, data=None, options=None):
        if data is not None:
            entry.data = data
        if options is not None:
            entry.options = options
        self.updated.append((entry.entry_id, data, options))

    async def async_reload(self, entry_id):
        self.reloaded.append(entry_id)


class _FakeHass:
    def __init__(self):
        self.loop = asyncio.get_running_loop()
        self.config_entries = _FakeConfigEntries()
        self.existing_unique_ids = set()

    async def async_add_executor_job(self, func, *args):
        return func(*args)


class ConfigFlowTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.orig_validate = cf._async_validate_connectivity

    async def asyncTearDown(self):
        cf._async_validate_connectivity = self.orig_validate

    async def test_user_step_success_creates_entry(self):
        async def ok_validate(hass, data, probe_socket=True):
            return None

        cf._async_validate_connectivity = ok_validate
        flow = cf.ConfigFlow()
        flow.hass = _FakeHass()

        result = await flow.async_step_user({**_VALID_INPUT})

        self.assertEqual(result['type'], 'create_entry')
        self.assertEqual(result['title'], 'Buspro (192.168.1.10)')
        self.assertEqual(result['data'][CONF_HOST], '192.168.1.10')

    async def test_user_step_invalid_host_shows_error(self):
        async def bad_validate(hass, data, probe_socket=True):
            raise cf.InvalidHost()

        cf._async_validate_connectivity = bad_validate
        flow = cf.ConfigFlow()
        flow.hass = _FakeHass()

        result = await flow.async_step_user({
            CONF_HOST: 'bad-host',
            CONF_PORT: 6000,
            CONF_CLIENT_ADDRESS: DEFAULT_CLIENT_ADDRESS,
        })

        self.assertEqual(result['type'], 'form')
        self.assertEqual(result['errors'].get('base'), 'invalid_host')

    async def test_options_flow_init_shows_menu(self):
        entry = _FakeEntry(data={CONF_HOST: '1.1.1.1', CONF_PORT: 6000})
        flow = cf.BusproOptionsFlow(entry)
        flow.hass = _FakeHass()

        result = await flow.async_step_init(None)

        self.assertEqual(result['type'], 'menu')
        self.assertIn('gateway', result['menu_options'])

    async def test_options_flow_gateway_saves_data(self):
        async def ok_validate(hass, data, probe_socket=True):
            return None

        cf._async_validate_connectivity = ok_validate
        entry = _FakeEntry(data={CONF_HOST: '1.1.1.1', CONF_PORT: 6000})
        flow = cf.BusproOptionsFlow(entry)
        flow.hass = _FakeHass()

        result = await flow.async_step_gateway({
            CONF_HOST: '2.2.2.2',
            CONF_PORT: 6001,
            CONF_SEND_PORT: 6001,
            CONF_RECEIVE_PORT: 6001,
            CONF_CLIENT_ADDRESS: DEFAULT_CLIENT_ADDRESS,
        })

        self.assertEqual(result['type'], 'create_entry')
        self.assertEqual(result['data'][CONF_HOST], '2.2.2.2')
        self.assertEqual(result['data'][CONF_PORT], 6001)

    async def test_reconfigure_updates_and_reloads(self):
        async def ok_validate(hass, data, probe_socket=True):
            return None

        cf._async_validate_connectivity = ok_validate
        hass = _FakeHass()
        entry = _FakeEntry(
            entry_id='entry-1',
            data={CONF_HOST: '10.0.0.1', CONF_PORT: 6000},
            options={},
        )
        hass.config_entries.entries[entry.entry_id] = entry

        flow = cf.ConfigFlow()
        flow.hass = hass
        flow.context = {'entry_id': entry.entry_id}

        result = await flow.async_step_reconfigure({
            CONF_HOST: '10.0.0.2',
            CONF_PORT: 6002,
            CONF_SEND_PORT: 6002,
            CONF_RECEIVE_PORT: 6002,
            CONF_CLIENT_ADDRESS: DEFAULT_CLIENT_ADDRESS,
        })

        self.assertEqual(result['type'], 'abort')
        self.assertEqual(result['reason'], 'reconfigure_successful')
        self.assertEqual(entry.data[CONF_HOST], '10.0.0.2')
        self.assertIn(entry.entry_id, hass.config_entries.reloaded)


if __name__ == '__main__':
    unittest.main()
