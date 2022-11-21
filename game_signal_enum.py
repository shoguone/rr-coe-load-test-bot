from enum import Enum

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
