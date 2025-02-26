from RoomType import RoomType

class Room:
    prices = {
            RoomType.LUX: 120,
            RoomType.HALF_LUX: 100,
            RoomType.SINGLE: 70,
            RoomType.SIMPLE_DOUBLE: 80,
            RoomType.DOUBLE_WITH_SOFA: 90
        }
    def __init__(self, id, room_type):
        self.id = id
        self.type = room_type
        self.price = Room.prices[room_type]
        self.checkInDate = None
        self.checkOutDate = None

    def isAvailable(self, checkInDate):
        return self.isFree() or checkInDate > self.checkInDate
    
    def checkIn(self, checkInDate, checkOutDate):
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
        return self

    def checkOut(self):
        pass

    def get_price(self):
        return self.price * (self.checkOutDate - self.checkInDate)
    
    def displayRoomInfo(self):
        return  f"RoomId : {self.id} \n" + \
                f"RoomType : {self.type} \n" + \
                f"Price : {self.price} \n" + \
                f"CheckInDate : {self.checkInDate} \n" + \
                f"CheckOutDate : {self.checkOutDate}"
    
    def get_type(self):
        return self.type

    def isFree(self):
        return self.checkInDate is None and self.checkOutDate is None