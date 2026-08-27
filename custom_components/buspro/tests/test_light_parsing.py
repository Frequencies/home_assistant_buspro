"""Tests for Light and LightConfirmable telegram parsing."""

import unittest
from unittest.mock import MagicMock, patch

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.core.telegram import Telegram
from custom_components.buspro.pybuspro.helpers.enums import OperateCode
from custom_components.buspro.pybuspro.devices.light import Light
from custom_components.buspro.pybuspro.devices.light_confirmable import Light as LightConfirmable

CLIENT_ADDRESS = (1, 100)
DEVICE_ADDRESS = (1, 10)
CHANNEL = 2


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


def _make_light():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = Light(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


def _make_light_confirmable():
    buspro = MagicMock()
    buspro.client_address = CLIENT_ADDRESS
    with patch("asyncio.ensure_future", side_effect=_no_op_ensure_future):
        device = LightConfirmable(buspro, DEVICE_ADDRESS, channel_number=CHANNEL)
    device._call_device_updated = MagicMock()
    return device


class TestLightSingleChannelControlResponse(unittest.TestCase):
    """Opcode 0x0032 — brightness echo after a set command.
    payload[0]=channel, payload[2]=brightness.
    Clears _awaiting_ack; updates _previous_brightness if nonzero.
    Requires len >= 3.
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_sets_brightness(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 75]))
        self.assertEqual(device.current_brightness, 75)

    def test_non_matching_channel_ignored(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL + 1, 0xF8, 75]))
        device._call_device_updated.assert_not_called()

    def test_short_payload_ignored(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8]))
        device._call_device_updated.assert_not_called()

    def test_clears_awaiting_ack(self):
        device = _make_light()
        device._awaiting_ack = True
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 50]))
        self.assertFalse(device._awaiting_ack)

    def test_updates_previous_brightness_when_nonzero(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 80]))
        self.assertEqual(device.previous_brightness, 80)

    def test_does_not_update_previous_brightness_when_zero(self):
        device = _make_light()
        device._previous_brightness = 60
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 0]))
        self.assertEqual(device.previous_brightness, 60)

    def test_is_on_when_brightness_nonzero(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 100]))
        self.assertTrue(device.is_on)

    def test_is_off_when_brightness_zero(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 0]))
        self.assertFalse(device.is_on)


class TestLightReadStatusOfChannelsResponse(unittest.TestCase):
    """Opcode 0x0034 — multi-channel status poll.
    payload[0]=count; payload[channel]=brightness.
    Double guard: channel <= payload[0] AND channel < len(payload).
    """
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_brightness_set_from_channel_index(self):
        device = _make_light()
        # payload: [count=4, ch1=0, ch2=80, ch3=0, ch4=0]
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 80, 0, 0]))
        self.assertEqual(device.current_brightness, 80)

    def test_channel_exceeds_count_ignored(self):
        device = _make_light()
        # CHANNEL=2, payload[0]=1 → 2 > 1 → ignored
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [1, 50]))
        device._call_device_updated.assert_not_called()

    def test_channel_beyond_payload_length_ignored(self):
        device = _make_light()
        # payload[0]=4 but only 2 entries → channel=2 is at index 2 but len([4,50])=2 → out of bounds
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [4, 50]))
        device._call_device_updated.assert_not_called()

    def test_zero_brightness(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 0, 0, 0]))
        self.assertEqual(device.current_brightness, 0)
        self.assertFalse(device.is_on)

    def test_full_brightness(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 100, 0, 0]))
        self.assertEqual(device.current_brightness, 100)
        self.assertTrue(device.is_on)


class TestLightSceneControlResponse(unittest.TestCase):
    """Opcode 0x0003 — scene change triggers a re-read (no direct state change)."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_scene_response_does_not_change_brightness(self):
        device = _make_light()
        device._telegram_received_cb(_telegram(OperateCode.SceneControlResponse, []))
        # Brightness stays at default (0); re-read is scheduled but patched out
        self.assertEqual(device.current_brightness, 0)


class TestLightConfirmableSingleChannelControlResponse(unittest.TestCase):
    """LightConfirmable has identical parsing (plus mark_confirmed)."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_matching_channel_sets_brightness(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 65]))
        self.assertEqual(device.current_brightness, 65)

    def test_non_matching_channel_ignored(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [99, 0xF8, 65]))
        device._call_device_updated.assert_not_called()

    def test_is_on_when_nonzero(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 50]))
        self.assertTrue(device.is_on)

    def test_is_off_when_zero(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.SingleChannelControlResponse,
                                               [CHANNEL, 0xF8, 0]))
        self.assertFalse(device.is_on)


class TestLightConfirmableReadStatusOfChannelsResponse(unittest.TestCase):
    """LightConfirmable 0x0034 — guard: channel <= payload[0] only (no len check)."""
    def setUp(self):
        self._patcher = patch("asyncio.ensure_future", side_effect=_no_op_ensure_future)
        self._patcher.start()

    def tearDown(self):
        self._patcher.stop()


    def test_brightness_updated(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse,
                                               [4, 0, 90, 0, 0]))
        self.assertEqual(device.current_brightness, 90)

    def test_channel_exceeds_count_ignored(self):
        device = _make_light_confirmable()
        device._telegram_received_cb(_telegram(OperateCode.ReadStatusOfChannelsResponse, [1, 50]))
        device._call_device_updated.assert_not_called()


if __name__ == "__main__":
    unittest.main()
