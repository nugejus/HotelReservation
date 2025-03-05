from Model.RoomType import RoomType
from typing import *

class Room:
    """
    Represents a hotel room with a specific room type, price, and occupancy schedule.
    """

    # Class-level dictionaries for room prices and display names, keyed by RoomType.
    prices = {
        RoomType.LUX: 120,
        RoomType.HALF_LUX: 100,
        RoomType.SINGLE: 70,
        RoomType.SIMPLE_DOUBLE: 80,
        RoomType.DOUBLE_WITH_SOFA: 90
    }

    names_to_display = {
        RoomType.LUX: "LUX",
        RoomType.HALF_LUX: "Half-LUX",
        RoomType.SINGLE: "SINGLE",
        RoomType.SIMPLE_DOUBLE: "DOUBLE",
        RoomType.DOUBLE_WITH_SOFA: "DOUBLE-SOFA"
    }

    def __init__(self, id: int, room_type: RoomType, days: int) -> None:
        """
        Initializes a Room instance.

        :param id: A unique identifier for the room.
        :param room_type: An instance of RoomType specifying the type of the room.
        :param days: The total number of days to track occupancy for this room.
        """
        self.id = id                          # Unique identifier for the room.
        self.type = room_type                 # The room's type.
        # If the room is valid (i.e., not marked as NOT_A_ROOM), set its price and initialize its occupancy schedule.
        if self.type != RoomType.NOT_A_ROOM:
            self.price = Room.prices[room_type]
            # occupancyDuration is a list of booleans indicating occupancy status for each day (True if occupied, False if free).
            self.occupancyDuration = [False] * days

    # SETTERS
    def checkIn(self, checkInDate: int, checkOutDate: int) -> Self:
        """
        Marks the room as occupied from checkInDate up to (but not including) checkOutDate.

        :param checkInDate: The starting day index for the stay.
        :param checkOutDate: The ending day index (non-inclusive) for the stay.
        :return: The current Room instance (allows for method chaining if desired).
        """
        for i in range(checkInDate, checkOutDate):
            self.occupancyDuration[i] = True
        return self

    # GETTERS
    def isAvailable(self, checkInDate: int, checkOutDate: int) -> bool:
        """
        Checks if the room is available (i.e., not occupied) for every day in the specified range.

        :param checkInDate: The starting day index (inclusive).
        :param checkOutDate: The ending day index (non-inclusive).
        :return: True if the room is valid and none of the days in the range are occupied; otherwise, False.
        """
        return (self.type != RoomType.NOT_A_ROOM and 
                not any(self.occupancyDuration[checkInDate:checkOutDate]))

    def isRoom(self) -> bool:
        """
        Determines if this object represents a valid room (not a dummy room).

        :return: True if the room is valid; False otherwise.
        """
        return self.type != RoomType.NOT_A_ROOM

    def isOccupied(self, today: int) -> bool:
        """
        Checks if the room is occupied on a given day.

        :param today: The day index to check occupancy.
        :return: True if the room is occupied on that day; otherwise, False.
        """
        # Debugging code (commented out): print([("0" if b else "_") for b in self.occupancyDuration])
        return self.occupancyDuration[today]

    def get_type(self) -> RoomType:
        """
        Returns the RoomType of this room.

        :return: The room's type.
        """
        return self.type

    def get_price(self, checkInDate: int, checkOutDate: int) -> int:
        """
        Calculates the total price for a stay over the specified date range.

        :param checkInDate: The starting day index (inclusive).
        :param checkOutDate: The ending day index (non-inclusive).
        :return: The total price computed as room price multiplied by the number of days.
        """
        return self.price * (checkOutDate - checkInDate)

    def get_id(self) -> int:
        """
        Returns the unique identifier of this room.

        :return: The room's ID.
        """
        return self.id

    def get_type_name(self) -> str:
        """
        Provides a human-readable display name for the room type (e.g., 'Люкс').

        :return: A string representing the room's type.
        """
        return Room.names_to_display[self.type]
