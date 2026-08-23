"""Relay decoder for control and response telegrams."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder


class RelayDecoder(DeviceTypeDecoder):
    """Decode relay control and response telegrams."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0x00, 0x31), (0x00, 0x32), (0x00, 0x33), (0x00, 0x34), (0x00, 0x03),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "SingleChannelControl":
            return {
                "action": "control",
                "channel": payload[0] if len(payload) > 0 else None,
                "brightness": payload[1] if len(payload) > 1 else None,
                "runtime_minutes": payload[2] if len(payload) > 2 else 0,
                "runtime_seconds": payload[3] if len(payload) > 3 else 0,
            }

        elif code_name == "SingleChannelControlResponse":
            return {
                "action": "control_response",
                "channel": payload[0] if len(payload) > 0 else None,
                "success": bool(payload[1] if len(payload) > 1 else False),
                "brightness": payload[2] if len(payload) > 2 else None,
            }

        elif code_name == "ReadStatusOfChannels":
            return {"action": "read_all_status"}

        elif code_name == "ReadStatusOfChannelsResponse":
            if len(payload) < 1:
                return {"action": "read_all_status_response", "channels": {}}
            channel_count = payload[0]
            channels = {
                i + 1: payload[i + 1]
                for i in range(min(channel_count, len(payload) - 1))
            }
            return {
                "action": "read_all_status_response",
                "channel_count": channel_count,
                "channels": channels,
            }

        elif code_name == "SceneControlResponse":
            return {"action": "scene_control_response"}

        return {}
