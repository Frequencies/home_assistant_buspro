import unittest

from tests.bootstrap import ensure_homeassistant_stubs

ensure_homeassistant_stubs()

from custom_components.buspro.pybuspro.helpers.enums import DeviceType, OperateCode
from custom_components.buspro.pybuspro.helpers.generics import Generics


class GenericsTests(unittest.TestCase):
    def setUp(self):
        self.g = Generics()

    def test_calculate_minutes_seconds(self):
        self.assertEqual(self.g.calculate_minutes_seconds(125), (2, 5))

    def test_integer_hex_roundtrip(self):
        ints = [1, 2, 255]
        as_hex = self.g.integer_list_to_hex(ints)
        self.assertEqual(self.g.hex_to_integer_list(as_hex), ints)

    def test_get_enum_value_known(self):
        self.assertEqual(self.g.get_enum_value(DeviceType, DeviceType.PyBusPro.value), DeviceType.PyBusPro)
        self.assertEqual(
            self.g.get_enum_value(OperateCode, OperateCode.ReadStatusOfChannels.value),
            OperateCode.ReadStatusOfChannels,
        )

    def test_get_enum_value_unknown(self):
        self.assertIsNone(self.g.get_enum_value(DeviceType, b"\x12\x34"))
        self.assertIsNone(self.g.get_enum_value(OperateCode, b"\x12\x34"))


if __name__ == "__main__":
    unittest.main()
