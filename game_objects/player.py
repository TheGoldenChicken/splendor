
class Player:
    def __init__(self):
        self.mines = []
        self.points = 0
        self.has_noble = False
        self.reserved_cards = [] # Maybe [None] * 3 to prevent more than 3 reserved cards?