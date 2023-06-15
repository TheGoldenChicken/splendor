from game_objects.board import Board
from load_cards import load_cards
import game_objects

new_board = Board()

cards = load_cards()
new_board.init(cards)

class splendor_env:

    def __init__(self,num_players=2, init=False):

        self.board = Board()
        self.players = []
        if init:
            self.cards = load_cards()
            self.board.init(self.cards)
            for i in range(num_players):
                self.players.append(game_objects.player.Player(id=i))

    def reset(self):
        """
        Resets game, use after each episode
        :return:
        """
        # TODO: This function ugly :(((((( maek pretty plox
        self.board.init(cards)
        for player in self.players:
            player.board = self.board
            player.cards = []
            player.reserved_cards = []
            player.has_noble = False
            player.taken_turn = False
            player.update_mines_and_points_and_nobles()

    def init_render(self):
        pass

    def render(self):
        pass

    def step(self):
        # Ok, so there's a major problem here:
        # Basically the step function needs to take one round of input for each player representing their actions
        # Basically a one-hot encoding of what they're gonna do...
        # But, if they make an illegal move, there is no way to have them do anything else
        # UNLESS, if they make an illegal move, we just have them do a random move...
        for current_player in self.players:
            while not current_player.taken_turn:


        pass