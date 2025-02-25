from Hotel import Hotel
import random
from RoomType import RoomType
from Request import Request

class Experiment:
    def __init__(self, days, hour_per_step):
        self.days = days          # 전체 시뮬레이션 기간 (일)
        self.hour_per_step = hour_per_step          # 시뮬레이션 단계 (시간 단위)
        self.hotel = Hotel()
        self.parameters = {}
        # 통계 관련 속성
        self.occupancyRates = {}  # 각 객실 유형별 점유율
        self.executedRequests = 0 # 성공적으로 처리된 요청 수
        self.bookingRequests = 0  # 전체 요청 수

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
        self.bookingRequests += 1
        success = self.hotel.processRequest(request)
        if success:
            self.executedRequests += 1
        self.current_hour += self.hour_per_step
        if self.current_hour >= 24:
            self.current_day += 1
            self.current_hour -= 24
        self.computeStatistics()

        return request

    def run(self):
        while self.current_day < self.days:
            req = self.generateRequest()
            self.bookingRequests += 1
            success = self.hotel.processRequest(req)
            if success:
                self.executedRequests += 1
            self.current_hour += self.hour_per_step
            if self.current_hour >= 24:
                self.current_day += 1
                self.current_hour -= 24
        self.computeStatistics()

    def computeStatistics(self):
        # 각 객실 유형별 점유율 계산
        counts = {rt: 0 for rt in RoomType}
        total = {rt: 0 for rt in RoomType}
        for room in self.hotel.rooms:
            total[room.type] += 1
            if room.checkInDate is not None:
                counts[room.type] += 1
        for rt in RoomType:
            if total[rt] > 0:
                self.occupancyRates[rt] = (counts[rt] / total[rt]) * 100
            else:
                self.occupancyRates[rt] = 0.0

    def displayStatistics(self):
        stats = f"전체 요청 수: {self.bookingRequests}\n" + \
                f"성공한 요청 수: {self.executedRequests}\n"
        for rt in self.occupancyRates:
            stats += f"{rt.name} 점유율: {self.occupancyRates[rt]:.2f}%\n"
        return stats