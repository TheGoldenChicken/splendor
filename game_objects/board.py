
import random
from load_cards import load_cards
from game_objects.card import Card
from game_objects.noble import Noble

# TODO:
    # Find out why color_to_int and two functions are not 'missing' when only importing Board from this file... ;_;

color_to_int = {
    'RED': 0,
    'GREEN': 1,
    'BLUE': 2,
    'BLACK': 3,
    'WHITE': 4
}

def make_card(card_dict, level):
    cost = [0] * 5
    for color, price in card_dict['price'].items():
        cost[color_to_int[color]] = price
    color = card_dict['color']
    score = card_dict['score']
    return Card(level, cost, color, score)

def make_noble(noble_dict):
    cost = [0] * 5
    for color, price in noble_dict['price'].items():
        cost[color_to_int[color]] = price
    return Noble(cost)


class Board:
    def __init__(self):
        #self.current_cards = [[None] * 4] * 3 # cards on the table
        #self.current_cards = [[None] * 4 for _ in range(3)] # Why do it like this? - Python references are retarded, as am I
        self.current_cards = [None] * 12 # Simpler approach

        # self.bottom_cards = [None] * 4
        # self.middle_cards = [None] * 4
        # self.top_cards = [None] * 4

        self.deck = [None] * 3 # One for each level of cards
        self.nobles = [None] * 3
        self.noble_deck = []
        self.coins = [0,0,0,0,0,0] #RGBBW - GOLD

    def reset_coins(self, players):
        self.coins = [7,7,7,7,7,5] #RGBBW - GOLD

    def reset_board(self, specific_level=False):
        # if specific_level == False:
        #     self.current_cards = [[None] * 4] * 3
        # else:
        #     self.current_cards[specific_level] = [None] * 4
        self.current_cards = [None] * 12


    def reset_decks(self,cards, specific_level=False):
        # cards = load_cards() # Don't load cards every time since this might take time
        if not specific_level:
            for i, level in enumerate(cards['deck']):
                self.deck[i] = [make_card(card, i) for card in level[f'level{i+1}']]

    def reset_noble_deck(self, cards):
        self.noble_deck = [make_noble(noble) for noble in cards['noble']]

    def populate_board(self):
        """
        call after taking cards from board
        """
        # for i, stack in enumerate(self.current_cards):
        #     for r, card in enumerate(stack):
        #         if card == None:
        #             new_card = random.randint(0, len(self.deck[i])-1)
        #             self.current_cards[i][r] = self.deck[i][new_card] # Index deck by i because of levels of cards
        #             self.deck[i].pop(new_card) # Pycharm gives error since it thinks deck[i] holds a None type

        for i, card in enumerate(self.current_cards):
            if card == None:
                card_level = i // 4
                new_card = random.randint(0, len(self.deck[card_level])-1)
                self.current_cards[i] = self.deck[card_level][new_card]
                self.deck[card_level].pop(new_card)  # Pycharm gives error since it thinks deck[i] holds a None type

    def remove_card(self, card_to_remove):
        """
        Removes card based on its specific object
        """
        for i, card in enumerate(self.current_cards):
            if card == card_to_remove:
                self.current_cards[i] = None

    def get_nobles(self):
        curr_nobles = random.sample(range(0,len(self.noble_deck)), 3)
        self.nobles = [self.noble_deck[i] for i in curr_nobles]

    def init(self, cards):
        self.reset_decks(cards)
        self.reset_noble_deck(cards)
        self.get_nobles()
        self.populate_board()

#
# self.cards[i] = [card if card is not None
#      else self.deck[i][random.randint(0,len(self.deck[i])-1)] for card in stack]