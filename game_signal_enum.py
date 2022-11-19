from enum import Enum

# class GameSignal(Enum):
GameSignal = Enum('GameSignal', [
    'None',
    'Ping',
    'LobbyUpdate',
    'GameAction',
    'GameVisual',
    'Direct',
    'LogicEvents',
    'Colosseum',

    'TimeOut',
    'Error',
    'DropConnection'
])

# print(GameSignal.Ping)
for gs in GameSignal:
    # print(type(gs))
    print(gs.name)