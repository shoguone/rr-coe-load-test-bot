import json
from typing import Callable
from runtime_context import RuntimeContext
from game_event_enum import GameEvent

class MessageProcessor():
    def __init__(self, player_id) -> None:
        self.player_id = player_id
        self.ctx = None
        self.handlers = {
            'on_choose_card': [],
            'on_play_card': [],
            'on_attack_target': [],
            'on_pass_turn': []
        }
    
    def get_runtime_context(self):
        return self.ctx

    def handle_single_message_event(self, message):
        message_type1_field = message.get('Type')
        message_type2_field = message.get('$type')
        event_type = None
        if message_type1_field is not None:
            event_type = message_type1_field
        if message_type2_field is not None:
            event_type = message_type2_field
        
        if event_type == GameEvent.InitializeGame.value:
            self.__handle_initialize_game(message)
        elif event_type == GameEvent.ChangeCardsState.value:
            self.__handle_change_cards_state(message)
        elif event_type == GameEvent.TurnGame.value:
            self.__handle_turn_game(message)
        elif event_type == GameEvent.ChangeObjectMoves.value \
            or event_type == GameEvent.ChangeAttackToHeroCount.value \
            or event_type == GameEvent.ChangePlayerMana.value \
            or event_type == GameEvent.ChangePlayerState.value \
            or event_type == GameEvent.EndGame.value \
            or event_type == GameEvent.TechnicalEndGame.value:
            print('\t', message)
        else:
            print('\t\tskip', message)

    def on_choose_card(self, callback_function: Callable):
        self.handlers['on_choose_card'].append(callback_function)

    def on_play_card(self, callback_function: Callable):
        self.handlers['on_play_card'].append(callback_function)

    def on_attack_target(self, callback_function: Callable):
        self.handlers['on_attack_target'].append(callback_function)

    def on_pass_turn(self, callback_function: Callable):
        self.handlers['on_pass_turn'].append(callback_function)

    def __handle_initialize_game(self, message):
        print("\tINIT signal")
        # f = open('initialize_game.json', 'w')
        # f.write(json.dumps(message))
        # f.close()
        # print('stored INIT to file')
        self.ctx = RuntimeContext(self.player_id, message)

    def __handle_change_cards_state(self, message):
        print('\t', message)
        card_ids = message['CardIds']
        new_state = message['NewState']
        for card in filter(lambda c: c.get_id() in card_ids, self.ctx.cards):
            card.set_state(new_state)
        
        if not self.ctx.is_player_turn():
            return

        player_choose_cards = list(filter(lambda c:
            c.is_owner_player() and c.is_state_in_choose(),
            self.ctx.cards))
        if len(player_choose_cards) > 0:
            card = player_choose_cards[0]
            self.__fire_event('on_choose_card', card.get_id())
            return

        player_all_table_cards = list(filter(lambda c:
            c.is_owner_player() and c.is_state_on_table(),
            self.ctx.cards))

        player_mana = self.ctx.player.get_mana()
        player_available_hand_cards = list(filter(lambda c:
            c.is_owner_player() and c.is_state_in_hand() and c.get_cost() < player_mana,
            self.ctx.cards))
        if len(player_available_hand_cards) > 0 and len(player_all_table_cards) < 6:
            card = player_available_hand_cards[0]
            self.__fire_event('on_play_card', card.get_id())
            return

        player_available_table_cards = list(filter(lambda c:
            c.has_attack_hero_moves() and c.has_moves(),
            player_all_table_cards))
        if len(player_available_table_cards) > 0:
            enemy_table_guardian_cards = list(filter(lambda c:
                not c.is_owner_player() and c.is_state_on_table() and c.is_guardian(),
                self.ctx.cards))
            target = enemy_table_guardian_cards[0] \
                if len(enemy_table_guardian_cards) > 0 \
                else list(filter(lambda h: not h.is_owner_player(), self.ctx.heroes))[0]
            self.__fire_event('on_attack_target', (card.get_id(), target.get_id()))
            return
        
        self.__fire_event('on_pass_turn')

    def __handle_turn_game(self, message):
        print('\t', message)
        owner_id = message['OwnerId']
        self.ctx.set_timer_owner(owner_id)
        print('  ** ' + ('MY turn' if self.ctx.is_player_turn() else 'ENEMY turn'))

    def __fire_event(self, event_name, argument = None):
        if argument is None:
            for handler in self.handlers[event_name]:
                handler()
        else:
            for handler in self.handlers[event_name]:
                handler(argument)
