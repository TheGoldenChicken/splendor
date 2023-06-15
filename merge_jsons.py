import json
from load_cards import load_cards
import os

cards1 = load_cards(os.getcwd() + '/cards.json')
cards2 = load_cards(os.getcwd() + '/cards2.json')

# Merge the cards first, the the nobles

check = [[[i['score'], i['color'], i['price']] for i in cards1['deck'][r][f'level{r+1}']]
         for r in range(len(cards1['deck']))] # Ugly AF, never remind me of this again

for i, level in enumerate(cards2['deck']):
    for card in level[f'level{i+1}']:
        if card not in check[i]:
            cards1['deck'][i][f'level{i+1}'].append(card)


with open("cards_complete.json", "w") as outfile:
    json.dump(cards1, outfile, indent=2)
    outfile.close()


