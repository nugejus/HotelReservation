import random
from Model.RoomType import RoomType
from Model.Hotel import Hotel
from Model.Request import Request
from Model.Statistics import Statistics

from typing import *
T = TypeVar("T")

class ExperimentController:
    """
    A class representing a simulation (experiment) of hotel room requests.
    It generates random requests, processes them through a Hotel instance,
    and updates statistics for each simulation step.
    """

    def __init__(self) -> None:
        """
        Initializes the experiment with the given parameters.

        :param days: Total number of days for the simulation.
        :param hour_per_step: The number of hours that pass in one simulation step.
        :param rooms_info: A dictionary mapping each RoomType to the count of rooms in the hotel.
        """
        # Simulation parameters
        self.days = None                      # The total simulation duration in days
        self.hour_per_step = None    # The number of hours per simulation step
        self.request_num_per_step = None

        self.hotel = None
        self.statistics = None

        self.current_hour = 0
        self.current_day = 0

        # Possible room types for random request generation (excluding NOT_A_ROOM)
        self.RoomTypes = list(RoomType)[:5]

    def initialize_experiment(self, days, steps, rooms_info, request_num_per_step):
        # Simulation parameters
        self.days = days                      # The total simulation duration in days
        self.hour_per_step = steps    # The number of hours per simulation step
        self.request_num_per_step = request_num_per_step

        self.hotel = Hotel(rooms_info, days)
        self.statistics = Statistics(self.hotel.get_room_numbers())

    def _generateRequest(self) -> Request:
        """
        Generates a single random room request with random room type, duration, and start day.
        If the generated request is out of the simulation range, returns a dummy 'NOT_A_ROOM'.
        """
        desired_room_type = random.choice(self.RoomTypes)
        duration_day = random.randint(1, 5)

        checkInDate = self.current_day + random.randint(0, self.days - self.current_day)
        checkOutDate = checkInDate + duration_day
        if checkOutDate >= self.days:
            checkOutDate = self.days

        if checkInDate < self.days and checkOutDate <= self.days:
            return Request(desired_room_type, checkInDate, checkOutDate)
        
        # Return an invalid request if the generated date range exceeds total simulation days
        return Request(RoomType.NOT_A_ROOM, -1, -1)
    
    def generateRequests(self, min_request_num: int, max_request_num : int) -> List[Request]:
        """
        Generates a random number of requests (between 1 and max_request_num).

        :param max_request_num: Maximum number of requests to generate in one step.
        :return: A list of randomly generated Request objects.
        """
        req_num = random.randint(min_request_num, max_request_num)
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
        self.requests = self.generateRequests(*self.request_num_per_step)
        self.request_results = self.hotel.processRequests(self.requests)
        current_occupancy = self.hotel.get_current_occupancy(self.current_day)
        # Update experiment statistics
        self.statistics.update(self.requests, self.request_results, current_occupancy)

        # # Debugging code (prints occupancy info)
        # for room in self.hotel.rooms:
        #     print(room.type, room.occupancyDuration)
        # print()

        return True

    # GETTERS (Display / Utility Methods)
    def displayStatistics(self):
        return self.statistics.displayStatistics()
    
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
    
    def gotoEnd(self):
        total_min_steps = self.days * (24 // self.hour_per_step) * self.request_num_per_step[0]
        total_max_steps = self.days * (24 // self.hour_per_step) * self.request_num_per_step[1]
        self.requests = self.generateRequests(total_min_steps, total_max_steps)
        self.request_results = self.hotel.processRequests(self.requests)
        current_occupancy = self.hotel.get_current_occupancy(self.current_day)

        self.current_day = self.days - 1
        self.current_hour = 23

        self.statistics.update(self.requests, self.request_results, current_occupancy)