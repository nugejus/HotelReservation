from Hotel import Hotel
import random
from RoomType import RoomType
from Request import Request

class Experiment:
    def __init__(self, days, hour_per_step, rooms_info):
        self.days = days            # 전체 시뮬레이션 기간 (일)
        self.hour_per_step = hour_per_step          # 시뮬레이션 단계 (시간 단위)
        self.hotel = Hotel(rooms_info, days)
        self.parameters = {}

        # 통계 관련 속성
        self.total_requests = 0  # 전체 요청 수
        self.total_occupancy = self.hotel.get_room_numbers() # 총 방의 갯수
        self.succesed_requests = 0 # 성공한 요청 수

        self.avg_occupancy = 0 # 점유중인 방의갯수
        self.success_rate = 0 # 성공적으로 처리된 요청 수
        self.profit = 0

        self.current_day = 0
        self.current_hour = 0

        self.request = None

    def generateRequest(self):
        # 랜덤 요청 생성
        desired_room_type = random.choice(list(RoomType))
        try:
            duration_day = random.randint(1,5)
            checkInDate = self.current_day + random.randint(0, 10)
            checkOutDate = checkInDate + duration_day
            if checkInDate < self.days and checkOutDate < self.days:
                return Request(desired_room_type, checkInDate, checkOutDate)
            else:
                raise Exception
        except:
            return False


    def step(self):
        self.request = self.generateRequest()

        if not self.request:
            return False, False, self.current_day, self.current_hour

        request_result = self.hotel.processRequest(self.request)
        self.updateStatistics(request_result)

        self.current_hour += self.hour_per_step
        if self.current_hour >= 24:
            self.current_day += 1
            self.current_hour -= 24

        for room in self.hotel.rooms:
            print(room.type, room.occupancyDuration)
        print()

        return self.request, request_result, self.current_day, self.current_hour

    def updateStatistics(self, request_result):
        self.total_requests += 1

        _, checkInDate, checkOutDate = self.request.get_request_info()

        if request_result:
            self.succesed_requests += 1
            self.profit += request_result.get_price(checkInDate, checkOutDate)

        self.success_rate = (self.succesed_requests / self.total_requests) * 100
        self.avg_occupancy = (self.hotel.get_current_occupancy(self.current_day) / self.total_occupancy) * 100
        
    def getStatistics(self):
        return {"avg_occupancy" : self.avg_occupancy,
                "profit" : self.profit,
                "success_rate" : self.success_rate}