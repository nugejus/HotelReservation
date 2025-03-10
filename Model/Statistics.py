from Model.RoomType import RoomType
from typing import List, Dict, Tuple, DefaultDict

class Statistics:
    def __init__(self, total_room_count: int) -> None:
        """
        Initializes the Statistics instance with the total number of rooms.
        
        :param total_room_count: Total number of rooms available in the hotel.
        """
        # Total number of requests processed so far.
        self.total_requests: int = 0
        # Total number of rooms available in the hotel.
        self.total_room_count: int = total_room_count
        # Number of successfully processed requests (i.e., successful reservations).
        self.succesed_requests: int = 0

        # Sum of occupancy percentages across simulation updates.
        self.sum_occupancy: float = 0.0
        # Average occupancy rate (in percentage) computed over updates.
        self.avg_occupancy: float = 0.0
        # Success rate (in percentage) of room reservation requests.
        self.success_rate: float = 0.0
        # Count of occupancy updates used to calculate the average occupancy.
        self.occupancy_count: int = 1
        # Total profit accumulated from successful reservations.
        self.profit: float = 0.0

    def update(self, request_results: List[Tuple[int, any]], current_occupancy: int) -> None:
        """
        Updates the statistics based on the latest batch of room requests and their results.
        Each element in request_results is a tuple containing (cost, room).

        :param request_results: A list of tuples (cost, room) returned after processing requests.
        :param current_occupancy: The current number of occupied rooms in the hotel.
        """
        # Update the total number of processed requests.
        self.total_requests += len(request_results)

        # Process each tuple (cost, room) from the request results.
        for cost, request_result in request_results:
            # If the room is valid (i.e., the reservation was successful),
            # increment the count of successful reservations and add the cost to the profit.
            if request_result.is_room():
                self.succesed_requests += 1
                self.profit += cost

        # Calculate the success rate as the percentage of successful requests.
        self.success_rate = (self.succesed_requests / self.total_requests) * 100

        # Compute today's occupancy percentage.
        occupancy_today = (current_occupancy / self.total_room_count) * 100
        # Add the current occupancy percentage (rounded to 2 decimals) to the cumulative sum.
        self.sum_occupancy += round(occupancy_today, 2)
        # Calculate the average occupancy across all updates so far.
        self.avg_occupancy = self.sum_occupancy / self.occupancy_count
        # Increment the count of occupancy updates.
        self.occupancy_count += 1

    def display_statistics(self) -> Dict[str, float]:
        """
        Returns a dictionary containing key simulation statistics, such as average occupancy,
        total profit, success rate, total requests, count of successful requests, and failed requests.

        :return: A dictionary with keys 'avg_occupancy', 'profit', 'success_rate', 'total_request',
                 'success_count', and 'fail_count'.
        """
        return {
            "avg_occupancy": self.avg_occupancy,
            "profit": self.profit,
            "success_rate": self.success_rate,
            "total_request": self.total_requests,
            "success_count": self.succesed_requests,
            "fail_count": self.total_requests - self.succesed_requests
        }

    def goto_end(self, requests: List[any], request_results: List[Tuple[int, any]], remaining_occupancy: List[int]) -> None:
        """
        Processes the remaining simulation steps at the end of the experiment.
        It updates the statistics based on the final batch of room requests and adjusts occupancy statistics.

        :param requests: A list of Request objects for the remaining simulation steps.
        :param request_results: A list of tuples (cost, room) corresponding to these requests.
        :param remaining_occupancy: A list of occupancy numbers (one per remaining step).
        """
        # Update the total number of processed requests by adding the number of new requests.
        self.total_requests += len(requests)

        # Process each request and its corresponding result.
        for request, request_result in zip(requests, request_results):
            check_in_date, check_out_date = request.get_time_info()

            # If the reservation is successful, update successful request count and profit.
            if request_result.is_room():
                self.succesed_requests += 1
                # Calculate the cost for the stay.
                cost = request_result.get_price(check_in_date, check_out_date)
                # Apply a 70% discount if the reserved room type differs from the requested type.
                if request.get_type() == request_result.get_type():
                    self.profit += cost
                else:
                    self.profit += cost * 0.7

        # Recalculate the success rate based on all processed requests.
        self.success_rate = (self.succesed_requests / self.total_requests) * 100
        
        # Update occupancy statistics for each remaining occupancy value.
        for oc in remaining_occupancy:
            occupancy_i = (oc / self.total_room_count) * 100
            self.sum_occupancy += round(occupancy_i, 2)
            self.avg_occupancy = self.sum_occupancy / self.occupancy_count
            self.occupancy_count += 1
