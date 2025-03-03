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

        self.RoomTypes = list(RoomType)[:5]

    def generateRequest(self):
        # 랜덤 요청 생성
        desired_room_type = random.choice(self.RoomTypes)
        duration_day = random.randint(1,5)
        checkInDate = self.current_day + random.randint(0, 10)
        checkOutDate = checkInDate + duration_day

        if checkInDate < self.days and checkOutDate < self.days:
            return Request(desired_room_type, checkInDate, checkOutDate)

        return Request(RoomType.NOT_A_ROOM, -1, -1)

    def step(self):
        self.current_hour += self.hour_per_step
        if self.current_hour >= 24:
            self.current_day += 1
            self.current_hour -= 24

        if self.current_day == self.days:
            return False

        self.request = self.generateRequest()
        self.request_result = self.hotel.processRequest(self.request)

        self.updateStatistics()

        # Debugging code
        for room in self.hotel.rooms:
            print(room.type, room.occupancyDuration)
        print()
        # Debugging code

        return True

    def updateStatistics(self):
        self.total_requests += 1

        checkInDate, checkOutDate = self.request.get_time_info()

        if self.request_result.isAvailable(0, 0):
            self.succesed_requests += 1
            self.profit += self.request_result.get_price(checkInDate, checkOutDate)

        self.success_rate = (self.succesed_requests / self.total_requests) * 100
        self.avg_occupancy = (self.hotel.get_current_occupancy(self.current_day) / self.total_occupancy) * 100
        

    # GETTERS
    def displayStatistics(self):
        return {"avg_occupancy" : self.avg_occupancy,
                "profit" : self.profit,
                "success_rate" : self.success_rate}
    
    def displayReservationInfo(self):
        if self.request.isRequest():
            room_type, (checkIn, checkOut) = self.request.get_room_name(), self.request.get_time_info()
            if self.request_result.isRoom():
                return  f"+/ Id : {self.request_result.get_id()} / Wanted : {room_type} / " + \
                        f"Reserved : {self.request_result.get_type_name()} / In {checkIn} / Out {checkOut}"
            else:
                return f"-/ Wanted : {room_type} / In : {checkIn} / Out : {checkOut}"
        else:
            return ""
        
    def displayTodayOccupancy(self):
        occupancy = self.hotel.getTodayOccupancy(self.current_day)
        room_numbers_each_type = self.hotel.get_room_info()
        display = dict()

        for room_type in RoomType:
            if not room_type == RoomType.NOT_A_ROOM:
                display[room_type] = f"{occupancy[room_type]}/{room_numbers_each_type[room_type]}"

        return display

    def getTimeInfo(self):
        return self.current_day, self.current_hour