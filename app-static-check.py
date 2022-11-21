from message_handler import MessageProcessor
from runtime_context import RuntimeContext
from my_mock import MyMock
from runtime_card import RuntimeCard

mock_instance = MyMock()
init_response = mock_instance.get_init_response()

my_id = '2d302546-46d1-433a-a535-dfe7eaf17510'

context = RuntimeContext(my_id, init_response)

# print('len(runtime_data)', len(runtime_data))
print('len(cards)', len(context.cards))
print('len(heroes)', len(context.heroes))
print('len(pets)', len(context.pets))

# find all creatures with state
creatures = list(filter(RuntimeCard.is_creature, context.cards))
print('len(creatures)', len(creatures))

guardians = list(filter(RuntimeCard.is_guardian, context.cards))
print('len(guardians)', len(guardians))

# ChangeCardsState {"OldState":4,"NewState":4,"CardIds":[532]}
# ChangeObjectMoves {"Max":1,"From":1,"To":0,"Id":512}
# ChangeAttackToHeroCount {"Max":1,"From":1,"To":0,"Id":512}
# ChangePlayerMana {"Max":2,"From":0,"To":2,"Id":"2b3d5a7e-2219-4e91-85c9-1b82f871e132"}
# TurnGame {"EndTime":"2022-11-18T13:26:10.574325Z","Turn":3,"Round":2,"OwnerId":"2b3d5a7e-2219-4e91-85c9-1b82f871e132","State":"Game"}

change_cards_state = {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeCardsState, CoE.Shared', 'OldState': 0, 'NewState': 4, 'CardIds': [265, 270, 286, 314, 315, 304, 305]}
change_object_moves = {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangeObjectMoves, CoE.Shared', 'Max': 1, 'From': 1, 'To': 0, 'Id': 260}
change_player_mana = {'$type': 'CoE.Shared.GameCore.LogicEvents.ChangePlayerMana, CoE.Shared', 'Max': 1, 'From': 0, 'To': 1, 'Id': '2b3d5a7e-2219-4e91-85c9-1b82f871e132'}
turn_game = {'$type': 'CoE.Shared.GameCore.LogicEvents.TurnGame, CoE.Shared', 'EndTime': '2022-11-21T12:11:08.8466734Z', 'Turn': 2, 'Round': 1, 'OwnerId': '2b3d5a7e-2219-4e91-85c9-1b82f871e132', 'State': 'Game'}

msg_proc = MessageProcessor(context)
msg_proc.handle_single_message_event(change_cards_state)