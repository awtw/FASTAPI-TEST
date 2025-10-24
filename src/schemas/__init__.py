from enum import Enum, EnumMeta


class MetaEnum(EnumMeta):
    def __contains__(cls, item):
        try:
            cls(item)
        except ValueError:
            return False
        return True


class CustomStringEnum(str, Enum, metaclass=MetaEnum):
    def __str__(self):
        return self.value