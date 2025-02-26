from Room import Room

class Hotel:
    def __init__(self, rooms_info):
        self.rooms = []
        c = 0
        for room_type, numbers in rooms_info.items():
            for i in range(c, c + numbers):
                self.rooms.append(Room(i, room_type))
            c = c + numbers + 1

    def checkAvailability(self, roomType, checkInDate):
        # 요청한 타입과 일치하는 객실 검색
        for room in self.rooms:
            if room.get_type() == roomType and room.isAvailable(checkInDate):
                return room
        # 대체 객실 제공 로직은 필요시 추가
        return None

    def processRequest(self, req):
        roomType, checkInDate, checkOutDate = req.get_request_info()
        room = self.checkAvailability(roomType, checkInDate)
        if room:
            # 예약 성공 시 객실에 체크인/체크아웃 날짜 저장
            return room.checkIn(checkInDate, checkOutDate)

        else:
            return False
        
    def get_room_numbers(self):
        return len(self.rooms)
    
    def get_current_occupancy(self):
        current_occupancy = 0
        for room in self.rooms:
            current_occupancy += not room.isFree()
        return current_occupancy