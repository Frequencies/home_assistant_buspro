"""Base class for device-specific decoders."""

from abc import ABC, abstractmethod
from typing import Any, Dict, List


class DeviceTypeDecoder(ABC):
    """Base class for device-specific decoders."""

    @abstractmethod
    def can_decode(self, operate_code: Any, payload: List[int]) -> bool:
        """Check if this decoder handles the opcode."""
        pass

    @abstractmethod
    def decode_payload(self, operate_code: Any, payload: List[int]) -> Dict[str, Any]:
        """Decode opcode and payload into readable fields."""
        pass
