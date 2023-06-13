class SmartCard:
    def __init__(self, card_id, balance=0):
        self.card_id = card_id
        self.balance = balance
        self.stations_visited = 0

    def top_up(self, amount):
        self.balance += amount

    def calculate_fare(self, stations):
        fare = 15 + 5 * max(stations - 3, 0)
        discount = (self.stations_visited // 5) * 0.05 * fare
        return fare - discount

    def deduct_fare(self, fare):
        self.balance -= fare
        self.stations_visited += 1