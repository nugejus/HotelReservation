from Room import Room
from RoomType import RoomType

from collections import defaultdict
from typing import *
from Request import Request

class Hotel:
    """
    Represents a hotel which manages a collection of Room objects and processes room requests.
    """

    def __init__(self, rooms_info : Dict[RoomType, int], days : int) -> None:
        """
        Initializes the Hotel with a given dictionary of room information 
        and the total number of days for which occupancy is tracked.

        :param rooms_info: A dictionary where the key is a RoomType and the value is 
                           the count of rooms of that type.
        :param days: The total number of days for which occupancy data is maintained.
        """
        self.rooms = []
        self.rooms_info = rooms_info
        
        c = 0
        # For each room type and its count, create Room objects and store them in the list.
        for room_type, numbers in rooms_info.items():
            for i in range(c, c + numbers):
                self.rooms.append(Room(i, room_type, days))
            # Increase the index counter by the number of rooms + 1 
            # (likely to ensure IDs don't overlap or for spacing).
            c = c + numbers + 1

    def _processRequest(self, req: Request) -> Room:
        """
        A helper method to process an individual room request.
        Attempts to find an available room of the requested type and date range,
        otherwise returns a 'NOT_A_ROOM' placeholder.

        :param req: A request object providing (roomType, checkInDate, checkOutDate).
        :return: The Room object if found; otherwise a dummy Room (NOT_A_ROOM).
        """
        roomType, checkInDate, checkOutDate = req.get_request_info()
        room = self.checkAvailability(roomType, checkInDate, checkOutDate)
        
        if room:
            return room.checkIn(checkInDate, checkOutDate)
        else:
            # If no suitable room is found, return a dummy 'NOT_A_ROOM'
            return Room(-1, RoomType.NOT_A_ROOM, -1)
        
    def processRequests(self, requests : List[Request]) -> List[Room]:
        """
        Processes a list of requests by calling _processRequest on each one.

        :param requests: A list of request objects.
        :return: A list of Room objects (or NOT_A_ROOM placeholders) corresponding 
                 to the processed requests.
        """
        process_results = []
        for request in requests:
            process_results.append(self._processRequest(request))
        return process_results
        
    # GETTERS
    def checkAvailability(self, roomType : RoomType, checkInDate : int, checkOutDate : int) -> None:
        """
        Checks if there's an available room matching the requested room type and date range.
        If no exact match is found, it looks for an upgraded room type (larger than requested).

        :param roomType: The requested RoomType.
        :param checkInDate: The start day index (inclusive).
        :param checkOutDate: The end day index (non-inclusive).
        :return: A Room object if available; otherwise None.
        """
        # First, try to find a room of the exact requested type.
        for room in self.rooms:
            if room.get_type() == roomType and room.isAvailable(checkInDate, checkOutDate):
                return room
        
        # If none is found, provide an upgraded room if possible.
        for room in self.rooms:
            if room.get_type() > roomType and room.isAvailable(checkInDate, checkOutDate):
                return room
        
        return None
        
    def get_room_numbers(self) -> int:
        """
        Returns the total number of Room objects in the hotel.
        """
        return len(self.rooms)
    
    def get_current_occupancy(self, today : int) -> int:
        """
        Counts how many rooms are occupied on a particular day.

        :param today: The day index for occupancy checking.
        :return: The number of occupied rooms.
        """
        current_occupancy = 0
        for room in self.rooms:
            current_occupancy += not room.isFree(today)
        return current_occupancy
    
    def getTodayOccupancy(self, today : int) -> DefaultDict:
        """
        Returns a dictionary that maps each RoomType to the occupancy count 
        (occupied rooms) for that type on the given day.

        :param today: The day index to check occupancy.
        :return: A defaultdict(int) mapping RoomType -> number of occupied rooms.
        """
        occupancy = defaultdict(int)
        
        for room in self.rooms:
            occupancy[room.type] += not room.isFree(today)
        
        return occupancy
    
    def get_room_info(self) -> Dict[RoomType, int]:
        """
        Returns the original dictionary (rooms_info) that was used to set up the hotel.
        """
        return self.rooms_info
