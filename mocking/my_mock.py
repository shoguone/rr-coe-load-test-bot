import json

class MyMock:
    def __init__(self):
        init_response_f = open('init-response.json', 'r')
        init_response_str = init_response_f.read()
        self.init_response = json.loads(init_response_str)
        self.logic_events = [
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 0, 'NewState': 4, 'CardIds': [265, 270, 286, 314, 315, 304, 305]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 4, 'NewState': 1, 'CardIds': [314, 315, 304, 305]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 4, 'NewState': 1, 'CardIds': [265, 270, 286]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 260},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 260},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangePlayerMana, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': '2b3d5a7e-2219-4e91-85c9-1b82f871e132'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': 292},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': 292},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.TurnGame, CoE.Shared', 'EndTime': '2022-11-21T12:11:08.8466734Z', 'Turn': 2, 'Round': 1, 'OwnerId': '2b3d5a7e-2219-4e91-85c9-1b82f871e132', 'State': 'Game'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 0, 'NewState': 4, 'CardIds': [297, 301]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 4, 'NewState': 4, 'CardIds': [297]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangePlayerMana, CoE.Shared', 'Max': 1, 'From': 1, 'To': 6, 'Id': '2b3d5a7e-2219-4e91-85c9-1b82f871e132'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangePlayerMana, CoE.Shared', 'Max': 1, 'From': 6, 'To': 1, 'Id': '2b3d5a7e-2219-4e91-85c9-1b82f871e132'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 315},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 315},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 1, 'NewState': 2, 'CardIds': [315]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 0, 'NewState': 4, 'CardIds': [322]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 0, 'To': 0, 'Id': 315},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 0, 'To': 0, 'Id': 315},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 292},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 292},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangePlayerMana, CoE.Shared', 'Max': 2, 'From': 1, 'To': 2, 'Id': '2d302546-46d1-433a-a535-dfe7eaf17510'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': 260},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeAttackToHeroCount, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': 260},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.TurnGame, CoE.Shared', 'EndTime': '2022-11-21T12:12:11.8674469Z', 'Turn': 3, 'Round': 2, 'OwnerId': '2d302546-46d1-433a-a535-dfe7eaf17510', 'State': 'Game'},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 0, 'NewState': 4, 'CardIds': [279, 276]},
            {'$type': 'CoE.Shared.GameCore.LogicEvents.TechnicalEndGame, CoE.Shared', 'Reason': 'Afk', 'LooserId': '2d302546-46d1-433a-a535-dfe7eaf17510', 'WinnerId': '2b3d5a7e-2219-4e91-85c9-1b82f871e132'}
        ]

    def get_init_response(self):
        return self.init_response