class Request:
    def __init__(self, roomType, checkInDate, checkOutDate):
        self.roomType = roomType
        self.checkInDate = checkInDate
        self.checkOutDate = checkOutDate
    
    def display_request_info(self):
        return  f"Room Type : {self.roomType} \n" + \
                f"Check in date : day {self.checkInDate} \n" + \
                f"Check out date : day {self.checkOutDate}"
    
    def get_request_info(self):
        return self.roomType, self.checkInDate, self.checkOutDate