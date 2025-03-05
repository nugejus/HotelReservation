from Model.Room import Room
from Model.Request import Request
from Model.RoomType import RoomType

from collections import defaultdict
from typing import *

class Hotel:
    """
    Represents a hotel that manages a collection of Room objects and processes room requests.
    """

    def __init__(self, rooms_info: Dict[RoomType, int], days: int) -> None:
        """
        Initializes the Hotel with room configuration and the total number of days for tracking occupancy.

        :param rooms_info: A dictionary mapping each RoomType to the count of rooms of that type.
        :param days: The total number of days for which occupancy data is maintained.
        """
        self.rooms = []            # List to store Room objects.
        self.rooms_info = rooms_info
        
        c = 0
        # Create Room objects for each room type based on the provided counts.
        # The variable 'c' is used as a starting ID for each room. After processing one type,
        # it is incremented by the number of rooms created plus one to leave a gap between IDs.
        for room_type, numbers in rooms_info.items():
            for i in range(c, c + numbers):
                self.rooms.append(Room(i, room_type, days))
            c = c + numbers + 1  # Update the room ID counter with an extra gap.

    def _processRequest(self, req: Request) -> Room:
        """
        Processes a single room request.
        It attempts to find an available room of the requested type and date range.
        If found, the room is checked in for the given period; otherwise, a dummy room indicating failure is returned.

        :param req: A Request object containing the room type, check-in date, and check-out date.
        :return: The Room object if a room is available and checked in; otherwise, a dummy Room (with NOT_A_ROOM type).
        """
        roomType, checkInDate, checkOutDate = req.get_request_info()
        room = self.checkAvailability(roomType, checkInDate, checkOutDate)
        
        if room:
            return room.checkIn(checkInDate, checkOutDate)
        else:
            # Return a dummy room indicating no available room was found.
            return Room(-1, RoomType.NOT_A_ROOM, -1)
        
    def processRequests(self, requests: List[Request]) -> List[Room]:
        """
        Processes a list of room requests by applying the _processRequest helper method to each request.

        :param requests: A list of Request objects.
        :return: A list of Room objects corresponding to the processed requests.
                 Each Room will either be a successfully assigned room or a dummy room (NOT_A_ROOM).
        """
        process_results = []
        for request in requests:
            process_results.append(self._processRequest(request))
        return process_results
        
    # GETTERS
    def checkAvailability(self, roomType: RoomType, checkInDate: int, checkOutDate: int) -> Optional[Room]:
        """
        Checks if there is an available room matching the requested room type and date range.
        If no room of the exact type is available, an upgrade to a higher room type is attempted.

        :param roomType: The requested RoomType.
        :param checkInDate: The check-in day index (inclusive).
        :param checkOutDate: The check-out day index (non-inclusive).
        :return: A Room object if one is available; otherwise, None.
        """
        # First, try to find a room of the exact requested type.
        for room in self.rooms:
            if room.get_type() == roomType and room.isAvailable(checkInDate, checkOutDate):
                return room
        
        # If no room of the requested type is available, attempt to find an upgraded room type.
        for room in self.rooms:
            if room.get_type() > roomType and room.isAvailable(checkInDate, checkOutDate):
                return room
        
        # No available room found.
        return None
        
    def get_room_numbers(self) -> int:
        """
        Returns the total number of Room objects in the hotel.

        :return: The total count of rooms.
        """
        return len(self.rooms)
    
    def get_current_occupancy(self, today: int) -> int:
        """
        Counts the number of rooms that are occupied on a specific day.

        :param today: The day index for checking occupancy.
        :return: The number of occupied rooms.
        """
        current_occupancy = 0
        for room in self.rooms:
            # room.isOccupied(today) should return 1 if occupied, 0 otherwise.
            current_occupancy += room.isOccupied(today)
        return current_occupancy
    
    def getTodayOccupancy(self, today: int) -> DefaultDict[RoomType, int]:
        """
        Returns a dictionary mapping each RoomType to the number of occupied rooms for that type on the given day.

        :param today: The day index to check occupancy.
        :return: A defaultdict(int) mapping RoomType to the count of occupied rooms.
        """
        occupancy = defaultdict(int)
        
        for room in self.rooms:
            occupancy[room.type] += room.isOccupied(today)
        
        return occupancy
    
    def get_room_info(self) -> Dict[RoomType, int]:
        """
        Returns the initial room configuration dictionary used to set up the hotel.

        :return: A dictionary mapping RoomType to the count of rooms of that type.
        """
        return self.rooms_info
