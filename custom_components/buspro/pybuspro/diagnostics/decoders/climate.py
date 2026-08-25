"""Climate decoder for floor heating and AC control."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder


class ClimateDecoder(DeviceTypeDecoder):
    """Decode floor heating and AC climate control."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0x19, 0x44), (0x19, 0x45),
            (0x19, 0x46), (0x19, 0x47),
            (0x19, 0x48), (0x19, 0x49),
            (0x1C, 0x5C), (0x1C, 0x5D),
            (0x1C, 0x5E), (0x1C, 0x5F),
            (0xE3, 0xD8), (0xE3, 0xD9),
            (0xE3, 0xDA), (0xE3, 0xDB),
            (0xE3, 0xE5),
            (0xE3, 0xE7), (0xE3, 0xE8),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "ReadFloorHeatingStatusResponse":
            if len(payload) < 8:
                return {}
            mode_names = {0: "", 1: "Normal", 2: "Day", 3: "Night", 4: "Away", 5: "Timer"}
            return {
                "action": "floor_heating_status_response",
                "temperature_type": "celsius" if payload[0] == 0 else "fahrenheit",
                "status": bool(payload[1]),
                "mode": payload[2],
                "mode_name": mode_names.get(payload[2], "Unknown"),
                "normal_temperature": payload[3],
                "day_temperature": payload[4],
                "night_temperature": payload[5],
                "away_temperature": payload[6],
                "work_type": payload[7],
            }

        elif code_name == "ControlFloorHeatingModuleStatusResponse":
            return {
                "action": "floor_heating_module_control_response",
                "channel": payload[0] if len(payload) > 0 else None,
                "success": bool(payload[1]) if len(payload) > 1 else False,
            }

        elif code_name == "ReadPanelACResponse":
            commands = {3: "status", 4: "temperature"}
            command = payload[0] if len(payload) > 0 else None
            value = payload[1] if len(payload) > 1 else None
            return {
                "action": "panel_ac_response",
                "command": commands.get(command, f"unknown_{command}"),
                "value": value,
            }

        elif code_name == "BroadcastTemperatureResponse":
            return {
                "action": "broadcast_temperature",
                "temperature": payload[1] if len(payload) > 1 else None,
            }

        return {}
