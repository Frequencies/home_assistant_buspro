import unittest

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

import custom_components.buspro as buspro_init
from custom_components.buspro.const import CONF_HOST, CONF_PORT, CONF_SEND_PORT, CONF_RECEIVE_PORT


class _FakeConfigEntry:
    def __init__(self, data, options=None, entry_id='e1'):
        self.data = data
        self.options = options or {}
        self.entry_id = entry_id


class _FakeHass:
    def __init__(self):
        self.data = {}


class _FakeModule:
    created = []

    def __init__(self, hass, host, port, send_port=None, receive_port=None):
        self.hass = hass
        self.host = host
        self.port = port
        self.send_port = send_port
        self.receive_port = receive_port
        self.started = False
        self.services_registered = False
        _FakeModule.created.append(self)

    async def start(self):
        self.started = True

    def register_services(self, force=False):
        self.services_registered = True


class SetupEntryTests(unittest.IsolatedAsyncioTestCase):
    async def test_setup_entry_prefers_options_over_data(self):
        orig = buspro_init.BusproModule
        _FakeModule.created.clear()
        buspro_init.BusproModule = _FakeModule
        try:
            hass = _FakeHass()
            entry = _FakeConfigEntry(
                data={
                    CONF_HOST: '1.1.1.1',
                    CONF_PORT: 6000,
                    CONF_SEND_PORT: 6000,
                    CONF_RECEIVE_PORT: 6000,
                },
                options={
                    CONF_HOST: '2.2.2.2',
                    CONF_PORT: 6001,
                    CONF_SEND_PORT: 6002,
                    CONF_RECEIVE_PORT: 6003,
                },
            )

            ok = await buspro_init.async_setup_entry(hass, entry)

            self.assertTrue(ok)
            self.assertEqual(len(_FakeModule.created), 1)
            mod = _FakeModule.created[0]
            self.assertEqual(mod.host, '2.2.2.2')
            self.assertEqual(mod.port, 6001)
            self.assertEqual(mod.send_port, 6002)
            self.assertEqual(mod.receive_port, 6003)
            self.assertTrue(mod.started)
            self.assertTrue(mod.services_registered)
        finally:
            buspro_init.BusproModule = orig


if __name__ == '__main__':
    unittest.main()
