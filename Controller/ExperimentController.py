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

    MIN_DAYS, MAX_DAYS = 12, 30
    MIN_STEPS, MAX_STEPS = 1, 6
    MIN_REQ, MAX_REQ = 1, 6
    MIN_ROOM_NUM, MAX_ROOM_NUM = 4, 6
    MIN_DURATION_DAY, MAX_DURATION_DAY = 1, 5
    ONE_DAY = 24
    def __init__(self) -> None:
        """
        Initializes an ExperimentController instance with default values.
        The simulation parameters (e.g., days, hours per step, room info) are set to None.
        They must be initialized later using the 'initialize_experiment' method.
        """
        # Simulation parameters (to be set during experiment initialization)
        self.days = None                      # Total simulation duration in days
        self.hour_per_step = None             # Number of hours that pass in one simulation step
        self.request_num_per_step = None      # Tuple (min_requests, max_requests) per simulation step

        self.hotel = None                     # Hotel instance to process room requests

        self.current_hour = 0                 # Current simulation hour
        self.current_day = 0                  # Current simulation day

        # List of possible room types for random request generation.
        # Assumes that the first five elements of RoomType are valid types and exclude NOT_A_ROOM.
        self.RoomTypes = list(RoomType)[:5]

    def initialize_experiment(self, days: int, steps: int, rooms_info: Dict[RoomType, int], request_num_per_step: Tuple[int, int]) -> None:
        """
        Initializes the simulation parameters and creates instances for Hotel and Statistics.

        :param days: Total number of days for the simulation.
        :param steps: Number of hours that pass in one simulation step.
        :param rooms_info: A dictionary mapping each RoomType to the number of rooms in the hotel.
        :param request_num_per_step: A tuple (min_requests, max_requests) specifying the range of requests generated per step.
        """
        # Set simulation parameters
        self.days = days                      # Total simulation duration in days
        self.hour_per_step = steps            # Number of hours per simulation step
        self.request_num_per_step = request_num_per_step

        # Create Hotel instance based on room information and simulation duration
        self.hotel = Hotel(rooms_info, days)

    def generate_request(self) -> Request:
        """
        Generates a single random room request.
        The request has a randomly selected room type (from valid types), a random duration (1 to 5 days),
        and a random check-in date within the simulation period.
        If the calculated check-out date exceeds the simulation duration, it is clamped to the total days.
        If the request falls outside the valid simulation range, a dummy request with NOT_A_ROOM is returned.
        
        :return: A Request object representing the generated room request.
        """
        # Randomly choose a valid room type from the available types.
        desired_room_type = random.choice(self.RoomTypes)
        # Determine a random duration of stay between 1 and 5 days.
        duration_day = random.randint(ExperimentController.MIN_DURATION_DAY, ExperimentController.MAX_DURATION_DAY)

        # Randomly select a check-in date starting from the current day up to the end of simulation.
        check_in_date = self.current_day + random.randint(0, self.days - self.current_day)
        # Calculate the check-out date based on the duration of stay.
        check_out_date = check_in_date + duration_day
        # Clamp the check-out date to the simulation limit if it exceeds the total days.
        if check_out_date >= self.days:
            check_out_date = self.days

        # Return a valid request if the check-in and check-out dates fall within simulation bounds.
        if check_in_date < self.days and check_out_date <= self.days:
            return Request(desired_room_type, check_in_date, check_out_date)
        
        # Otherwise, return a dummy request indicating an out-of-range request.
        return Request(RoomType.NOT_A_ROOM, -1, -1)

    def generate_requests(self, min_request_num: int, max_request_num: int) -> List[Request]:
        """
        Generates a random list of room requests.
        The number of requests is randomly chosen between min_request_num and max_request_num.

        :param min_request_num: Minimum number of requests to generate in one step.
        :param max_request_num: Maximum number of requests to generate in one step.
        :return: A list of randomly generated Request objects.
        """
        # Determine the number of requests to generate for this simulation step.
        req_num = random.randint(min_request_num, max_request_num)
        requests = []

        # Generate each request and add it to the list.
        for _ in range(req_num):
            requests.append(self.generate_request())

        return requests

    def step(self) -> bool:
        """
        Advances the simulation by one time step.
        It increments the current time by the specified hours per step.
        If 24 hours are reached, the simulation day is incremented.
        Then, random room requests are generated, processed by the hotel,
        and simulation statistics are updated.

        :return: False if the simulation has reached the final day; otherwise, True.
        """
        # Increment the current hour by the simulation step interval.
        self.current_hour += self.hour_per_step
        # If the current hour is 24 or more, advance to the next day and adjust the hour.
        if self.current_hour >= ExperimentController.ONE_DAY:
            self.current_day += 1
            self.current_hour -= ExperimentController.ONE_DAY

        # If the simulation has reached the final day, stop the simulation.
        if self.current_day == self.days:
            return False

        # Generate room requests for the current simulation step.
        self.requests = self.generate_requests(*self.request_num_per_step)
        # Process the generated requests using the Hotel instance; pass the current day for context.
        self.request_results = self.hotel.process_requests(self.requests, self.current_day)

        return True

    def display_statistics(self) -> str:
        """
        Retrieves a formatted string representation of the simulation statistics.

        :return: A string displaying the current simulation statistics.
        """
        return self.hotel.get_statistics()

    def display_reservation_info(self) -> str:
        """
        Builds a string describing each room request along with its reservation result.
        For each valid request, it includes the desired room type, reservation status,
        check-in/check-out dates, and cost information. If a discount is applied, it notes that.

        :return: A formatted string with reservation details for each request.
        """
        display = ""
        # Loop through each request and its corresponding result.
        for request, (cost, request_result) in zip(self.requests, self.request_results):
            if request.is_request():
                # Get the room type's friendly name and the time info (check-in and check-out dates).
                room_type, (checkIn, checkOut) = request.get_room_name(), request.get_time_info()
                if request_result.is_room():
                    # Append information about the successful reservation.
                    display += (
                        f"+/ Id : {request_result.get_id()} / Wanted : {room_type} / "
                        f"Reserved : {request_result.get_type_name()} / In {checkIn} / Out {checkOut} / Cost {cost}"
                    )
                    # If the reserved room type is different from the requested type, note a discount.
                    display += "/ Discounted(70%)\n" if request.get_type() != request_result.get_type() else "\n"
                else:
                    # Append information about the failed reservation.
                    display += f"-/ Wanted : {room_type} / In : {checkIn} / Out : {checkOut}\n"
        return display

    def display_today_occupancy(self) -> str:
        """
        Retrieves today's occupancy status for each room type.
        It returns a dictionary where each key is a RoomType and the value is a string
        showing the number of occupied rooms over the total available (e.g., "2/5").

        :return: A dictionary with room occupancy details for the current simulation day.
        """
        # Get the occupancy counts for the current day.
        occupancy = self.hotel.get_today_occupancy(self.current_day)
        # Get the total room numbers for each room type.
        room_numbers_each_type = self.hotel.get_room_info()
        display = dict()

        # Build a display string for each valid room type.
        for room_type in RoomType:
            if room_type != RoomType.NOT_A_ROOM:
                display[room_type] = f"{occupancy[room_type]}/{room_numbers_each_type[room_type]}"
        return display

    def get_time_info(self) -> Tuple[str, str]:
        """
        Returns the current simulation time.

        :return: A tuple containing the current day (1-indexed) and the current hour formatted as a string.
        """
        return f"{self.current_day + 1}/{self.days}", f"{self.current_hour}:00"

    def get_init_info(self) -> Tuple[int, int]:
        """
        Retrieves initial simulation parameters.

        :return: A tuple containing the total simulation days and the number of hours per simulation step.
        """
        return self.days, self.hour_per_step

    def goto_end(self) -> None:
        """
        Advances the simulation to its end state by processing a batch of room requests that simulate
        all remaining steps of the experiment. It calculates the remaining number of simulation steps based on
        the current day and hour, generates a batch of requests for those remaining steps, processes them,
        updates the occupancy, and sets the simulation time to the final day at 23:00 hours.
        """
        # Calculate the number of steps per day.
        steps_per_day = ExperimentController.ONE_DAY // self.hour_per_step
        # Calculate the total number of simulation steps.
        total_steps = self.days * steps_per_day
        # Calculate the number of steps that have been completed so far.
        completed_steps = self.current_day * steps_per_day + (self.current_hour // self.hour_per_step)
        # Determine the remaining number of steps.
        remaining_steps = total_steps - completed_steps
        # Calculate the minimum and maximum number of requests for the remaining steps.
        remaining_min_requests = remaining_steps * self.request_num_per_step[0]
        remaining_max_requests = remaining_steps * self.request_num_per_step[1]

        # Generate a batch of requests covering the remaining simulation period.
        self.requests = self.generate_requests(remaining_min_requests, remaining_max_requests)
        # Process these requests using the Hotel instance, providing the current day.
        self.request_results = self.hotel.process_requests(self.requests, self.current_day)

        # Set simulation time to the final day at 23:00.
        self.current_day = self.days - 1
        self.current_hour = ExperimentController.ONE_DAY - 1
