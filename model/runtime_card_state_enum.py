from enum import Enum

class RuntimeCardState(Enum):
    InDeck = 0
    InHand = 1
    InTable = 2
    InDiscard = 3
    InChoose = 4
    InShow = 5
    InSacrifice = 6
    InManualDiscard = 7
    InManualImmediatelyDiscard = 8
