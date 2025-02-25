class Request:
    def __init__(self, roomType, checkInDate, checkOutDate):
        self.desiredRoomType = roomType
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate

    def validate(self):
        return self.checkInDate < self.checkOutDate
    
    def get_request_info(self):
        return f"Room Type : {self.desiredRoomType} \nCheck in date : day {self.checkInDate} \nCheck out date : day {self.checkOutDate}"