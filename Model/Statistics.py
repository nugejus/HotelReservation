from Model import Room, Request
from typing import *
T = TypeVar("T")

class Statistics:
    def __init__(self, total_room_count):
        self.total_requests = 0              # Total requests generated so far
        self.total_room_count = total_room_count  # The total number of rooms in the hotel
        self.succesed_requests = 0           # Number of successfully processed requests

        self.sum_occupancy = 0
        self.avg_occupancy = 0   # The average (actually current day's) occupancy rate (in %)
        self.success_rate = 0    # The success rate of requests (in %)
        self.occupancy_count = 1
        self.profit = 0          # The total profit (e.g., sum of room prices)

    def update(self, requests: Request, request_results: Room, current_occupancy: int):
        self.total_requests += len(request_results)

        for request, request_result in zip(requests, request_results):
            checkInDate, checkOutDate = request.get_time_info()

            # If the room returned is valid,
            # we consider it a successful reservation.
            if request_result.isRoom():
                self.succesed_requests += 1
                self.profit += request_result.get_price(checkInDate, checkOutDate)

        self.success_rate = (self.succesed_requests / self.total_requests) * 100

        self.total_occupancy_today = (current_occupancy / self.total_room_count) * 100
        self.sum_occupancy += round(self.total_occupancy_today,2)
        self.avg_occupancy = self.sum_occupancy / self.occupancy_count
        self.occupancy_count += 1

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