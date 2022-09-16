
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
    # Add -v options to basically every functino to prevent RL agent spamming console

# Press the green button in the gutter to run the script.
# if __name__ == '__main__':
#     print_hi('PyCharm')
#
