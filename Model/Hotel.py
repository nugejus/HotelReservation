from Model.Room import Room
from Model.Request import Request
from Model.RoomType import RoomType
from Model.Statistics import Statistics

from collections import defaultdict
from typing import Dict, List, Tuple, DefaultDict

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
        self.rooms: List[Room] = []          # List to store Room objects.
        self.rooms_info: Dict[RoomType, int] = rooms_info
        
        c = 0
        # Create Room objects for each room type based on the provided counts.
        # 'c' is used as the starting ID for each room; after processing one type,
        # it is incremented by the number of rooms created plus one to leave a gap between IDs.
        for room_type, numbers in rooms_info.items():
            for i in range(c, c + numbers):
                self.rooms.append(Room(i, room_type, days))
            c = c + numbers + 1  # Update the room ID counter with an extra gap.

        # Initialize the Statistics instance with the total number of rooms.
        self.statistics: Statistics = Statistics(len(self.rooms))

    def process_request(self, req: Request) -> Tuple[int, Room]:
        """
        Processes a single room request.
        It attempts to find an available room of the requested type and date range.
        If found, the room is checked in for the given period; otherwise, a dummy room is returned.

        :param req: A Request object containing the room type, check-in date, and check-out date.
        :return: A tuple (cost, Room) where cost is the cost for the stay if successful,
                 and Room is either the assigned room or a dummy Room (with NOT_A_ROOM type) if no room is available.
        """
        room_type, check_in_date, check_out_date = req.get_request_info()
        cost, room = self.check_availability(room_type, check_in_date, check_out_date)
        
        if cost > -1:
            # If a valid room is found, check the room in and return the cost and the room.
            return (cost, room.check_in(check_in_date, check_out_date))
        else:
            # Otherwise, return a dummy room indicating no available room was found.
            return (-1, Room(-1, RoomType.NOT_A_ROOM, -1))
        
    def process_requests(self, requests: List[Request], today: int) -> List[Tuple[int, Room]]:
        """
        Processes a list of room requests by applying the process_request method to each request.

        :param requests: A list of Request objects.
        :param today: The current day index for occupancy context.
        :return: A list of tuples (cost, Room) corresponding to the processed requests.
        """
        process_results: List[Tuple[int, Room]] = []
        for request in requests:
            process_results.append(self.process_request(request))

        # Update statistics using the processed requests and the current occupancy.
        self.statistics.update(
            request_results=process_results, 
            current_occupancy=self.get_current_occupancy(today)
        )
        return process_results
        
    def check_availability(self, room_type: RoomType, check_in_date: int, check_out_date: int) -> Tuple[int, Room]:
        """
        Checks if there is an available room matching the requested room type and date range.
        If no room of the exact type is available, an upgrade to a higher room type is attempted.

        :param room_type: The requested RoomType.
        :param check_in_date: The check-in day index (inclusive).
        :param check_out_date: The check-out day index (non-inclusive).
        :return: A tuple (cost, Room) where cost is the price for the stay if available,
                 or (-1, dummy Room) if no room is available.
        """
        # First, try to find a room of the exact requested type.
        for room in self.rooms:
            if room.get_type() == room_type and room.is_available(check_in_date, check_out_date):
                return (room.get_price(check_in_date, check_out_date), room)
        
        # If no room of the requested type is available, attempt to find an upgraded room type.
        for room in self.rooms:
            if room.get_type() > room_type and room.is_available(check_in_date, check_out_date):
                # Apply a 30% discount if the room is upgraded.
                return (int(room.get_price(check_in_date, check_out_date) * 0.7), room)
        
        # No available room found.
        return (-1, Room(-1, RoomType.NOT_A_ROOM, -1))
        
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
            # room.is_occupied(today) should return 1 if occupied, 0 otherwise.
            current_occupancy += room.is_occupied(today)
        return current_occupancy
    
    def get_today_occupancy(self, today: int) -> DefaultDict[RoomType, int]:
        """
        Returns a dictionary mapping each RoomType to the number of occupied rooms for that type on the given day.

        :param today: The day index to check occupancy.
        :return: A defaultdict mapping RoomType to the count of occupied rooms.
        """
        occupancy: DefaultDict[RoomType, int] = defaultdict(int)
        
        for room in self.rooms:
            occupancy[room.type] += room.is_occupied(today)
        
        return occupancy
    
    def get_room_info(self) -> Dict[RoomType, int]:
        """
        Returns the initial room configuration dictionary used to set up the hotel.

        :return: A dictionary mapping RoomType to the count of rooms of that type.
        """
        return self.rooms_info

    def get_statistics(self) -> str:
        """
        Retrieves a formatted string representation of the current simulation statistics.

        :return: A string representing the simulation statistics.
        """
        return self.statistics.display_statistics()
