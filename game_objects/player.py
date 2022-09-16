color_to_int = {
    'RED': 0,
    'GREEN': 1,
    'BLUE': 2,
    'BLACK': 3,
    'WHITE': 4
}

class Player:
    def __init__(self, id=0):
        self.id = id # Just to tell players apart
        # TODO: REPLACE THESE WITH [0] * 5/6?
        self.mines = [0,0,0,0,0] # RGBBW
        self.coins = [0,0,0,0,0,0] # RGBBW - GOLD
        self.points = 0
        self.has_noble = False
        self.reserved_cards = [] # Maybe [None] * 3 to prevent more than 3 reserved cards?
        self.board = None # The current game board that the player plays at
        self.taken_turn = False
        self.cards = [] # Supposed to hold game_object.card.Card objects

    def update_mines_and_points_and_nobles(self):
        """
        Call just to update the amount of...
        mines and points player has based on cards
        Also updates nobles now...
        """
        self.mines = [0] * 5
        self.points = 0
        for card in self.cards:
            self.mines[card.color] += 1
            self.points += card.points
            if self.has_noble:
                self.points += 3

        # If no nobles, check if they can geet a noble
        if not self.has_noble:
            for noble in self.board.nobles:
                if sum([max(0, nc - pm) for nc, pm in zip(noble.requirements, self.mines)]) == 0:
                    self.has_noble = True
                    # TODO: SOME MESSAGE HERE
                    # TODO: SOME METHOD TO GET THE PRECISE NOBLE PICTURE

    def take_coins(self, coins_to_take, one_hot=True):
        """
        :param coins_to_take:
        :param one_hot: Whether coins_to_take is given as a one-hot encoding vector
        :return:
        """

        if sum(self.coins) >= 10:
            print("Too many coins")
            return False

        # Add double numbers if one_hot
        if one_hot and 0 < sum(coins_to_take[:5]) < 3: # This shit ugly, np.nonzero would have worked fine
            double_grab = next((i for i, x in enumerate(coins_to_take) if x), None) # coin to grab doubble of
            if not self.board.coins[double_grab] < 2:
                self.coins[double_grab] += 2
                return True # Returns true to indicate turn has passed
            else:
                print("Not enough coins of that type to grab double!")
                return False

        offset = 5 * one_hot
        if sum([i for i, e in enumerate(coins_to_take[offset:]) if e != 0]) > 3:
            for i, r in enumerate(coins_to_take[offset:]):
                if self.board.coins[i] < r:
                    print("No enough coins of that type to grab")
                    return False
                self.coins[i] += r
            # Use walrus operator if possible?
            return True

        print("You're either getting too many coins, or too many of the same type!")
        return False


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
        self.board.remove_card(to_reserve)
        self.board.populate_board()
        self.coins[-1] += 1
        self.taken_turn = True

    def purchase_card(self, card_to_purchase, from_reserved):
        if from_reserved:
            card = self.reserved_cards[card_to_purchase]
        else:
            card = self.board.current_cards[card_to_purchase]


        # TODO: Check if that does it

        # First, subtract the player's current mines from the price, and check if they have enough in total
        # TODO: ROLL THESE TWO INTO ONE
        needed_coins = [max(0, cc - sm) for cc, sm in zip(card.cost, self.mines)]
        needed_gold = [max(0, cc - sc) for cc, sc in zip(needed_coins, self.coins[:-1])]
        if sum(needed_gold) > self.gold:
            print(f"You do not have enough coins, you need: \n {needed_gold[0]} red, \n {needed_gold[1]} green,"
                  f"\n {needed_gold[2]} blue, \n {needed_gold[3]} black, , \n {needed_gold[4]}.")
            return

        # If they have enough, subtract coins needed from their coin base
        else: # Not really necessary to use else?
            self.coins = [sc - max(0,nc) for sc, nc in zip(self.coins, needed_coins)]

        # Finally, we subtract the needed gold based on the 'gold debt'
        self.coins[-1] -= abs(sum([i for i in self.coins[:-1] if i<0]))

        self.cards.append(card)
        self.update_mines_and_points_and_nobles()

        self.board.remove_card(card) # Remove the added card
        self.board.populate_board() # Re-populate the board

        # current_cost = card.cost # To manipulate and check against
        # current_cost = [cc - sm for cc, sm in zip(card.cost, self.mines)]
        #
        # tmp_player_coins = [0,0,0,0,0]
        # for cost_type in enumerate(card.cost):
        #
        #
        # current_cost = [cc - sc for cc, sc in zip(card.cost, self.coins)]
        # for cost in enumerate(card.cost):
        #
        # for i, cost in enumerate(card.cost):
        #     if cost >= self.mines[i]:
        #         cost = cost - self.mines[i]
        #         if cost > self.coins[i]:
        #             diff = cost - self.coins[i]
        #             needed[i] = diff
        #
        #             gold_needed = cost - self.coins[i]
        #
        #
        #         diff = self.mines[i]
        #         gold_needed += diff
        #         needed[i] = max(0, cost - self.mines[i])
        #
        # if gold_needed > self.coins[-1]:
        #     print(f'Sorry, you cannot afford {card.cost}, you need {needed} or {gold_needed - self.coins[-1]} more gold coins')
        #     return
