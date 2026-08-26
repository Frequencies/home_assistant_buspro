"""Passive + active HDL Buspro bus scanner.

Discovers physical devices by hooking the catch-all telegram callback and
repeatedly broadcasting a spread of read requests. A directed phase follows
to ask each found device individually for its channel status, which many
relay/dimmer modules only answer when addressed directly.
"""
from __future__ import annotations

import asyncio
import logging
import time
from dataclasses import dataclass, field

from .pybuspro.buspro import Buspro
from .pybuspro.core.telegram import Telegram
from .pybuspro.helpers.enums import OperateCode

_LOGGER = logging.getLogger(__name__)

_BROADCAST: tuple[int, int] = (255, 255)

_IGNORED_SOURCES = {(200, 200), (0, 0), (255, 255)}

# Broadcast read requests that provoke replies from every device class.
# Note: curtain enum is ReadStatusofCurtainSwitch (lowercase 'o') in this codebase.
_PROVOCATIONS: tuple[tuple[object, list[int]], ...] = (
    (OperateCode.ReadStatusOfChannels, []),
    (OperateCode.ReadSensorStatus, []),
    (OperateCode.ReadSensorsInOneStatus, []),
    (OperateCode.ReadFloorHeatingStatus, []),
    (OperateCode.ReadDryContactStatus, [1, 1]),
    (OperateCode.ReadStatusOfUniversalSwitch, [1]),
    (OperateCode.ReadStatusofCurtainSwitch, [1]),
    (OperateCode.ReadStatusofCurtainSwitch, [2]),
    (b"\x00\x0e", []),
)

_TYPE_HI = 19
_TYPE_LO = 20

_POLL_INTERVAL = 2.5
_FRAME_GAP = 0.05
_DIRECTED_ROUNDS = 2
_DIRECTED_LISTEN = 2.0
_DIRECTED_MAX_SECONDS = 20.0

_KEYPAD_COMMAND_OPS = {
    "SingleChannelControl",
    "SceneControl",
    "UniversalSwitchControl",
    "BroadcastStatusOfUniversalSwitch",
}

_LOAD_RESPONSE_OPS = {
    "ReadStatusOfChannelsResponse",
    "SingleChannelControlResponse",
    "ReadSensorStatusResponse",
    "ReadSensorsInOneStatusResponse",
    "BroadcastSensorStatusResponse",
    "BroadcastSensorStatusAutoResponse",
    "ReadFloorHeatingStatusResponse",
    "ReadDryContactStatusResponse",
    "ReadStatusOfUniversalSwitchResponse",
    "ReadStatusofCurtainSwitchResponse",
    "CurtainSwitchControlResponse",
}


@dataclass
class DiscoveredDevice:
    """A single device heard on the bus during a scan."""

    subnet_id: int
    device_id: int
    type_code: str
    type_name: str
    channel_count: int | None = None
    op_codes: set[str] = field(default_factory=set)
    dimmer_evidence: bool = False

    @property
    def address(self) -> str:
        return f"{self.subnet_id}.{self.device_id}"

    @property
    def key(self) -> str:
        return f"{self.subnet_id}-{self.device_id}"

    @property
    def looks_like_keypad(self) -> bool:
        return (
            self.channel_count is None
            and bool(self.op_codes & _KEYPAD_COMMAND_OPS)
            and not (self.op_codes & _LOAD_RESPONSE_OPS)
        )

    def summary(self) -> str:
        chans = f"{self.channel_count}ch" if self.channel_count else "?ch"
        ops = ",".join(sorted(self.op_codes)) or "none"
        hints = []
        if self.dimmer_evidence:
            hints.append("dimmer")
        if self.looks_like_keypad:
            hints.append("keypad")
        hint = f" [{'/'.join(hints)}]" if hints else ""
        return (
            f"{self.address} type={self.type_code}({self.type_name}) "
            f"{chans}{hint} replied=[{ops}]"
        )


class BusScanner:
    """Harvest devices from an HDL Buspro bus using a live Buspro client."""

    def __init__(self, buspro: Buspro) -> None:
        self._buspro = buspro
        self._found: dict[tuple[int, int], DiscoveredDevice] = {}

    def _on_telegram(self, telegram) -> None:
        try:
            allowed = getattr(self._buspro, "allowed_source_ips", None)
            udp_addr = getattr(telegram, "udp_address", None)
            if allowed and udp_addr and udp_addr[0] not in allowed:
                return

            src = getattr(telegram, "source_address", None)
            if not src:
                return
            subnet, device = int(src[0]), int(src[1])
            if (subnet, device) in _IGNORED_SOURCES:
                return

            type_code, type_name = self._extract_type(telegram)
            dev = self._found.get((subnet, device))
            if dev is None:
                dev = DiscoveredDevice(
                    subnet_id=subnet,
                    device_id=device,
                    type_code=type_code,
                    type_name=type_name,
                )
                self._found[(subnet, device)] = dev
            elif dev.type_name == "Unknown" and type_name != "Unknown":
                dev.type_code = type_code
                dev.type_name = type_name

            op_name = self._op_name(telegram)
            if op_name:
                dev.op_codes.add(op_name)

            if op_name == "ReadStatusOfChannelsResponse":
                payload = getattr(telegram, "payload", None) or []
                if payload:
                    count = int(payload[0])
                    if 1 <= count <= 64:
                        dev.channel_count = max(dev.channel_count or 0, count)
                    for raw in payload[1 : 1 + min(count, 64)]:
                        try:
                            level = int(raw)
                        except (TypeError, ValueError):
                            continue
                        if 1 <= level <= 254 and level != 100:
                            dev.dimmer_evidence = True
                            break
            elif op_name == "SingleChannelControlResponse":
                payload = getattr(telegram, "payload", None) or []
                if len(payload) >= 3:
                    try:
                        level = int(payload[2])
                    except (TypeError, ValueError):
                        level = -1
                    if 1 <= level <= 254 and level != 100:
                        dev.dimmer_evidence = True
            elif op_name in (
                "ReadStatusofCurtainSwitchResponse",
                "CurtainSwitchControlResponse",
            ):
                payload = getattr(telegram, "payload", None) or []
                if payload:
                    try:
                        curtain_no = int(payload[0])
                    except (TypeError, ValueError):
                        curtain_no = 0
                    if 1 <= curtain_no <= 32:
                        dev.channel_count = max(dev.channel_count or 0, curtain_no)
        except Exception as err:  # noqa: BLE001
            _LOGGER.debug("Scan telegram parse error: %s", err)

    @staticmethod
    def _extract_type(telegram) -> tuple[str, str]:
        type_code = "0x0000"
        udp = getattr(telegram, "udp_data", None)
        if udp is not None and len(udp) > _TYPE_LO:
            type_code = f"0x{udp[_TYPE_HI]:02X}{udp[_TYPE_LO]:02X}"
        source_device_type = getattr(telegram, "source_device_type", None)
        type_name = getattr(source_device_type, "name", None) or "Unknown"
        return type_code, type_name

    @staticmethod
    def _op_name(telegram) -> str | None:
        oc = getattr(telegram, "operate_code", None)
        name = getattr(oc, "name", None)
        if name:
            return name
        udp = getattr(telegram, "udp_data", None)
        if udp is not None and len(udp) > 22:
            return f"0x{udp[21]:02X}{udp[22]:02X}"
        return None

    async def scan(self, duration: float = 15.0) -> list[DiscoveredDevice]:
        """Run discovery and return devices sorted by address."""
        buspro = self._buspro
        if buspro is None or buspro.network_interface is None:
            raise RuntimeError("gateway_unavailable")

        duration = max(float(duration), 1.0)
        previous_cb = buspro.callback_all_messages
        buspro.register_telegram_received_all_messages_cb(self._on_telegram)
        try:
            elapsed = 0.0
            while elapsed < duration:
                await self._broadcast_provocations()
                step = min(_POLL_INTERVAL, duration - elapsed)
                if step <= 0:
                    break
                await asyncio.sleep(step)
                elapsed += step
            await self._directed_channel_reads()
        finally:
            buspro.callback_all_messages = previous_cb

        found = sorted(
            self._found.values(), key=lambda d: (d.subnet_id, d.device_id)
        )
        self._log_summary(found, duration)
        return found

    async def _broadcast_provocations(self) -> None:
        ni = self._buspro.network_interface
        if ni is None:
            return
        for operate_code, payload in _PROVOCATIONS:
            telegram = Telegram()
            telegram.target_address = _BROADCAST
            telegram.operate_code = operate_code
            telegram.payload = list(payload)
            try:
                await ni.send_telegram(telegram)
            except Exception as err:  # noqa: BLE001
                _LOGGER.debug("Provocation send failed (%s): %s", operate_code, err)
            await asyncio.sleep(_FRAME_GAP)

    async def _directed_channel_reads(self) -> None:
        ni = self._buspro.network_interface
        if ni is None or not self._found:
            return
        addresses = [(d.subnet_id, d.device_id) for d in list(self._found.values())]
        deadline = time.monotonic() + _DIRECTED_MAX_SECONDS
        for _round in range(_DIRECTED_ROUNDS):
            if time.monotonic() >= deadline:
                break
            for subnet, device in addresses:
                if time.monotonic() >= deadline:
                    break
                telegram = Telegram()
                telegram.target_address = (subnet, device)
                telegram.operate_code = OperateCode.ReadStatusOfChannels
                telegram.payload = []
                try:
                    await ni.send_telegram(telegram)
                except Exception as err:  # noqa: BLE001
                    _LOGGER.debug("Directed read to %s.%s failed: %s", subnet, device, err)
                await asyncio.sleep(_FRAME_GAP)
            await asyncio.sleep(
                min(_DIRECTED_LISTEN, max(deadline - time.monotonic(), 0.0))
            )

    def _log_summary(self, found: list[DiscoveredDevice], duration: float) -> None:
        if not found:
            _LOGGER.info(
                "HDL Buspro bus scan (%.0fs): no devices responded. "
                "Check gateway IP and that HA can receive UDP on port 6000.",
                duration,
            )
            return
        _LOGGER.info("HDL Buspro bus scan (%.0fs): %d device(s) found:", duration, len(found))
        for dev in found:
            _LOGGER.info("  %s", dev.summary())
