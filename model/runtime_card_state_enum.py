from enum import Enum

class RuntimeCardState(Enum):
    InDeck = 'InDeck'
    InHand = 'InHand'
    InTable = 'InTable'
    InDiscard = 'InDiscard'
    InChoose = 'InChoose'
    InShow = 'InShow'
    InSacrifice = 'InSacrifice'
    InManualDiscard = 'InManualDiscard'
    InManualImmediatelyDiscard = 'InManualImmediatelyDiscard'
