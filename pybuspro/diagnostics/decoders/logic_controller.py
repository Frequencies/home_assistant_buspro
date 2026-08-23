"""Logic controller decoder for device diagnostics."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder


class LogicControllerDecoder(DeviceTypeDecoder):
    """Decode logic controller diagnostics."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0xF0, 0x65), (0xF0, 0x66),
            (0xEE, 0xFD), (0xEE, 0xFE),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "IsDeviceOnlineResponse":
            return {"action": "online_check", "online": True}

        elif code_name == "ReadFirmwareVersionResponse":
            firmware_str = ""
            try:
                firmware_str = bytes(payload).rstrip(b"\x00").decode("ascii", errors="ignore")
            except Exception:
                firmware_str = ".".join(str(b) for b in payload)

            return {
                "action": "firmware_version",
                "firmware_version": firmware_str,
                "firmware_payload": payload,
            }

        return {}
