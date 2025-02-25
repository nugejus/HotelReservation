from RoomType import RoomType
from Room import Room

class Hotel:
    def __init__(self):
        self.rooms = []
        # 최소 20개 이상의 객실 생성 (여기서는 20개로 고정)
        K = 20
        types = [RoomType.LUX, RoomType.HALF_LUX, RoomType.SINGLE, RoomType.SIMPLE_DOUBLE, RoomType.DOUBLE_WITH_SOFA]
        prices = {
            RoomType.LUX: 120,
            RoomType.HALF_LUX: 100,
            RoomType.SINGLE: 70,
            RoomType.SIMPLE_DOUBLE: 80,
            RoomType.DOUBLE_WITH_SOFA: 90
        }
        for i in range(1, K + 1):
            room_type = types[(i - 1) % len(types)]
            price = prices[room_type]
            room = Room(i, room_type, price)
            self.rooms.append(room)

    def checkAvailability(self, roomType, checkInDate, checkOutDate):
        # 요청한 타입과 일치하는 객실 검색
        for room in self.rooms:
            if room.type == roomType and room.isAvailable(checkInDate, checkOutDate):
                return room
        # 대체 객실 제공 로직은 필요시 추가
        return None

    def processRequest(self, req):
        if not req.validate():
            return False
        room = self.checkAvailability(req.desiredRoomType, req.checkInDate, req.checkOutDate)
        if room:
            # 예약 성공 시 객실에 체크인/체크아웃 날짜 저장
            room.checkInDate = req.checkInDate
            room.checkOutDate = req.checkOutDate
            return True
        else:
            return False