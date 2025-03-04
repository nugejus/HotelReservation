import random
from Model.RoomType import RoomType
from Model.Hotel import Hotel
from Model.Request import Request

from typing import *
T = TypeVar("T")

class Experiment:
    """
    A class representing a simulation (experiment) of hotel room requests.
    It generates random requests, processes them through a Hotel instance,
    and updates statistics for each simulation step.
    """

    def __init__(self, days : int, hour_per_step : int, rooms_info : Dict[RoomType, int]) -> None:
        """
        Initializes the experiment with the given parameters.

        :param days: Total number of days for the simulation.
        :param hour_per_step: The number of hours that pass in one simulation step.
        :param rooms_info: A dictionary mapping each RoomType to the count of rooms in the hotel.
        """
        # Simulation parameters
        self.days = days                      # The total simulation duration in days
        self.hour_per_step = hour_per_step    # The number of hours per simulation step
        self.hotel = Hotel(rooms_info, days)

        # Statistical data
        self.total_requests = 0              # Total requests generated so far
        self.total_occupancy = self.hotel.get_room_numbers()  # The total number of rooms in the hotel
        self.succesed_requests = 0           # Number of successfully processed requests

        self.sum_occupancy = 0
        self.avg_occupancy = 0   # The average (actually current day's) occupancy rate (in %)
        self.success_rate = 0    # The success rate of requests (in %)
        self.occupancy_count = 1
        self.profit = 0          # The total profit (e.g., sum of room prices)

        # Current time tracking
        self.current_day = 0
        self.current_hour = 0

        # Possible room types for random request generation (excluding NOT_A_ROOM)
        self.RoomTypes = list(RoomType)[:5]

    def _generateRequest(self) -> Request:
        """
        Generates a single random room request with random room type, duration, and start day.
        If the generated request is out of the simulation range, returns a dummy 'NOT_A_ROOM'.
        """
        desired_room_type = random.choice(self.RoomTypes)
        duration_day = random.randint(1, 5)

        checkInDate = self.current_day + random.randint(0, 10)
        checkOutDate = checkInDate + duration_day

        if checkInDate < self.days and checkOutDate < self.days:
            return Request(desired_room_type, checkInDate, checkOutDate)
        
        # Return an invalid request if the generated date range exceeds total simulation days
        return Request(RoomType.NOT_A_ROOM, -1, -1)
    
    def generateRequests(self, max_request_num : int) -> List[Request]:
        """
        Generates a random number of requests (between 1 and max_request_num).

        :param max_request_num: Maximum number of requests to generate in one step.
        :return: A list of randomly generated Request objects.
        """
        req_num = random.randint(1, max_request_num)
        requests = []

        for _ in range(req_num):
            requests.append(self._generateRequest())

        return requests

    def step(self) -> bool:
        """
        Advances the simulation by one step. Increments time (hour_per_step), 
        generates random requests, processes them through the hotel, and updates statistics.

        :return: False if the simulation has reached the final day, otherwise True.
        """
        self.current_hour += self.hour_per_step
        if self.current_hour >= 24:
            self.current_day += 1
            self.current_hour -= 24

        if self.current_day == self.days:
            # Simulation ends
            return False

        # Generate and process requests
        self.requests = self.generateRequests(5)
        self.request_results = self.hotel.processRequests(self.requests)

        # Update experiment statistics
        self._updateStatistics()

        # Debugging code (prints occupancy info)
        for room in self.hotel.rooms:
            print(room.type, room.occupancyDuration)
        print()

        return True

    def _updateStatistics(self) -> None:
        """
        Updates the statistical attributes based on the latest requests and processing results.
        """
        self.total_requests += len(self.request_results)

        for request, request_result in zip(self.requests, self.request_results):
            checkInDate, checkOutDate = request.get_time_info()

            # If the room returned is valid (i.e., isAvailable(0, 0) returns True),
            # we consider it a successful reservation.
            if request_result.isAvailable(0, 0):
                self.succesed_requests += 1
                self.profit += request_result.get_price(checkInDate, checkOutDate)

        self.success_rate = (self.succesed_requests / self.total_requests) * 100

        self.total_occupancy_today = (self.hotel.get_current_occupancy(self.current_day) / self.hotel.get_room_numbers()) * 100
        self.sum_occupancy += self.total_occupancy_today
        self.avg_occupancy = self.sum_occupancy / self.occupancy_count
        self.occupancy_count += 1

    # GETTERS (Display / Utility Methods)
    def displayStatistics(self) -> Dict[str, T]:
        """
        Returns a dictionary containing current occupancy, profit, and success rate.
        Useful for GUI updates or console logs.
        """
        return {
            "avg_occupancy": self.avg_occupancy,
            "profit": self.profit,
            "success_rate": self.success_rate
        }
    
    def displayReservationInfo(self) -> str:
        """
        Builds a string describing each request and whether it was successfully 
        reserved or not, along with room type and check-in/check-out information.
        """
        display = ""
        for request, request_result in zip(self.requests, self.request_results):
            if request.isRequest():
                room_type, (checkIn, checkOut) = request.get_room_name(), request.get_time_info()
                if request_result.isRoom():
                    display += (
                        f"+/ Id : {request_result.get_id()} / Wanted : {room_type} / "
                        f"Reserved : {request_result.get_type_name()} / In {checkIn} / Out {checkOut} \n"
                    )
                else:
                    display += f"-/ Wanted : {room_type} / In : {checkIn} / Out : {checkOut}\n"
        return display

    def displayTodayOccupancy(self) -> str:
        """
        Returns a dictionary mapping each RoomType to a string representation
        of today's occupancy (e.g., "2/5" meaning 2 out of 5 rooms occupied).
        """
        occupancy = self.hotel.getTodayOccupancy(self.current_day)
        room_numbers_each_type = self.hotel.get_room_info()
        display = dict()

        for room_type in RoomType:
            if room_type != RoomType.NOT_A_ROOM:
                display[room_type] = f"{occupancy[room_type]}/{room_numbers_each_type[room_type]}"
        return display

    def getTimeInfo(self) -> str:
        """
        Returns the current simulation time as a tuple (day, hour).
        """
        return self.current_day, self.current_hour

    def get_init_info(self):
        return self.days, self.hour_per_step