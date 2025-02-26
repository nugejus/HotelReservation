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
        self.price = Room.prices[room_type]

        self.occupancyDuration = [False] * days

    def isAvailable(self, checkInDate, checkOutDate):
        return not any(self.occupancyDuration[checkInDate:checkOutDate])
    
    def checkIn(self, checkInDate, checkOutDate):
        for i in range(checkInDate, checkOutDate):
            self.occupancyDuration[i] = True
        return self

    def get_price(self, checkInDate, checkOutDate):
        return self.price * (checkOutDate - checkInDate)
    
    def displayRoomInfo(self):
        return  f"RoomId : {self.id} \n" + \
                f"RoomType : {Room.names_to_display[self.type]} \n" + \
                f"Price : {self.price} \n"
    
    def get_type(self):
        return self.type

    def isFree(self, today):
        return not self.occupancyDuration[today]