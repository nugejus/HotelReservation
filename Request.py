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
    
    def display_request_info(self):
        if self.roomType != RoomType.NOT_A_ROOM:
            return  f"Room Type : {Request.names_to_display[self.roomType]} \n" + \
                    f"Check in date : day {self.checkInDate} \n" + \
                    f"Check out date : day {self.checkOutDate}"
        else:
            return "Nobody wants to stay in Our Hotel...."
    
    def get_request_info(self):
        return self.roomType, self.checkInDate, self.checkOutDate