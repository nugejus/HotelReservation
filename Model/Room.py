from Model.RoomType import RoomType
from typing import *

class Room:
    """
    Represents a hotel room with a specific room type, price, and occupancy schedule.
    """

    # Class-level dictionaries for room prices and names to display, keyed by RoomType.
    prices = {
        RoomType.LUX: 120,
        RoomType.HALF_LUX: 100,
        RoomType.SINGLE: 70,
        RoomType.SIMPLE_DOUBLE: 80,
        RoomType.DOUBLE_WITH_SOFA: 90
    }

    names_to_display = {
        RoomType.LUX: "Люкс",
        RoomType.HALF_LUX: "Полу-Люкс",
        RoomType.SINGLE: "Одна кровать",
        RoomType.SIMPLE_DOUBLE: "Две кровати",
        RoomType.DOUBLE_WITH_SOFA: "Две кровати с диваном"
    }

    def __init__(self, id : int, room_type : RoomType, days : int) -> None:
        """
        Initializes a Room instance.

        :param id: A unique identifier for the room.
        :param room_type: An instance of RoomType specifying the type of the room.
        :param days: The total number of days to track occupancy for this room.
        """
        self.id = id
        self.type = room_type
        # If the room is valid (not NOT_A_ROOM), set up the price and occupancy tracking.
        if self.type != RoomType.NOT_A_ROOM:
            self.price = Room.prices[room_type]
            # occupancyDuration is a list of booleans indicating occupancy (True) or free (False) for each day.
            self.occupancyDuration = [False] * days

    # SETTERS
    def checkIn(self, checkInDate : int, checkOutDate : int) -> Self:
        """
        Marks the room as occupied from checkInDate to checkOutDate (non-inclusive).

        :param checkInDate: The start day index for checking in.
        :param checkOutDate: The end day index (non-inclusive).
        :return: Returns the current Room instance (for fluent chaining if desired).
        """
        for i in range(checkInDate, checkOutDate):
            self.occupancyDuration[i] = True
        return self

    # GETTERS
    def isAvailable(self, checkInDate : int, checkOutDate : int) -> bool:
        """
        Checks if the room is available (not occupied) throughout a specified range of days.

        :param checkInDate: The start day index (inclusive).
        :param checkOutDate: The end day index (non-inclusive).
        :return: True if it's an actual room (not NOT_A_ROOM) and no days in the range are occupied; otherwise, False.
        """
        return (self.type != RoomType.NOT_A_ROOM 
                and not any(self.occupancyDuration[checkInDate:checkOutDate]))

    def isRoom(self) -> bool:
        """
        Checks if this object is a valid room (i.e., not marked as NOT_A_ROOM).

        :return: True if valid, False otherwise.
        """
        return self.type != RoomType.NOT_A_ROOM

    def isFree(self, today) -> bool:
        """
        Checks if the room is free (not occupied) on a given day.

        :param today: The day index to check occupancy.
        :return: True if the room is free that day; otherwise, False.
        """
        return not self.occupancyDuration[today]

    def get_type(self) -> RoomType:
        """
        Returns the RoomType of this room.
        """
        return self.type

    def get_price(self, checkInDate : int, checkOutDate : int) -> int:
        """
        Calculates the total price for a stay over the specified date range.

        :param checkInDate: The start day index (inclusive).
        :param checkOutDate: The end day index (non-inclusive).
        :return: The calculated total price for the stay.
        """
        return self.price * (checkOutDate - checkInDate)

    def get_id(self) -> int:
        """
        Returns the unique identifier for this room.
        """
        return self.id

    def get_type_name(self) -> str:
        """
        Provides a human-readable string for the room type (e.g., 'Люкс').

        :return: The display name corresponding to the room's type.
        """
        return Room.names_to_display[self.type]
