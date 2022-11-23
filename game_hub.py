import json
from typing import Callable

from model.cmd_params_model import CmdParamsModel
from model.game_signal_enum import GameSignal
from processors.behaviour_processor import BehaviourProcessor
from processors.message_processor import MessageProcessor
from signalr_hub_user import SignalRHubUser


class GameHub():
    def __init__(self, hub_user: SignalRHubUser, player_id) -> None:
        self.exit_handler = None
        self.player_id = player_id

        self.hub_user = hub_user
        self.hub_connection = hub_user.hub
        self.hub_connection.on_open(self.__on_connected_to_game)
        self.hub_connection.on_close(lambda: print("Game closed"))

        for signal_type_enum in GameSignal:
            self.hub_user.on(signal_type_enum.value, \
                lambda msgs: self.__on_game_message(signal_type_enum.value, msgs))

        self.message_processor = MessageProcessor(player_id)
        self.message_processor.on_game_initialized(self.__on_context_init)
        self.message_processor.on_end_game(self.__on_game_end)

    def start(self):
        self.hub_connection.start()

    def on_exit(self, callback: Callable):
        self.exit_handler = callback

    def __on_connected_to_game(self):
        print('connected to Game, sending ReadyToPlay...')
        self.hub_user.send('ReadyToPlay', [])

    def __on_context_init(self, context):
        self.behaviour_processor = BehaviourProcessor(self.player_id, context)

        self.behaviour_processor.on_mulligan(self.__send_mulligan)
        self.behaviour_processor.on_choose_card(self.__send_choose_card)
        self.behaviour_processor.on_play_card(self.__send_play_card)
        self.behaviour_processor.on_attack_target(self.__send_attack_target)
        self.behaviour_processor.on_pass_turn(self.__send_pass_turn)

        self.behaviour_processor.start()

    def __on_game_message(self, signal_type, message_list):
        print('--- got signal ' + signal_type)
        try:
            for message in message_list:
                message_type = type(message)
                if message_type is str:
                    message = json.loads(message)

                message_type = type(message)
                if message_type is list:
                    for item in message:
                        self.message_processor.handle_single_message_event(item)
                elif message_type is dict:
                    self.message_processor.handle_single_message_event(message)
        except Exception as ex:
            print('!!! __on_game_message exception', ex)

    def __on_game_end(self):
        print('Game End. Exiting...')
        self.behaviour_processor.stop()
        self.hub_connection.stop()
        if self.exit_handler is not None:
            self.exit_handler()

    def __send_mulligan(self):
        print(' * fire: on_mulligan')
        self.hub_user.send('PerformCommand',
            CmdParamsModel.create_mulligan_cmd_params())

    def __send_choose_card(self, card_id):
        print(' * fire: on_choose_card', card_id)
        self.hub_user.send('PerformCommand',
            CmdParamsModel.create_choose_card_cmd_params(card_id))

    def __send_play_card(self, card_id):
        print(' * fire: on_play_card', card_id)
        self.hub_user.send('PerformCommand',
            CmdParamsModel.create_play_card_cmd_params(card_id))

    def __send_attack_target(self, card_and_target_ids):
        print(' * fire: on_attack_target', *card_and_target_ids)
        self.hub_user.send('PerformCommand',
            CmdParamsModel.create_attack_target_cmd_params(*card_and_target_ids))

    def __send_pass_turn(self):
        print(' * fire: on_pass_turn')
        self.hub_user.send('PerformCommand',
            CmdParamsModel.create_pass_turn_cmd_params())
