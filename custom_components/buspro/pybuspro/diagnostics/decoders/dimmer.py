"""Dimmer decoder for load types and limits."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder
from .relay import RelayDecoder


class DimmerDecoder(DeviceTypeDecoder):
    """Decode dimmer-specific opcodes."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0x00, 0x31), (0x00, 0x32), (0x00, 0x33), (0x00, 0x34),
            (0xF0, 0x12), (0xF0, 0x13),
            (0xF0, 0x14), (0xF0, 0x15),
            (0xF0, 0x16), (0xF0, 0x17),
            (0xF0, 0x3F), (0xF0, 0x40),
            (0xF0, 0x41), (0xF0, 0x42),
            (0xF0, 0x4D), (0xF0, 0x4E),
            (0xF0, 0x4F), (0xF0, 0x50),
            (0xF0, 0x65), (0xF0, 0x66),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "ReadChannelLoadTypeResponse":
            load_types = {i + 1: payload[i] for i in range(len(payload))}
            return {"action": "read_load_types", "load_types": load_types}

        elif code_name == "ReadLimitOfEveryChannelResponse":
            if len(payload) < 2:
                return {"action": "read_limits", "limits": {}}
            limits = {
                "minimum": payload[0],
                "channels": {i + 1: payload[i + 1] for i in range(1, len(payload))},
            }
            return {"action": "read_limits", "limits": limits}

        elif code_name == "IsDeviceOnlineResponse":
            return {"action": "online_check_response", "online": True}

        # Fallback to relay decoder
        relay_decoder = RelayDecoder()
        if relay_decoder.can_decode(operate_code, payload):
            return relay_decoder.decode_payload(operate_code, payload)

        return {}
