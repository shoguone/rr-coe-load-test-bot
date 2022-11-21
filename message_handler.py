import json
from runtime_card_state_enum import RuntimeCardState
from runtime_context import RuntimeContext
from game_event_enum import GameEvent

class MessageProcessor():
    def __init__(self) -> None:
        self.ctx = None
    
    def get_runtime_context(self):
        return self.ctx

    # todo : not needed
    def set_runtime_context(self, ctx):
        self.ctx = ctx

    def handle_single_message_event(self, message):
        message_type1_field = message.get('Type')
        message_type2_field = message.get('$type')
        event_type = None
        type_prefix = "Type"
        if message_type1_field is not None:
            # print('+ Type: ', message_type1_field)
            event_type = message_type1_field
        if message_type2_field is not None:
            # print('+ $type: ', message_type2_field)
            type_prefix = '$type'
            event_type = message_type2_field
        
        if event_type == GameEvent.InitializeGame.value:
            self.__handle_initialize_game(message)
        elif event_type == GameEvent.ChangeCardsState.value:
            self.__handle_change_cards_state(message)
        elif event_type == GameEvent.TurnGame.value:
            self.__handle_turn_game(message)
        elif event_type == GameEvent.ChangeCardsState.value \
            or event_type == GameEvent.ChangeObjectMoves.value \
            or event_type == GameEvent.ChangeAttackToHeroCount.value \
            or event_type == GameEvent.ChangePlayerMana.value \
            or event_type == GameEvent.ChangePlayerState.value \
            or event_type == GameEvent.EndGame.value \
            or event_type == GameEvent.TechnicalEndGame.value:
            print(message)
        else:
            print('+ ' + type_prefix + ':', event_type)

    def __handle_initialize_game(self, message):
        print("INIT!")
        # f = open('initialize_game.json', 'w')
        # f.write(json.dumps(message))
        # f.close()
        # print('stored INIT to file')
        self.ctx = RuntimeContext(message)

    def __handle_change_cards_state(self, message):
        print(message)
        card_ids = message['CardIds']
        new_state = message['NewState']
        for card in filter(lambda c: c.get_id() in card_ids, self.ctx.cards):
            card.set_state(new_state)
        
        if new_state == RuntimeCardState.InChoose:
            print('mulligan or choose')
        elif new_state == RuntimeCardState.InHand:
            print('playable cards in hand')
        elif new_state == RuntimeCardState.InTable:
            print('playable cards on table')

        # if my turn
        # extract all hand and table cards
        # check mana for hand
        # check moves for table

    def __handle_turn_game(self, message):
        print(message)
        owner_id = message['OwnerId']
        state = message['State']