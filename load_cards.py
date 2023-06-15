import json

# cards2.json:
    # noble
        # price
            # BLACK, WHITE, ETC
    # deck
        # price
            # BLACK, WHITE, ETC
        # color
            # BLACK, WHITE, ETC
        # score
            # 1,2,3,4, etc

def load_cards(path_to_json=None):
    """
    Just loads cards from a .json file of cards
    Don't know if it is necessary to filter out noble or deck cards...
    ... There aren't really THAT many
    """
    if path_to_json == None: # Fuck everyone who says 'not path_to_json'
        path_to_json = 'cards_complete.json'

    f = open(path_to_json)
    cards = json.load(f)
    f.close()
    return cards


# for r, level in enumerate(cards['deck']):
#     curr_level = level[f'level{r+1}']
#     print(curr_level)
#     print(curr_level[0].values())
#     break
# #    for i, card in enumerate(level):
# #        print(card)
#         #print(card)
#         #if i == 4:
#         #    break