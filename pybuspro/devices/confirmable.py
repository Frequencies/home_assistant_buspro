"""Confirmation state pattern mixin for command acknowledgment.

This module provides the ConfirmableDevice mixin that enables optional
command confirmation for any device. When enabled, devices wait for a
response telegram confirming the command was received and executed.

When disabled (default), devices use the traditional fire-and-forget
pattern for backward compatibility and minimal overhead.

Configuration:
    enable_confirmation (bool): Enable confirmation mode. Default False.
    confirmation_timeout (float): Seconds to wait for response. Default 5.0.
    confirmation_retries (int): Retry attempts on timeout. Default 3.

Example usage:

    # Fire-and-forget (default)
    relay = RelayChannel(buspro, (1, 50), 1, enable_confirmation=False)
    await relay.set_on()

    # Confirmation mode with retries
    relay = RelayChannel(
        buspro, (1, 50), 1,
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3
    )
    success = await relay.set_on_with_confirmation()
    if not success:
        _LOGGER.error("Failed to turn on relay after retries")
"""

import asyncio
import logging
from typing import Callable, Optional

_LOGGER = logging.getLogger(__name__)


class ConfirmationState:
    """Holds state for a pending confirmation."""

    def __init__(self):
        """Initialize confirmation state."""
        self.event = asyncio.Event()
        self.confirmed = False


class ConfirmableDevice:
    """
    Mixin providing command confirmation capability.

    Devices that inherit from this can optionally wait for confirmation
    responses before considering a command successful. When disabled,
    behaves identically to the base Device (fire-and-forget).

    This mixin must be used with multiple inheritance along with Device:

        class MyDevice(ConfirmableDevice, Device):
            def __init__(self, buspro, address, enable_confirmation=False, **kwargs):
                ConfirmableDevice.__init__(
                    self,
                    enable_confirmation=enable_confirmation,
                    confirmation_timeout=kwargs.pop('confirmation_timeout', 5.0),
                    confirmation_retries=kwargs.pop('confirmation_retries', 3),
                )
                Device.__init__(self, buspro, address, **kwargs)
    """

    def __init__(
        self,
        enable_confirmation: bool = False,
        confirmation_timeout: float = 5.0,
        confirmation_retries: int = 3,
    ):
        """
        Initialize confirmation parameters.

        Args:
            enable_confirmation: Enable confirmation waiting. Default False.
            confirmation_timeout: Seconds to wait for response. Default 5.0.
            confirmation_retries: Retry attempts on timeout. Default 3.
        """
        self.enable_confirmation = bool(enable_confirmation)
        self.confirmation_timeout = max(0.1, float(confirmation_timeout))
        self.confirmation_retries = max(0, int(confirmation_retries))

        # Per-command confirmation state (command_id -> ConfirmationState)
        self._confirmation_states: dict[str, ConfirmationState] = {}
        self._confirmation_lock = asyncio.Lock()

        _LOGGER.debug(
            "%s confirmation enabled=%s timeout=%.1fs retries=%d",
            self.__class__.__name__,
            self.enable_confirmation,
            self.confirmation_timeout,
            self.confirmation_retries,
        )

    async def send_and_confirm(
        self,
        command_id: str,
        command_fn: Callable,
        verify_fn: Optional[Callable] = None,
        timeout: Optional[float] = None,
        retries: Optional[int] = None,
    ) -> bool:
        """
        Send a command and optionally wait for confirmation.

        If confirmation is disabled, sends the command and returns True
        (assuming success). If enabled, waits for a confirmation response
        with automatic retry on timeout.

        Args:
            command_id: Unique ID for this command (e.g., "relay_1_on").
                        Used to match responses. Should be the same ID
                        passed to mark_confirmed() in the callback.
            command_fn: Async callable that sends the command.
            verify_fn: Optional async callable to verify state changed.
                       Receives (self) and should return bool.
            timeout: Override default confirmation_timeout (seconds).
            retries: Override default confirmation_retries (attempts).

        Returns:
            True if command succeeded or confirmation disabled.
            False if command timed out or failed after all retries.

        Example:

            async def send_command():
                await self._module.async_set_channel(self._channel, 100)

            success = await self.send_and_confirm(
                command_id="relay_1_on",
                command_fn=send_command
            )
        """
        if not self.enable_confirmation:
            # Fire-and-forget mode: send and assume success
            try:
                await command_fn()
                _LOGGER.debug(
                    "%s command %s sent (confirmation disabled)",
                    self.__class__.__name__,
                    command_id,
                )
                return True
            except Exception as e:
                _LOGGER.error(
                    "%s command %s failed: %s",
                    self.__class__.__name__,
                    command_id,
                    e,
                )
                return False

        # Confirmation mode: send, wait, retry on timeout
        timeout = timeout or self.confirmation_timeout
        retries = retries or self.confirmation_retries
        attempts = 0

        while attempts <= retries:
            attempts += 1
            try:
                _LOGGER.debug(
                    "%s command %s sending (attempt %d/%d)",
                    self.__class__.__name__,
                    command_id,
                    attempts,
                    retries + 1,
                )

                # Send the command
                await command_fn()

                # Wait for confirmation
                confirmed = await self._wait_for_confirmation(
                    command_id, timeout, verify_fn
                )

                if confirmed:
                    _LOGGER.debug(
                        "%s command %s confirmed on attempt %d",
                        self.__class__.__name__,
                        command_id,
                        attempts,
                    )
                    return True

                if attempts > retries:
                    _LOGGER.warning(
                        "%s command %s failed after %d attempts",
                        self.__class__.__name__,
                        command_id,
                        attempts,
                    )
                    return False

                # Retry with exponential backoff (25ms, 50ms, 100ms, ...)
                backoff = 0.025 * (2 ** (attempts - 1))
                _LOGGER.debug(
                    "%s retrying %s after %.3fs",
                    self.__class__.__name__,
                    command_id,
                    backoff,
                )
                await asyncio.sleep(backoff)

            except asyncio.TimeoutError:
                if attempts > retries:
                    _LOGGER.warning(
                        "%s command %s timed out after %d attempts",
                        self.__class__.__name__,
                        command_id,
                        attempts,
                    )
                    return False
                _LOGGER.debug(
                    "%s command %s attempt %d timed out, retrying",
                    self.__class__.__name__,
                    command_id,
                    attempts,
                )

            except Exception as e:
                _LOGGER.error(
                    "%s command %s error: %s",
                    self.__class__.__name__,
                    command_id,
                    e,
                )
                return False

        return False

    async def _wait_for_confirmation(
        self,
        command_id: str,
        timeout: float,
        verify_fn: Optional[Callable] = None,
    ) -> bool:
        """
        Wait for a confirmation response with timeout.

        Args:
            command_id: Command to wait for.
            timeout: Timeout in seconds.
            verify_fn: Optional callable to verify state changed.

        Returns:
            True if confirmed, False if timeout.
        """
        async with self._confirmation_lock:
            if command_id not in self._confirmation_states:
                self._confirmation_states[command_id] = ConfirmationState()

            state = self._confirmation_states[command_id]
            state.event.clear()

        try:
            # Wait for either confirmation event or timeout
            await asyncio.wait_for(state.event.wait(), timeout)

            # Event set means confirmation received
            confirmed = state.confirmed

            # Optional verification callback
            if confirmed and verify_fn is not None:
                try:
                    confirmed = await verify_fn(self)
                except Exception as e:
                    _LOGGER.error(
                        "%s verification failed for %s: %s",
                        self.__class__.__name__,
                        command_id,
                        e,
                    )
                    confirmed = False

            return confirmed

        except asyncio.TimeoutError:
            _LOGGER.debug(
                "%s confirmation timeout for %s (>%.1fs)",
                self.__class__.__name__,
                command_id,
                timeout,
            )
            return False
        finally:
            # Clean up state
            async with self._confirmation_lock:
                self._confirmation_states.pop(command_id, None)

    def mark_confirmed(self, command_id: str):
        """
        Mark a command as confirmed.

        Call this from your telegram receive callback when you get
        a response confirming the command was executed.

        Args:
            command_id: The command ID to mark confirmed.
                        Must match the command_id passed to send_and_confirm().

        Example (in telegram callback):

            def _telegram_received_cb(self, telegram):
                if telegram.operate_code == OperateCode.SingleChannelControlResponse:
                    channel = telegram.payload[0]
                    if channel == self._channel:
                        self.mark_confirmed("relay_on")
        """
        async def _mark():
            async with self._confirmation_lock:
                if command_id in self._confirmation_states:
                    state = self._confirmation_states[command_id]
                    state.confirmed = True
                    state.event.set()
                    _LOGGER.debug(
                        "%s marked %s as confirmed",
                        self.__class__.__name__,
                        command_id,
                    )

        # Schedule async marking (may be called from sync context)
        if hasattr(self, "_buspro") and hasattr(self._buspro, "loop"):
            asyncio.ensure_future(_mark(), loop=self._buspro.loop)

    def _cleanup_confirmation_state(self):
        """Clean up all pending confirmation states (on device close)."""
        for state in self._confirmation_states.values():
            state.event.set()
        self._confirmation_states.clear()
