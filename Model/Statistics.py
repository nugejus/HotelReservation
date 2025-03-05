from Model import Room, Request
from typing import List, Dict

class Statistics:
    def __init__(self, total_room_count: int) -> None:
        # Total number of requests processed so far.
        self.total_requests = 0
        # Total number of rooms available in the hotel.
        self.total_room_count = total_room_count
        # Number of successfully processed requests (i.e., reservations made).
        self.succesed_requests = 0

        # Sum of occupancy percentages across simulation updates.
        self.sum_occupancy = 0
        # Average occupancy rate (in percentage) computed over updates.
        self.avg_occupancy = 0
        # Success rate (in percentage) of room reservation requests.
        self.success_rate = 0
        # Count of occupancy updates used to calculate the average occupancy.
        self.occupancy_count = 1
        # Total profit accumulated from successful reservations.
        self.profit = 0

    def update(self, requests: List[Request], request_results: List[Room], current_occupancy: int) -> None:
        """
        Updates the statistics based on the latest batch of room requests and results.

        :param requests: A list of Request objects generated in the current simulation step.
        :param request_results: A list of Room objects returned after processing the requests.
                                Each Room indicates whether a reservation was successful.
        :param current_occupancy: The current number of occupied rooms in the hotel.
        """
        # Update the total number of processed requests.
        self.total_requests += len(request_results)

        # Process each request and its corresponding result.
        for request, request_result in zip(requests, request_results):
            checkInDate, checkOutDate = request.get_time_info()

            # If the result represents a valid room (reservation successful),
            # count it as a successful reservation and add the price for the stay.
            if request_result.is_room():
                self.succesed_requests += 1
                self.profit += request_result.get_price(checkInDate, checkOutDate)

        # Calculate the success rate as the percentage of successful requests.
        self.success_rate = (self.succesed_requests / self.total_requests) * 100

        # Compute today's occupancy percentage based on the current occupancy.
        self.total_occupancy_today = (current_occupancy / self.total_room_count) * 100
        # Add the current occupancy percentage (rounded to 2 decimals) to the sum.
        self.sum_occupancy += round(self.total_occupancy_today, 2)
        # Calculate the average occupancy over the updates so far.
        self.avg_occupancy = self.sum_occupancy / self.occupancy_count
        # Increment the count of occupancy updates.
        self.occupancy_count += 1

    def display_statistics(self) -> Dict[str, float]:
        """
        Returns a dictionary containing the average occupancy, total profit, and success rate.
        This information can be used for updating GUIs or logging to the console.

        :return: A dictionary with keys 'avg_occupancy', 'profit', and 'success_rate'.
        """
        return {
            "avg_occupancy": self.avg_occupancy,
            "profit": self.profit,
            "success_rate": self.success_rate
        }
