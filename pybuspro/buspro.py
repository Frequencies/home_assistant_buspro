''' pybuspro version 1.0.0  '''

import asyncio
import logging

from .helpers.enums import *
from .transport.network_interface import NetworkInterface


# ip, port = gateway_address
# subnet_id, device_id, channel = device_address


class Buspro:
    def __init__(
        self,
        gateway_address_send_receive,
        loop_=None,
        client_address=None,
        advertised_ip=None,
    ):
        self.loop = loop_ or asyncio.get_event_loop()
        self.state_updater = None
        self.started = False
        self.network_interface = None
        self.logger = logging.getLogger("buspro.log")
        self.telegram_logger = logging.getLogger("buspro.telegram")

        self.callback_all_messages = None
        self._telegram_received_cbs = []
        self._telegram_received_cbs_by_addr = {}
        self._diagnostics = None  # Optional DiagnosticCapture instance

        self.gateway_address_send_receive = gateway_address_send_receive
        if client_address is None:
            raise ValueError("Buspro client_address is required")
        self.client_address = tuple(client_address)
        self.advertised_ip = advertised_ip

    # Cleanup is explicit via stop(); relying on __del__ + run_until_complete
    # is invalid on a running event loop and would raise on interpreter exit.

    # noinspection PyUnusedLocal
    async def start(self, state_updater=False):  # , daemon_mode=False):
        self.network_interface = NetworkInterface(self, self.gateway_address_send_receive)
        self.network_interface.register_callback(self._callback_all_messages)
        await self.network_interface.start()
        self.started = True

    async def stop(self):
        await self._stop_network_interface()
        self.started = False

    def _callback_all_messages(self, telegram):
        if telegram is None:
            return

        if self.telegram_logger.isEnabledFor(logging.DEBUG):
            self.telegram_logger.debug(telegram)

        # Record to diagnostics (determine direction by address matching)
        if self._diagnostics is not None:
            from .diagnostics import Direction
            direction = Direction.RESPONSE  # Default
            if telegram.target_address == self.client_address:
                direction = Direction.REQUEST
            self._record_telegram(telegram, direction)

        if self.callback_all_messages is not None:
            self.callback_all_messages(telegram)

        addresses = {self._addr_key(telegram.target_address), self._addr_key(telegram.source_address)}
        for address in addresses:
            # Snapshot the bucket: a callback may register/unregister devices,
            # which would otherwise mutate the list mid-iteration.
            for telegram_received_cb in tuple(self._telegram_received_cbs_by_addr.get(address, ())):
                # Isolate each device: a malformed telegram raising in one
                # callback must not starve every other device on this address.
                try:
                    postfix = telegram_received_cb['postfix']
                    if postfix is not None:
                        telegram_received_cb['callback'](telegram, postfix)
                    else:
                        telegram_received_cb['callback'](telegram)
                except Exception:
                    self.logger.exception("Error in telegram callback for %s", address)

    @staticmethod
    def _addr_key(device_address):
        return tuple(device_address) if device_address is not None else None

    async def _stop_network_interface(self):
        if self.network_interface is not None:
            await self.network_interface.stop()
            self.network_interface = None

    def register_telegram_received_all_messages_cb(self, telegram_received_cb):
        self.callback_all_messages = telegram_received_cb

    def register_telegram_received_device_cb(self, telegram_received_cb, device_address, postfix=None):
        entry = {
            'callback': telegram_received_cb,
            'device_address': device_address,
            'postfix': postfix}
        self._telegram_received_cbs.append(entry)
        self._telegram_received_cbs_by_addr.setdefault(self._addr_key(device_address), []).append(entry)

    def unregister_telegram_received_device_cb(self, telegram_received_cb, device_address, postfix=None):
        entry = {
            'callback': telegram_received_cb,
            'device_address': device_address,
            'postfix': postfix}
        self._telegram_received_cbs.remove(entry)
        key = self._addr_key(device_address)
        bucket = self._telegram_received_cbs_by_addr.get(key)
        if bucket is not None:
            bucket.remove(entry)
            if not bucket:
                del self._telegram_received_cbs_by_addr[key]

    def set_diagnostics(self, diagnostic_capture):
        """Attach a diagnostic capture instance."""
        self._diagnostics = diagnostic_capture

    def _record_telegram(self, telegram, direction):
        """Record telegram to diagnostics if enabled."""
        if self._diagnostics is not None:
            self._diagnostics.record_telegram(telegram, direction)
