import tools

abomination = [[0] * i + [2] + [0] * (4-i) for i in range(5)] # abomination list comprehension
unique_combinations = list(abomination + tools.unique_combinations([0,1,2,3,4], r=3))

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
        self.legal_moves = self.get_legal_moves(existing_dict=False, one_hot=False)

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
        return self.legal_moves[coins_to_take]

    def reserve_card(self, to_reserve):
        if self.legal_moves[to_reserve] == True:
            self.reserved_cards.append(self.board.current_cards[to_reserve])
            self.board.remove_card(to_reserve)
            self.board.populate_board()
            self.coins[-1] += 1
            #self.taken_turn = True
            return True


    def check_if_can_purchase_card(self, card):
        needed_coins = [max(0, cc - sm) for cc, sm in zip(card.cost, self.mines)]
        needed_gold = [max(0, cc - sc) for cc, sc in zip(needed_coins, self.coins[:-1])]
        if sum(needed_gold) > self.gold:
            print(f"You do not have enough coins, you need: \n {needed_gold[0]} red, \n {needed_gold[1]} green,"
                  f"\n {needed_gold[2]} blue, \n {needed_gold[3]} black, , \n {needed_gold[4]}.")
            return False # Cannot purchase card

        return needed_coins
    def purchase_card(self, card_to_purchase, from_reserved):
        if from_reserved:
            card = self.reserved_cards[card_to_purchase]
        else:
            card = self.board.current_cards[card_to_purchase]

        needed_coins = self.legal_moves[len(self.board.current_cards) + card_to_purchase + from_reserved * 3]
        if not needed_coins:
            return False

        # If they have enough, subtract coins needed from their coin base
        else: # Not really necessary to use else?
            self.coins = [sc - max(0,nc) for sc, nc in zip(self.coins, needed_coins)]

        # Finally, we subtract the needed gold based on the 'gold debt'
        self.coins[-1] -= abs(sum([i for i in self.coins[:-1] if i<0]))

        self.cards.append(card)
        self.update_mines_and_points_and_nobles()

        if not from_reserved:
            self.board.remove_card(card) # Remove the added card
        else:
            self.reserved_cards.pop(card_to_purchase)

        self.board.populate_board() # Re-populate the board

    def get_legal_moves(self,existing_dict=None, one_hot=False):
        """
        :param one_hot: Whether or not to return the legal moves as a true one-hot encoding, or have the coin options
        # be one-hot vectors themselves
        :return: list of all legal moves the player can make
        """

        # JUST MAKE THE FUCKING DICTIONARY WHEN YOU'RE DOING IT ANYWAY
            # THIS IS TO RESET ALL VALUES TO FALSE, YOU DUNCE
        if existing_dict == None:
            all_moves = [0] * 52 # 12 reserve, 12 buy, 5 grab double, 10 grab single, 3 buy reserved cards
            all_moves = {i: False for i in range(27)} # Reserve cards, buy cards, buy reserved cards
            # OK SO WE REALLY DON'T NEED TO DO THESE TWO THINGS
            all_moves.update({i: False for i in [[0] * i + [2] + [0] * (4-i) for i in range(5)]}) # ARISE! CHILD OF BLASPHEMY!
            all_moves.update({i: False for i in unique_combinations}) # Grab 1 coin combinations
            # {0-26: buy/reserve cards, [0,0,i,0,0]: grab i coins from 3rd place}
            all_moves = {}
        else:
            all_moves = dict.fromkeys(self.legal_moves, False)

        # 0-12: reserve cards:
        num_cards = len(self.board.current_cards)
        if len(self.reserved_cards) > 3 and sum(self.coins) > 10:
            for i in range(num_cards):
                all_moves[i] = True

        offset = num_cards
        if not one_hot:
            # 13-27: buy cards from board or from reserved
            for i, card in enumerate(self.board.current_cards + self.reserved_cards):
                needed_coins = self.check_if_can_purchase_card(card)
                if needed_coins:
                    all_moves[offset + i] = needed_coins # if possible to buy the card, set as legal action
            offset += num_cards

            # 27-??: take coins
            if sum(self.coins) > 10:
                for p, combination in enumerate(unique_combinations):
                    r = 0 # When you really wanna do lists anymore
                    for i, coin in enumerate(combination):
                        if self.board.coins[i] >= coin:
                            r += 1
                    if r-1 == 5:
                        if not one_hot:
                            all_moves[combination] = True
                        else:
                            all_moves[p+offset] = True

        return all_moves

    def take_turn(self, move):
        """
        Change the state of the game based on a specific move
        :param move: Move to make, must correspond to a key in the self.legal_moves property
        :return:
        """

