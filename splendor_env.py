from game_objects.board import Board
from load_cards import load_cards

new_board = Board()

cards = load_cards()
new_board.init(cards)

class splendor_env:

    def __init__(self, init=False):

        self.board = Board()
        self.players = []
        if init:
            self.cards = load_cards()
            self.board.init(self.cards)

