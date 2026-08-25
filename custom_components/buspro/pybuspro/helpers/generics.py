from .enums import DeviceType, OperateCode


class Generics:

    @staticmethod
    def calculate_minutes_seconds(seconds):
        return divmod(seconds, 60)  # (minutes, seconds)

    @staticmethod
    def integer_list_to_hex(list_):
        hex_ = bytearray(list_)
        return hex_

    @staticmethod
    def hex_to_integer_list(hex_value):
        list_of_integer = []
        for string in hex_value:
            list_of_integer.append(string)
        return list_of_integer

    @staticmethod
    def enum_has_value(enum, value):
        return value in enum._value2member_map_

    @staticmethod
    def get_enum_value(enum, value):
        # O(1) reverse lookup on the enum's built-in value map; returns None
        # for unknown values instead of scanning every member per datagram.
        try:
            return enum(value)
        except ValueError:
            return None
