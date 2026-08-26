"""Read-only diagnostics for an HDL Buspro logic controller."""

import asyncio
from datetime import datetime, timezone
import time

from .control import _GenericControl
from .device import Device
from ..helpers.enums import OperateCode


def decode_firmware_version(payload):
    """Decode firmware payloads without assuming one HDL firmware format."""
    values = bytes(payload or ())
    if not values:
        return None
    text = values.rstrip(b"\x00").decode("ascii", errors="ignore").strip()
    if text and all(32 <= value <= 126 for value in values.rstrip(b"\x00")):
        return text
    return ".".join(str(value) for value in values)


class LogicControllerDiagnostics(Device):
    """Shared status reader and telegram source for one logic controller."""

    def __init__(self, buspro, device_address, initial_refresh_delay=10):
        super().__init__(buspro, device_address)
        self._online = None
        self._firmware_version = None
        self._firmware_payload = None
        self._last_seen = None
        self._last_response = 0.0
        self._last_firmware_query = None
        self._telegram_cbs = []
        self._closed = False
        self.register_telegram_received_cb(self._telegram_received_cb)
        self._refresh_task = asyncio.ensure_future(self._refresh_loop(initial_refresh_delay))

    def register_telegram_cb(self, callback):
        """Register a listener for telegrams transmitted by the controller."""
        self._telegram_cbs.append(callback)

    def unregister_telegram_cb(self, callback):
        """Remove a telegram listener."""
        try:
            self._telegram_cbs.remove(callback)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        if tuple(telegram.source_address or ()) != self._device_address:
            return

        self._online = True
        self._last_response = time.monotonic()
        self._last_seen = datetime.now(timezone.utc)

        if telegram.operate_code == OperateCode.ReadFirmwareVersionResponse:
            self._firmware_payload = list(telegram.payload or ())
            self._firmware_version = decode_firmware_version(
                self._firmware_payload
            )

        for callback in list(self._telegram_cbs):
            callback(telegram)
        self._call_device_updated()

    async def _send_query(self, operate_code):
        control = _GenericControl(self._buspro)
        control.subnet_id, control.device_id = self._device_address
        control.operate_code = operate_code
        control.payload = []
        await control.send()

    async def refresh(self):
        """Refresh diagnostics using bounded read-only bus traffic."""
        now = time.monotonic()
        if self._last_response and now - self._last_response > 150:
            self._online = False
            self._call_device_updated()
        await self._send_query(OperateCode.IsDeviceOnline)
        if (
            self._last_firmware_query is None
            or now - self._last_firmware_query > 21600
        ):
            await asyncio.sleep(1)
            await self._send_query(OperateCode.ReadFirmwareVersion)
            self._last_firmware_query = time.monotonic()

    async def _refresh_loop(self, initial_refresh_delay):
        try:
            await asyncio.sleep(initial_refresh_delay)
            while not self._closed:
                await self.refresh()
                await asyncio.sleep(60)
        except asyncio.CancelledError:
            pass

    @property
    def online(self):
        return self._online

    @property
    def firmware_version(self):
        return self._firmware_version

    @property
    def firmware_payload(self):
        return self._firmware_payload

    @property
    def last_seen(self):
        return self._last_seen

    def close(self):
        """Stop polling and detach from the bus."""
        self._closed = True
        if not self._refresh_task.done():
            self._refresh_task.cancel()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass
