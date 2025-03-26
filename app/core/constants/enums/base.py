from enum import Enum


class BaseEnum(Enum):
    """
    - Base Enum class

    - methods:
        - choices: list : Return the choices of the enum
        - keys: list : Return the raw keys of the enum
    """

    @classmethod
    def values(cls):
        return [member.value for member in cls]

    @classmethod
    def keys(cls):
        return list(cls.__members__.keys())
