from Model.RoomType import RoomType
from typing import *

class Request:
    """
    Represents a request for a hotel room, including the desired room type and the check-in/check-out dates.
    """

    # A mapping from RoomType values to their human-readable display strings.
    names_to_display = {
        RoomType.LUX: "LUX",
        RoomType.HALF_LUX: "Half-LUX",
        RoomType.SINGLE: "SINGLE",
        RoomType.SIMPLE_DOUBLE: "DOUBLE",
        RoomType.DOUBLE_WITH_SOFA: "DOUBLE-SOFA"
    }
    
    def __init__(self, roomType: RoomType, checkInDate: int, checkOutDate: int):
        """
        Initializes a new Request object with the specified room type and date range.
        
        :param roomType: The desired RoomType for the request.
        :param checkInDate: The starting day index (inclusive) for the stay.
        :param checkOutDate: The ending day index (non-inclusive) for the stay.
        """
        self.roomType = roomType            # The requested type of room.
        self.checkInDate = checkInDate      # The day index when the stay begins.
        self.checkOutDate = checkOutDate    # The day index when the stay ends.
    
    # GETTERS
    def get_time_info(self) -> Tuple[int, int]:
        """
        Returns the check-in and check-out dates as a tuple.
        
        :return: A tuple (checkInDate, checkOutDate) representing the period of the stay.
        """
        return self.checkInDate, self.checkOutDate
    
    def get_room_name(self) -> str:
        """
        Returns a human-readable string representing the requested room type.
        (e.g., 'LUX' for RoomType.LUX)
        
        :return: A string that describes the room type.
        """
        return Request.names_to_display[self.roomType]
    
    def get_request_info(self) -> Tuple[RoomType, int, int]:
        """
        Returns all request details including room type, check-in date, and check-out date.
        
        :return: A tuple (roomType, checkInDate, checkOutDate).
        """
        return self.roomType, self.checkInDate, self.checkOutDate
    
    def isRequest(self) -> bool:
        """
        Determines if this Request is valid (i.e., not a dummy request with RoomType.NOT_A_ROOM).
        
        :return: True if the request is valid; otherwise, False.
        """
        return self.roomType != RoomType.NOT_A_ROOM
