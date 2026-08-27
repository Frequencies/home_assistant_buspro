"""Tests for RelayModule and RelayChannel telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.relay import RelayModule
from custom_components.buspro.pybuspro.devices.relay_confirmable import RelayChannel

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)


def _no_op_ensure_future(coro):
    try:
        coro.close()
    except AttributeError:
        pass
    return MagicMock(done=lambda: True, cancel=lambda: None)


def _telegram(operate_code, payload, target_address=None, source_address=None):
    t = Telegram()
    t.operate_code = operate_code
    t.payload = payload
    t.target_address = target_address or (0, 0)
    t.source_address = source_address or DEVICE_ADDRESS
    return t


def _make_relay_module():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        module = RelayModule(buspro, DEVICE_ADDRESS, initial_refresh_delay=0)
    return module


def _make_relay_confirmable_channel(channel_number=1):
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    module = MagicMock()
    module._buspro = buspro
    module._device_address = DEVICE_ADDRESS
    module.remove_channel = MagicMock()
    channel = RelayChannel(module, channel_number)
    channel._call_device_updated = MagicMock()
    return channel


class TestRelayModuleSingleChannelControlResponse(unittest.TestCase):
    """Opcode 0x0032 in RelayModule.
    payload[0]=channel_number, payload[2]=level. Min 3 bytes.
    Dispatches to the matching RelayChannel.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def _channel(self, module, number):
        ch = module.channel(number)
        ch._call_device_updated = MagicMock()
        return ch

    def test_matching_channel_updated(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        module._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [1, 0xF8, 100]))
        self.assertEqual(ch1._brightness, 100)
        self.assertTrue(ch1.is_on)

    def test_wrong_channel_not_updated(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        module._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [2, 0xF8, 100]))
        self.assertEqual(ch1._brightness, 0)

    def test_short_payload_ignored(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        module._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [1, 0xF8]))
        self.assertEqual(ch1._brightness, 0)

    def test_channel_off(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        ch1._brightness = 100
        module._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [1, 0xF8, 0]))
        self.assertEqual(ch1._brightness, 0)
        self.assertFalse(ch1.is_on)

    def test_multiple_channels_dispatched_correctly(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        ch2 = self._channel(module, 2)
        module._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [2, 0xF8, 75]))
        self.assertEqual(ch1._brightness, 0)
        self.assertEqual(ch2._brightness, 75)


class TestRelayModuleReadStatusOfChannelsResponse(unittest.TestCase):
    """Opcode 0x0034 in RelayModule.
    payload[0]=count; payload[channel_number]=level for each registered channel.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def _channel(self, module, number):
        ch = module.channel(number)
        ch._call_device_updated = MagicMock()
        return ch

    def test_single_channel_updated(self):
        module = _make_relay_module()
        ch2 = self._channel(module, 2)
        # payload: [count=4, ch1=0, ch2=75, ch3=0, ch4=0]
        module._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 75, 0, 0]))
        self.assertEqual(ch2._brightness, 75)

    def test_multiple_channels_updated(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        ch3 = self._channel(module, 3)
        module._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 100, 0, 50, 0]))
        self.assertEqual(ch1._brightness, 100)
        self.assertEqual(ch3._brightness, 50)

    def test_channel_number_exceeds_count_not_updated(self):
        module = _make_relay_module()
        ch5 = self._channel(module, 5)
        module._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [3, 0, 0, 0]))
        self.assertEqual(ch5._brightness, 0)

    def test_empty_payload_ignored(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        module._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, []))
        self.assertEqual(ch1._brightness, 0)

    def test_zero_level(self):
        module = _make_relay_module()
        ch1 = self._channel(module, 1)
        ch1._brightness = 100
        module._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [2, 0, 0]))
        self.assertEqual(ch1._brightness, 0)


class TestRelayModuleSceneControlResponse(unittest.TestCase):
    """Opcode 0x0003 in RelayModule — triggers a deferred refresh."""

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_scene_response_does_not_raise(self):
        module = _make_relay_module()
        module._telegram_received_cb(_telegram(OperateCode.SceneControlResponse, []))


class TestRelayChannelConfirmableSingleChannelControlResponse(unittest.TestCase):
    """RelayChannel (relay_confirmable.py) opcode 0x0032.
    payload[0]=channel, payload[2]=brightness. Min 3 bytes.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_matching_channel_on(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                                [1, 0xF8, 100]))
        self.assertEqual(channel._brightness, 100)
        self.assertTrue(channel.is_on)

    def test_matching_channel_off(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                                [1, 0xF8, 0]))
        self.assertEqual(channel._brightness, 0)
        self.assertFalse(channel.is_on)

    def test_non_matching_channel_ignored(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                                [2, 0xF8, 100]))
        channel._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                                [1, 0xF8]))
        channel._call_device_updated.assert_not_called()

    def test_partial_brightness(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                                [1, 0xF8, 50]))
        self.assertEqual(channel._brightness, 50)


class TestRelayChannelConfirmableReadStatusOfChannelsResponse(unittest.TestCase):
    """RelayChannel (relay_confirmable.py) opcode 0x0034.
    Guard: len(payload) > channel_number.
    Speed at payload[channel_number] directly.
    """

    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()

    def test_level_from_payload(self):
        channel = _make_relay_confirmable_channel(channel_number=2)
        channel._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                                [0, 0, 100]))
        self.assertEqual(channel._brightness, 100)

    def test_payload_too_short_ignored(self):
        channel = _make_relay_confirmable_channel(channel_number=3)
        channel._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 0]))
        channel._call_device_updated.assert_not_called()

    def test_zero_level(self):
        channel = _make_relay_confirmable_channel(channel_number=1)
        channel._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [0, 0]))
        self.assertEqual(channel._brightness, 0)
        self.assertFalse(channel.is_on)


if __name__ == "__main__":
    unittest.main()
