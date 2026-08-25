"""Cover decoder for curtain and blind control."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder


class CoverDecoder(DeviceTypeDecoder):
    """Decode curtain/blind control."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0xE3, 0xE0), (0xE3, 0xE1),
            (0xE3, 0xE2), (0xE3, 0xE3),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "CurtainSwitchControl":
            command_names = {0: "stop", 1: "open", 2: "close"}
            return {
                "action": "control",
                "channel": payload[0] if len(payload) > 0 else None,
                "command": command_names.get(payload[1] if len(payload) > 1 else None, "unknown"),
            }

        elif code_name in ("CurtainSwitchControlResponse", "ReadStatusofCurtainSwitchResponse"):
            state_names = {0: "stopped", 1: "opening", 2: "closing"}
            return {
                "action": "status_response",
                "channel": payload[0] if len(payload) > 0 else None,
                "state": state_names.get(payload[1] if len(payload) > 1 else None, "unknown"),
            }

        elif code_name == "ReadStatusofCurtainSwitch":
            return {
                "action": "read_status",
                "channel": payload[0] if len(payload) > 0 else None,
            }

        return {}
