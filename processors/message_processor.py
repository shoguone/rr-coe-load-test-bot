from typing import Callable

import logging_utility
from model.runtime_context import RuntimeContext
from model.game_event_enum import GameEvent

class MessageProcessor():
    def __init__(self, player_id: str) -> None:
        self.logger = logging_utility.create_file_logger(player_id, __name__)

        self.player_id = player_id

        self.ctx = None
        self.handlers = {
            'on_game_initialized': [],
            'on_card_state_changed': [],
            'on_end_game': []
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
        elif event_type == GameEvent.ChangeObjectMoves.value:
            self.__handle_change_object_moves(message)
        elif event_type == GameEvent.ChangeAttackToHeroCount.value:
            self.__handle_change_attack_to_hero_count(message)
        elif event_type == GameEvent.ChangePlayerMana.value:
            self.__handle_change_player_mana(message)
        elif event_type == GameEvent.EndGame.value \
            or event_type == GameEvent.TechnicalEndGame.value:
            self.__handle_end_game(message)
        else:
            self.logger.debug('\t\tskip %s', message)

    def on_game_initialized(self, callback_function: Callable):
        self.handlers['on_game_initialized'].append(callback_function)

    def on_card_state_changed(self, callback_function: Callable):
        self.handlers['on_card_state_changed'].append(callback_function)

    def on_end_game(self, callback_function: Callable):
        self.handlers['on_end_game'].append(callback_function)

    def __handle_initialize_game(self, message):
        self.logger.debug("\tINIT signal")
        self.ctx = RuntimeContext(self.player_id, message)
        self.__fire_event('on_game_initialized', self.ctx)

    def __handle_change_cards_state(self, message):
        self.logger.debug('\t%s', message)
        card_ids = message['CardIds']
        new_state = message['NewState']
        for card in filter(lambda c: c.get_id() in card_ids, self.ctx.cards):
            card.set_state(new_state)

        self.__fire_event('on_card_state_changed')

    def __handle_turn_game(self, message):
        self.logger.debug('\t%s', message)
        owner_id = message['OwnerId']
        state = message.get('State')
        self.ctx.set_timer_params(owner_id, state)
        self.logger.debug('  ** ' + ('MY turn' if self.ctx.is_player_turn() else 'ENEMY turn'))

    def __handle_change_object_moves(self, message):
        self.logger.debug('\t%s', message)
        runtime_id = message['Id']
        to = message['To']
        runtime_object = self.ctx.get_runtime_object_by_id(runtime_id)
        runtime_object.set_moves(to)

    def __handle_change_attack_to_hero_count(self, message):
        self.logger.debug('\t%s', message)
        runtime_id = message['Id']
        to = message['To']
        runtime_object = self.ctx.get_runtime_object_by_id(runtime_id)
        runtime_object.set_attack_hero_moves(to)

    def __handle_change_player_mana(self, message):
        self.logger.debug('\t%s', message)
        player_id = message['Id']
        to = message['To']
        player = self.ctx.player \
            if self.ctx.player.get_user_id() == player_id \
            else self.ctx.opponent
        player.set_mana(to)

    def __handle_end_game(self, message):
        self.logger.debug('\t%s', message)
        self.__fire_event('on_end_game')

    def __fire_event(self, event_name, argument = None):
        if argument is None:
            for handler in self.handlers[event_name]:
                handler()
        else:
            for handler in self.handlers[event_name]:
                handler(argument)
