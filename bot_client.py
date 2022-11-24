import json
import time

from config import Config
from game_hub import GameHub
import logging_utility
from signalr_hub_user import SignalRHubUser

class BotClient():
    def __init__(self, base_url, login_data, http_client, hub_user: SignalRHubUser) -> None:
        self.lobby_hub_url = base_url + Config.lobby_hub_path
        self.game_hub_url = base_url + Config.game_hub_path
        self.login_url = base_url + Config.login_path
        self.sign_auto_url = base_url + Config.sign_auto_path

        self.http_client = http_client
        self.hub_user = hub_user

        self.login_data = login_data
        self.current_hub_connection = None

    def start(self):
        self.__request_log_in()

        self.logger = logging_utility.create_file_logger(self.player_id, __name__)

        self.logger.info('Login success, user id: %s; token: %s', self.player_id, self.access_token)

        self.current_hub_connection = self.__init_lobby_hub()

        self.is_waiting = True
        self.__wait()

    def stop(self):
        self.logger.debug('bot STOP')
        self.is_waiting = False
        self.current_hub_connection.stop()

    def __init_lobby_hub(self):
        lobby_hub = self.hub_user.connect_to_hub(self.lobby_hub_url, self.access_token)

        lobby_hub.on_open(self.__on_connected_to_lobby)
        lobby_hub.on_close(lambda: self.logger.debug("Lobby closed"))

        self.hub_user.on("LobbyUpdate", self.__on_lobby_update)
        lobby_hub.start()
        return lobby_hub

    def __init_game_hub(self):
        self.logger.debug('Connecting to GameHub...')
        game_hub_connection = self.hub_user.connect_to_hub(self.game_hub_url, self.access_token)
        game_hub = GameHub(self.hub_user, self.player_id)
        game_hub.on_exit(self.stop)
        game_hub.start()
        return game_hub_connection

    def __on_connected_to_lobby(self):
        self.logger.debug('Connected to Lobby')
        response = self.__request_sign_for_auto_match('Casual')
        if not response.ok:
            self.stop()

    def __on_lobby_update(self, messages):
        self.logger.debug('got LobbyUpdate')
        message = messages[0]
        argObj = json.loads(message)

        action = argObj['Action']
        self.logger.debug('LobbyUpdate: Action: ' + action)
        if action == 'Started':
            self.logger.debug('Lobby: STARTED! Connecting to game hub...')
            self.current_hub_connection.stop()
            self.current_hub_connection = self.__init_game_hub()

    def __request_log_in(self):
        r = self.http_client.post(
                url=self.login_url,
                json=self.login_data,
                verify=False)
        response_json = r.json()
        self.player_id = response_json['id']
        self.access_token = response_json['accessToken']

    def __request_sign_for_auto_match(self, game_mode):
        self.logger.debug('Signing for ' + game_mode + ' match...')
        headers = { "Authorization": 'Bearer ' + self.access_token }
        payload = { "MatchMode": game_mode }
        r = self.http_client.post(url=self.sign_auto_url, json=payload, headers=headers, verify=False)
        self.logger.debug('sign_for_auto_match: %s', r)
        return r

    def __wait(self):
        while self.is_waiting:
            time.sleep(5)
