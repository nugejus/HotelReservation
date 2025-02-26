from enum import Enum

class RoomType(Enum):
    SINGLE = 1
    SIMPLE_DOUBLE = 2
    DOUBLE_WITH_SOFA = 3
    HALF_LUX = 4
    LUX = 5

    def __lt__(self, other):
        if self.__class__ is other.__class__:
            return self.value < other.value
        return NotImplemented