
import game_objects.board
from load_cards import load_cards

cards = load_cards()

new_board = game_objects.board.Board()

new_board.reset_decks(cards)
new_board.reset_noble_deck(cards)

new_board.get_nobles()
new_board.populate_board()

print(new_board.nobles)

for noble in new_board.nobles:
    print(noble.requirements)


# TODO:
    # add .config file so all settings can be changed
    # Consider whether adding a splendor_env is kinda superflous?
    # add pysimplegui to actually play the damn game
    # Roll board.remove_card and board.populate_board into one?
    # Update everything to use numpy arrays?
        # Make new version probably
    # Add -v options to basically every function to prevent RL agent spamming console
    # Consider what all the list comprehensions is actually doing, every lc creates a new list and possibly throws it away again
        # For loops for assignments, lc for creating lists
    # Consider killing the abomination of player.py
        # Not the entire class, just the abomination
