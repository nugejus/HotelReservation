from Hotel import Hotel
import random
from RoomType import RoomType
from Request import Request

class Experiment:
    def __init__(self, days, hour_per_step, rooms_info):
        self.days = days          # 전체 시뮬레이션 기간 (일)
        self.hour_per_step = hour_per_step          # 시뮬레이션 단계 (시간 단위)
        self.hotel = Hotel(rooms_info)
        self.parameters = {}

        # 통계 관련 속성
        self.occupancyRates = {}  # 각 객실 유형별 점유율
        self.success_rate = 0 # 성공적으로 처리된 요청 수

        self.total_requests = 0  # 전체 요청 수
        self.succesed_requests = 0 # 성공한 요청 수

        self.total_occupancy = self.hotel.get_room_numbers() # 총 방의 갯수
        self.avg_occupancy = 0 # 점유중인 방의갯수

        self.profit = 0

        self.current_day = 0
        self.current_hour = 0

    def generateRequest(self):
        # 랜덤 요청 생성
        desired_room_type = random.choice(list(RoomType))
        # 체류 기간: 1일(24시간)에서 5일(120시간) 사이
        duration_day = random.randint(1,5)
        checkInDate = self.current_day + random.randint(0, 10)
        checkOutDate = checkInDate + duration_day
        return Request(desired_room_type, checkInDate, checkOutDate)

    def step(self):
        request = self.generateRequest()
        request_result = self.hotel.processRequest(request)
        
        self.updateStatistics(request_result)

        self.current_hour += self.hour_per_step
        if self.current_hour >= 24:
            self.current_day += 1
            self.current_hour -= 24

        return request, request_result,  self.current_day, self.current_hour

    def updateStatistics(self, request_result):
        self.total_requests += 1

        if request_result:
            self.succesed_requests += 1
            self.success_rate = (self.succesed_requests / self.total_requests) * 100
            self.profit += request_result.get_price()
        
        self.avg_occupancy = self.hotel.get_current_occupancy() / self.total_occupancy
        
    def getStatistics(self):
        return {"avg_occupancy" : self.avg_occupancy,
                "profit" : self.profit,
                "success_rate" : self.success_rate}