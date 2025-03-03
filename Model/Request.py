from RoomType import RoomType
from typing import *

class Request:
    """
    Represents a request for a hotel room, including the desired room type
    and check-in/check-out dates.
    """
    names_to_display = {
        RoomType.LUX: "Люкс",
        RoomType.HALF_LUX: "Полу-Люкс",
        RoomType.SINGLE: "Одна кровать",
        RoomType.SIMPLE_DOUBLE: "Две кровати",
        RoomType.DOUBLE_WITH_SOFA: "Две кровати с диваном"
    }
    
    def __init__(self, roomType: RoomType, checkInDate: int, checkOutDate: int):
        """
        Initializes a new Request.

        :param roomType: The desired RoomType.
        :param checkInDate: The day index (inclusive) when the stay begins.
        :param checkOutDate: The day index (non-inclusive) when the stay ends.
        """
        self.roomType = roomType
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
    
    # GETTERS
    def get_time_info(self) -> Tuple[int, int]:
        """
        Returns the tuple (checkInDate, checkOutDate) for this request.
        """
        return self.checkInDate, self.checkOutDate
    
    def get_room_name(self) -> str:
        """
        Returns a human-readable string for the requested room type 
        (e.g., 'Люкс' for RoomType.LUX).
        """
        return Request.names_to_display[self.roomType]
    
    def get_request_info(self) -> Tuple[RoomType, int, int]:
        """
        Returns a tuple of (roomType, checkInDate, checkOutDate).
        """
        return self.roomType, self.checkInDate, self.checkOutDate
    
    def isRequest(self) -> bool:
        """
        Checks if the request is a valid room request (i.e., not 'NOT_A_ROOM').

        :return: True if it's a valid room request; otherwise False.
        """
        return self.roomType != RoomType.NOT_A_ROOM
