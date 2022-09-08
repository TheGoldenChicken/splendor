color_to_int = {
    'RED': 0,
    'GREEN': 1,
    'BLUE': 2,
    'BLACK': 3,
    'WHITE': 4
}

class Player:
    def __init__(self):
        self.mines = [0,0,0,0,0] # RGBBW
        self.coins = [0,0,0,0,0,0] # RGBBW - GOLD
        self.points = 0
        self.has_noble = False
        self.reserved_cards = [] # Maybe [None] * 3 to prevent more than 3 reserved cards?
        self.board = None
        self.taken_turn = False

    def reserve_card(self, to_reserve):
        if len(self.reserved_cards) >= 3:
            print('Too many reserved cards')
            return
        if self.board.coins[-1] <= 0:
            print('Not enough gold coins')
            return
        if sum(self.coins) >= 10:
            print('Too many coins')
            return

        self.reserved_cards.append(self.board.current_cards[to_reserve])
        self.coins[-1] += 1
        self.taken_turn = True
    def purchase_card(self, card_to_purchase, from_reserved):
        if from_reserved:
            card = self.reserved_cards[card_to_purchase]
        else:
            card = self.board.current_cards[card_to_purchase]


        # TODO: FIX THIS TERRIBLE SHITE
        gold_needed = 0
        needed = [0,0,0,0,0]
        for i, cost in enumerate(card.cost):
            if cost >= self.mines[i]:
                cost = cost - self.mines[i]
                if cost > self.coins[i]:
                    diff = cost - self.coins[i]
                    needed[i] = diff

                    gold_needed = cost - self.coins[i]


                diff = self.mines[i]
                gold_needed += diff
                needed[i] = max(0, cost - self.mines[i])

        if gold_needed > self.coins[-1]:
            print(f'Sorry, you cannot afford {card.cost}, you need {needed} or {gold_needed - self.coins[-1]} more gold coins')
            return
