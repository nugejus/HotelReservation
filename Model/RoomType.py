from enum import Enum
from typing import Self

class RoomType(Enum):
    """
    An enumeration for the different types of rooms in the system.
    Each enum member corresponds to a specific type of room,
    with an underlying integer value for comparison or sorting purposes.
    """
    SINGLE = 1
    SIMPLE_DOUBLE = 2
    DOUBLE_WITH_SOFA = 3
    HALF_LUX = 4
    LUX = 5
    NOT_A_ROOM = 6

    def __lt__(self, other: Self) -> bool:
        """
        Overloads the less-than operator (<) for RoomType.
        The comparison checks the integer 'value' field of each Enum member
        if the other object is also a RoomType. If not, it returns NotImplemented,
        allowing Python to handle the comparison with alternative methods.
        """
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented
