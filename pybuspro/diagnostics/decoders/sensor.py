"""Sensor decoder for multi-sensor readings."""

from typing import Any, Dict, List
from .base import DeviceTypeDecoder


class SensorDecoder(DeviceTypeDecoder):
    """Decode multi-sensor readings."""

    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        codes = {
            (0x16, 0x44), (0x16, 0x45), (0x16, 0x46), (0x16, 0x47),
            (0x16, 0x04), (0x16, 0x05),
            (0xE0, 0x18), (0xE0, 0x19),
            (0xE0, 0x17),
            (0x15, 0xCE), (0x15, 0xCF),
            (0xE3, 0xE5),
        }
        if hasattr(operate_code, 'value'):
            code_bytes = operate_code.value
        else:
            code_bytes = operate_code
        code_tuple = tuple(code_bytes) if isinstance(code_bytes, (bytes, list)) else None
        return code_tuple in codes

    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        code_name = operate_code.name if hasattr(operate_code, 'name') else str(operate_code)

        if code_name == "ReadSensorStatusResponse":
            if len(payload) < 8:
                return {}
            brightness = (payload[2] << 8) | payload[3] if len(payload) > 3 else 0
            return {
                "action": "sensor_status_response",
                "success": bool(payload[0]),
                "temperature": payload[1],
                "brightness_lux": brightness,
                "motion_detected": bool(payload[4]),
                "sonic_level": payload[5],
                "dry_contact_1": bool(payload[6]),
                "dry_contact_2": bool(payload[7]),
            }

        elif code_name == "ReadSensorsInOneStatusResponse":
            if len(payload) < 9:
                return {}
            brightness = (payload[2] << 8) | payload[3]
            return {
                "action": "sensors_in_one_response",
                "temperature": payload[1],
                "brightness_lux": brightness,
                "humidity": payload[4],
                "motion_detected": bool(payload[6]),
                "dry_contact_1": bool(payload[7]),
                "dry_contact_2": bool(payload[8]),
            }

        elif code_name in ("BroadcastSensorStatusResponse", "BroadcastSensorStatusAutoResponse"):
            if len(payload) < 7:
                return {}
            brightness = (payload[1] << 8) | payload[2]
            return {
                "action": "broadcast_sensor_status",
                "temperature": payload[0],
                "brightness_lux": brightness,
                "motion_detected": bool(payload[3]),
                "sonic_level": payload[4],
                "dry_contact_1": bool(payload[5]),
                "dry_contact_2": bool(payload[6]),
            }

        elif code_name == "ReadStatusOfUniversalSwitchResponse":
            return {
                "action": "universal_switch_status",
                "switch_number": payload[0] if len(payload) > 0 else None,
                "status": payload[1] if len(payload) > 1 else None,
            }

        elif code_name == "ReadDryContactStatusResponse":
            return {
                "action": "dry_contact_status",
                "switch_number": payload[1] if len(payload) > 1 else None,
                "status": bool(payload[2]) if len(payload) > 2 else None,
            }

        return {}
