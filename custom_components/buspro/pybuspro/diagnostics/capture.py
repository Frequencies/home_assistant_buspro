"""Core diagnostic capture engine."""

import logging
from collections import deque
from dataclasses import asdict
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List

from .models import Direction, TelegramRecord
from .decoders.base import DeviceTypeDecoder

_LOGGER = logging.getLogger(__name__)


class DiagnosticCapture:
    """Unified telegram capture with circular buffer and aliasing."""

    def __init__(
        self,
        max_records: int = 5000,
        address_aliases: Optional[Dict[tuple, str]] = None,
        opcode_names: Optional[Dict[bytes, str]] = None,
    ):
        self._max_records = max_records
        self._records: deque = deque(maxlen=max_records)
        self._address_aliases = address_aliases or {}
        self._opcode_names = opcode_names or {}
        self._decoders: Dict[str, DeviceTypeDecoder] = {}
        self._enabled_devices: set = set()
        self._enabled_global = True

    def subscribe_device(self, device_address: tuple) -> None:
        """Enable capture for a device."""
        self._enabled_devices.add(tuple(device_address))

    def unsubscribe_device(self, device_address: tuple) -> None:
        """Disable capture for a device."""
        self._enabled_devices.discard(tuple(device_address))

    def set_enabled_global(self, enabled: bool) -> None:
        """Enable/disable diagnostics globally."""
        self._enabled_global = enabled

    def set_address_alias(self, address: tuple, alias: str) -> None:
        """Map address to friendly name."""
        self._address_aliases[tuple(address)] = alias

    def remove_address_alias(self, address: tuple) -> None:
        """Remove alias."""
        self._address_aliases.pop(tuple(address), None)

    def register_decoder(self, device_type: str, decoder: DeviceTypeDecoder) -> None:
        """Register device-specific decoder."""
        self._decoders[device_type] = decoder

    def record_telegram(
        self,
        telegram: Any,
        direction: Direction,
    ) -> None:
        """Record a telegram with optional decoding."""
        if not self._enabled_global:
            return

        source_addr = tuple(telegram.source_address or ())
        target_addr = tuple(telegram.target_address or ())

        # Apply subscription filter
        if direction == Direction.REQUEST and target_addr not in self._enabled_devices:
            return
        if direction in (Direction.RESPONSE, Direction.BROADCAST) and source_addr not in self._enabled_devices:
            return

        # Decode opcode
        opcode_bytes = telegram.operate_code.value if hasattr(telegram.operate_code, 'value') else telegram.operate_code
        opcode_hex = f"0x{opcode_bytes.hex().upper()}"
        opcode_name = self._opcode_names.get(opcode_bytes) or telegram.operate_code.name

        payload = list(telegram.payload or [])

        # Try device-specific decoders
        decoded = None
        device_type_hint = None

        for device_type, decoder in self._decoders.items():
            if decoder.can_decode(telegram.operate_code, payload):
                try:
                    decoded = decoder.decode_payload(telegram.operate_code, payload)
                    device_type_hint = device_type
                    break
                except Exception as e:
                    _LOGGER.debug(f"Decoder error for {device_type}: {e}")

        record = TelegramRecord(
            timestamp=datetime.now(timezone.utc).isoformat(),
            direction=direction,
            source_address=source_addr,
            source_alias=self._address_aliases.get(source_addr),
            target_address=target_addr,
            target_alias=self._address_aliases.get(target_addr),
            operate_code=opcode_hex,
            operate_code_name=opcode_name,
            operate_code_enum=telegram.operate_code.name,
            payload=payload,
            payload_size=len(payload),
            crc=telegram.crc if hasattr(telegram, 'crc') else None,
            decoded=decoded,
            device_type_hint=device_type_hint,
        )

        self._records.append(record)

    def get_records(
        self,
        filters: Optional[Dict[str, Any]] = None,
        limit: int = 100,
    ) -> List[Dict[str, Any]]:
        """Retrieve captured records with filtering."""
        filters = filters or {}
        results = []

        for record in reversed(list(self._records)):
            # Filter by direction
            if "direction" in filters:
                dir_val = filters["direction"]
                if isinstance(dir_val, str):
                    try:
                        dir_val = Direction(dir_val)
                    except ValueError:
                        continue
                if record.direction != dir_val:
                    continue

            # Filter by opcode
            if "operate_code" in filters:
                if record.operate_code != filters["operate_code"]:
                    continue

            # Filter by device type
            if "device_type" in filters:
                if record.device_type_hint != filters["device_type"]:
                    continue

            # Filter by source address (or alias)
            if "source_address" in filters:
                addr_filter = filters["source_address"]
                if isinstance(addr_filter, str):
                    if record.source_alias != addr_filter:
                        continue
                else:
                    if record.source_address != tuple(addr_filter):
                        continue

            # Filter by target address
            if "target_address" in filters:
                addr_filter = filters["target_address"]
                if isinstance(addr_filter, str):
                    if record.target_alias != addr_filter:
                        continue
                else:
                    if record.target_address != tuple(addr_filter):
                        continue

            # Filter by time
            if "since_timestamp" in filters:
                if record.timestamp < filters["since_timestamp"]:
                    continue

            results.append(asdict(record))
            if len(results) >= limit:
                break

        return results

    def clear_records(self) -> None:
        """Clear all records."""
        self._records.clear()

    def get_stats(self) -> Dict[str, Any]:
        """Return statistics."""
        return {
            "total_records": len(self._records),
            "max_records": self._max_records,
            "enabled_global": self._enabled_global,
            "subscribed_devices": len(self._enabled_devices),
            "decoders_registered": len(self._decoders),
        }
