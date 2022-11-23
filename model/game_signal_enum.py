from enum import Enum

class GameSignal(Enum):
    Nothing = 'None'
    Ping = 'Ping'
    LobbyUpdate = 'LobbyUpdate'
    GameAction = 'GameAction'
    GameVisual = 'GameVisual'
    Direct = 'Direct'
    LogicEvents = 'LogicEvents'
    Colosseum = 'Colosseum'

    TimeOut = 'TimeOut'
    Error = 'Error'
    DropConnection = 'DropConnection'
