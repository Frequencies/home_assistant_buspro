"""Shared helpers for Buspro integration."""

from .entity import (
    address_key,
    attach_entity_to_physical_device,
    build_device_info,
    channel_number_from_unique_id,
    device_info_for_address,
    parse_device_address,
    registry_device_definitions,
    registry_device_metadata,
)
from .network import local_ip_for_gateway
from .dimmer import dimmer_diagnostic_definitions
from .logic_controller import (
    LOGIC_CONTROLLER_MODEL,
    logic_controller_coordinator,
    logic_controller_definitions,
)
