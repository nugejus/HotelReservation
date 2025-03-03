from RoomType import RoomType

class Room:
    prices = {
            RoomType.LUX: 120,
            RoomType.HALF_LUX: 100,
            RoomType.SINGLE: 70,
            RoomType.SIMPLE_DOUBLE: 80,
            RoomType.DOUBLE_WITH_SOFA: 90
        }
    names_to_display = {
            RoomType.LUX: "Люкс",
            RoomType.HALF_LUX: "Полу-Люкс",
            RoomType.SINGLE: "Одна кровать",
            RoomType.SIMPLE_DOUBLE: "Две кровати",
            RoomType.DOUBLE_WITH_SOFA: "Две кровати с диваном"
    }
    def __init__(self, id, room_type, days):
        self.id = id
        self.type = room_type
        if self.type != RoomType.NOT_A_ROOM:
            self.price = Room.prices[room_type]
            self.occupancyDuration = [False] * days
    
    # SETTERS
    def checkIn(self, checkInDate, checkOutDate):
        for i in range(checkInDate, checkOutDate):
            self.occupancyDuration[i] = True
        return self

    # GETTERS
    def isAvailable(self, checkInDate, checkOutDate):
        return self.type != RoomType.NOT_A_ROOM and not any(self.occupancyDuration[checkInDate:checkOutDate])

    def isRoom(self):
        return self.type != RoomType.NOT_A_ROOM
    
    def isFree(self, today):
        return not self.occupancyDuration[today]
    
    def get_type(self):
        return self.type
    
    def get_price(self, checkInDate, checkOutDate):
        return self.price * (checkOutDate - checkInDate)

    def get_id(self):
        return self.id
    
    def get_type_name(self):
        return Room.names_to_display[self.type]