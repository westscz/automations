from enum import Enum

class CardColor(Enum):
    RED=1
    GREEN=2
    BLUE=3
    YELLOW=4
    BLACK=5

class CardType(Enum):
    NORMAL=0
    STOP=1
    DIRECTION_CHANGE=2
    PLUS_TWO=3
    PLUS_FOUR=4
    COLOR_CHANGE=5

cards = []
for c in [CardColor.RED, CardColor.GREEN, CardColor.BLUE, CardColor.YELLOW]:
    for i in range(0,10):
        cards.append((c,i, CardType.NORMAL))
    for i in range(1,10):
        cards.append((c,i, CardType.NORMAL))

    for i in range(0,2):
        cards.append((c, None, CardType.STOP))
        cards.append((c, None, CardType.DIRECTION_CHANGE))
        cards.append((c, None, CardType.PLUS_TWO))

print(len(cards), (19*4)+(8*3))

for i in range(0,4):
    cards.append((CardColor.BLACK, None, CardType.PLUS_FOUR))
    cards.append((CardColor.BLACK, None, CardType.COLOR_CHANGE))

print(len(cards), 108)
