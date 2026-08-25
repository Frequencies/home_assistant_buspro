"""Climate control devices with optional command confirmation.

This module provides FloorHeating and PanelAC devices with confirmation
capability for temperature and mode changes. Confirmation is especially
useful for climate systems where state changes are critical.

Configuration:

    # Floor heating with confirmation
    floor_heat = FloorHeating(
        hdl,
        (1, 90),
        name="Bedroom Floor Heat",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    if await floor_heat.set_mode_with_confirmation(TemperatureMode.Heating):
        print("Floor heat mode confirmed")

    # Panel AC with confirmation
    ac = PanelAC(
        hdl,
        (1, 100),
        name="Living Room AC",
        enable_confirmation=True,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    )

    if await ac.turn_on_with_confirmation():
        print("AC turned on with confirmation")
"""

import asyncio
import struct
from .confirmable import ConfirmableDevice
from .control import (
    _ReadFloorHeatingStatus,
    _ControlFloorHeatingStatus,
    _ReadFloorHeatingModuleStatus,
    _ControlFloorHeatingModuleStatus,
    _ReadFloorHeatingTemperatureNew,
    _ReadFloorHeatingTemperatureLegacy,
    _ReadPanelAC,
    _ControlPanelAC,
)
from .device import Device, startup_read_delay
from ..helpers.enums import (
    OperateCode,
    SuccessOrFailure,
    TemperatureType,
    TemperatureMode,
    WorkType,
    FloorHeatingDeviceType,
)

_WORK_TYPE_VALUES = frozenset(w.value for w in WorkType)


class ControlFloorHeatingStatus:
    """Container for floor heating control parameters."""

    def __init__(self):
        self.temperature_type = None
        self.status = None
        self.mode = None
        self.normal_temperature = None
        self.day_temperature = None
        self.night_temperature = None
        self.away_temperature = None
        self.work_type = None


class ControlPanelACStatus:
    """Container for panel AC control parameters."""

    def __init__(self):
        self.status = None
        self.mode = None
        self.normal_temperature = None


class FloorHeating(ConfirmableDevice, Device):
    """Floor heating module with optional confirmation."""

    def __init__(
        self,
        buspro,
        device_address,
        name="",
        channel_number=None,
        device_type=FloorHeatingDeviceType.DLP,
        enable_confirmation=False,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    ):
        """
        Initialize floor heating with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            name: Human-readable name.
            channel_number: Optional channel number.
            device_type: FloorHeatingDeviceType enum.
            enable_confirmation: Enable confirmation waiting.
            confirmation_timeout: Seconds to wait for response.
            confirmation_retries: Retry attempts on timeout.
        """
        # Initialize ConfirmableDevice first
        ConfirmableDevice.__init__(
            self,
            enable_confirmation=enable_confirmation,
            confirmation_timeout=confirmation_timeout,
            confirmation_retries=confirmation_retries,
        )

        # Initialize Device
        Device.__init__(self, buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address
        self._channel_number = channel_number
        self._device_type = device_type

        self._temperature_type = None
        self._status = None
        self._mode = None
        self._current_temperature = None
        self._normal_temperature = None
        self._day_temperature = None
        self._night_temperature = None
        self._away_temperature = None
        self._work_type = WorkType.Heating
        self._valve = None
        self._watering_time = None
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_status(run_from_init=True)

    def close(self):
        """Detach from the bus and cancel pending tasks."""
        if self._closed:
            return
        self._closed = True
        self._cleanup_confirmation_state()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams."""
        if telegram.operate_code == OperateCode.ReadFloorHeatingStatusResponse:
            if len(telegram.payload) < 8:
                return

            self._temperature_type = telegram.payload[0]
            self._status = telegram.payload[1]
            self._mode = telegram.payload[2]
            self._current_temperature = telegram.payload[3]
            self._normal_temperature = telegram.payload[4]
            self._day_temperature = telegram.payload[5]
            self._night_temperature = telegram.payload[6]
            self._away_temperature = telegram.payload[7]
            self._call_device_updated()

            # Mark confirmations
            self.mark_confirmed("floor_heating_mode")
            self.mark_confirmed("floor_heating_temperature")

        elif telegram.operate_code == OperateCode.ControlFloorHeatingStatusResponse:
            self._call_read_current_status()

    async def read_status(self):
        """Request current floor heating status."""
        req = _ReadFloorHeatingStatus(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        if self._channel_number is not None:
            req.channel_number = self._channel_number
        await req.send()

    async def control_status(self, control: ControlFloorHeatingStatus):
        """Send floor heating control command."""
        req = _ControlFloorHeatingStatus(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        if self._channel_number is not None:
            req.channel_number = self._channel_number
        if control.temperature_type is not None:
            req.temperature_type = control.temperature_type
        if control.status is not None:
            req.status = control.status
        if control.mode is not None:
            req.mode = control.mode
        if control.normal_temperature is not None:
            req.normal_temperature = control.normal_temperature
        if control.day_temperature is not None:
            req.day_temperature = control.day_temperature
        if control.night_temperature is not None:
            req.night_temperature = control.night_temperature
        if control.away_temperature is not None:
            req.away_temperature = control.away_temperature
        if control.work_type is not None:
            req.work_type = control.work_type
        await req.send()

    # Confirmation-aware methods
    async def set_mode_with_confirmation(self, mode: TemperatureMode) -> bool:
        """
        Set heating mode with confirmation.

        Args:
            mode: TemperatureMode enum value.

        Returns:
            True if confirmed or confirmation disabled.
        """

        async def _send():
            control = ControlFloorHeatingStatus()
            control.mode = mode
            await self.control_status(control)

        return await self.send_and_confirm(
            command_id="floor_heating_mode",
            command_fn=_send,
        )

    async def set_temperature_with_confirmation(self, temperature: float) -> bool:
        """
        Set target temperature with confirmation.

        Args:
            temperature: Target temperature in celsius.

        Returns:
            True if confirmed or confirmation disabled.
        """

        async def _send():
            control = ControlFloorHeatingStatus()
            control.normal_temperature = temperature
            await self.control_status(control)

        success = await self.send_and_confirm(
            command_id="floor_heating_temperature",
            command_fn=_send,
        )

        if success:
            self._normal_temperature = temperature
            self._call_device_updated()
        return success

    def _call_read_current_status(self, run_from_init=False):
        """Schedule a status read."""

        async def read_current_status():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_status())

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}"

    @property
    def is_on(self):
        """Return True if heating is active."""
        return self._status == 1

    @property
    def mode(self):
        """Get current heating mode."""
        return self._mode

    @property
    def temperature(self):
        """Get current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Get target temperature."""
        return self._normal_temperature


class PanelAC(ConfirmableDevice, Device):
    """Panel AC unit with optional confirmation."""

    def __init__(
        self,
        buspro,
        device_address,
        name="",
        enable_confirmation=False,
        confirmation_timeout=5.0,
        confirmation_retries=3,
    ):
        """
        Initialize panel AC with confirmation support.

        Args:
            buspro: Buspro connection.
            device_address: (subnet, device) tuple.
            name: Human-readable name.
            enable_confirmation: Enable confirmation waiting.
            confirmation_timeout: Seconds to wait for response.
            confirmation_retries: Retry attempts on timeout.
        """
        # Initialize ConfirmableDevice first
        ConfirmableDevice.__init__(
            self,
            enable_confirmation=enable_confirmation,
            confirmation_timeout=confirmation_timeout,
            confirmation_retries=confirmation_retries,
        )

        # Initialize Device
        Device.__init__(self, buspro, device_address, name)

        self._buspro = buspro
        self._device_address = device_address

        self._status = None
        self._mode = None
        self._current_temperature = None
        self._normal_temperature = None
        self._closed = False

        self.register_telegram_received_cb(self._telegram_received_cb)
        self._call_read_current_panel_status(run_from_init=True)
        self._call_read_current_panel_temp(run_from_init=True)

    def close(self):
        """Detach from the bus and cancel pending tasks."""
        if self._closed:
            return
        self._closed = True
        self._cleanup_confirmation_state()
        super().close()
        try:
            self.unregister_telegram_received_cb(self._telegram_received_cb)
        except ValueError:
            pass

    def _telegram_received_cb(self, telegram):
        """Handle incoming telegrams."""
        if telegram.operate_code in (
            OperateCode.ReadPanelACResponse,
            OperateCode.ControlPanelACResponse,
        ):
            if len(telegram.payload) < 2:
                return
            command = telegram.payload[0]
            value = telegram.payload[1]

            if command == 3:
                self._status = value
                self._mode = value
                self._call_device_updated()
                self.mark_confirmed("panel_ac_mode")

            elif command == 4:
                self._current_temperature = value
                self._normal_temperature = value
                self._call_device_updated()
                self.mark_confirmed("panel_ac_temperature")

        elif telegram.operate_code == OperateCode.BroadcastTemperatureResponse:
            if len(telegram.payload) >= 2:
                self._current_temperature = telegram.payload[1]
                self._call_device_updated()

    async def read_status(self):
        """Request current AC status."""
        req = _ReadPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 3
        await req.send()

    async def read_temperature(self):
        """Request current temperature."""
        req = _ReadPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 4
        await req.send()

    async def control_ac_status(self, control: ControlPanelACStatus):
        """Send AC status control."""
        req = _ControlPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 3
        req.mode = (
            control.status if control.status is not None else control.mode
        )
        await req.send()

    async def control_ac_temperature(self, control: ControlPanelACStatus):
        """Send AC temperature control."""
        req = _ControlPanelAC(self._buspro)
        req.subnet_id, req.device_id = self._device_address
        req.command = 4
        req.mode = control.normal_temperature
        await req.send()

    # Confirmation-aware methods
    async def turn_on_with_confirmation(self) -> bool:
        """
        Turn AC on with confirmation.

        Returns:
            True if confirmed or confirmation disabled.
        """

        async def _send():
            control = ControlPanelACStatus()
            control.status = 1
            await self.control_ac_status(control)

        success = await self.send_and_confirm(
            command_id="panel_ac_mode",
            command_fn=_send,
        )

        if success:
            self._status = 1
            self._call_device_updated()
        return success

    async def turn_off_with_confirmation(self) -> bool:
        """
        Turn AC off with confirmation.

        Returns:
            True if confirmed or confirmation disabled.
        """

        async def _send():
            control = ControlPanelACStatus()
            control.status = 0
            await self.control_ac_status(control)

        success = await self.send_and_confirm(
            command_id="panel_ac_mode",
            command_fn=_send,
        )

        if success:
            self._status = 0
            self._call_device_updated()
        return success

    async def set_mode_with_confirmation(self, mode) -> bool:
        """Set AC mode with confirmation."""

        async def _send():
            control = ControlPanelACStatus()
            control.mode = mode
            await self.control_ac_status(control)

        return await self.send_and_confirm(
            command_id="panel_ac_mode",
            command_fn=_send,
        )

    async def set_temperature_with_confirmation(self, temperature: float) -> bool:
        """
        Set target temperature with confirmation.

        Args:
            temperature: Target temperature in celsius.

        Returns:
            True if confirmed or confirmation disabled.
        """

        async def _send():
            control = ControlPanelACStatus()
            control.normal_temperature = temperature
            await self.control_ac_temperature(control)

        success = await self.send_and_confirm(
            command_id="panel_ac_temperature",
            command_fn=_send,
        )

        if success:
            self._normal_temperature = temperature
            self._call_device_updated()
        return success

    def _call_read_current_panel_status(self, run_from_init=False):
        """Schedule a status read."""

        async def read_current_panel_status():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_status()

        self._spawn(read_current_panel_status())

    def _call_read_current_panel_temp(self, run_from_init=False):
        """Schedule a temperature read."""

        async def read_current_panel_temp():
            if run_from_init:
                await asyncio.sleep(startup_read_delay(self._device_address, base=5))
            await self.read_temperature()

        self._spawn(read_current_panel_temp())

    @property
    def is_on(self):
        """Return True if AC is on."""
        return self._status == 1

    @property
    def mode(self):
        """Get current AC mode."""
        return self._mode

    @property
    def temperature(self):
        """Get current temperature."""
        return self._current_temperature

    @property
    def target_temperature(self):
        """Get target temperature."""
        return self._normal_temperature

    @property
    def device_identifier(self):
        """Return device identifier."""
        return f"{self._device_address}"
