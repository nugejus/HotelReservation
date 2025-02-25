class Room:
    def __init__(self, id, room_type, price):
        self.id = id
        self.type = room_type
        self.price = price
        self.checkInDate = None
        self.checkOutDate = None

    def isAvailable(self, checkInDate, checkOutDate):
        if self.checkInDate is None and self.checkOutDate is None:
            return True
        return False
