from RoomType import RoomType

class Request:
    names_to_display = {
            RoomType.LUX: "Люкс",
            RoomType.HALF_LUX: "Полу-Люкс",
            RoomType.SINGLE: "Одна кровать",
            RoomType.SIMPLE_DOUBLE: "Две кровати",
            RoomType.DOUBLE_WITH_SOFA: "Две кровати с диваном"
    }
    def __init__(self, roomType, checkInDate, checkOutDate):
        self.roomType = roomType
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
    
    # GETTERS
    
    def get_time_info(self):
        return self.checkInDate, self.checkOutDate
    
    def get_room_name(self):
        return Request.names_to_display[self.roomType]
    
    def get_request_info(self):
        return self.roomType, self.checkInDate, self.checkOutDate
    
    def isRequest(self):
        return self.roomType != RoomType.NOT_A_ROOM