"""Data models for diagnostic system."""

from dataclasses import dataclass
from typing import Optional, Dict, Any, List
from enum import Enum


class Direction(Enum):
    """Direction of telegram flow."""
    REQUEST = "request"
    RESPONSE = "response"
    BROADCAST = "broadcast"


@dataclass
class TelegramRecord:
    """Single captured telegram with metadata."""
    timestamp: str
    direction: Direction
    source_address: tuple
    source_alias: Optional[str]
    target_address: tuple
    target_alias: Optional[str]
    operate_code: str
    operate_code_name: Optional[str]
    operate_code_enum: Optional[str]
    payload: List[int]
    payload_size: int
    crc: Optional[str]
    decoded: Optional[Dict[str, Any]] = None
    device_type_hint: Optional[str] = None
