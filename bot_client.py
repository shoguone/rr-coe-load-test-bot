import json
import time

from game_hub import GameHub
from signalr_hub_user import SignalRHubUser


class BotClient():
    def __init__(self, base_url, login_data, http_client, hub_user: SignalRHubUser) -> None:
        self.lobby_hub_url = base_url + '/hubs/lobby'
        self.game_hub_url = base_url + '/hubs/game'
        self.login_url = base_url + '/api/v1/Identity/Login'
        self.sign_auto_url = base_url + '/api/v1/Lobby/SignForAutoMatch'

        self.http_client = http_client
        self.hub_user = hub_user

        self.login_data = login_data
        self.current_hub_connection = None

    def start(self):
        self.__request_log_in()
        print('Login success, user id:', self.player_id, 'token:', self.access_token)

        self.current_hub_connection = self.__init_lobby_hub()

        self.is_waiting = True
        self.__wait()

    def stop(self):
        print('bot STOP')
        self.is_waiting = False
        self.current_hub_connection.stop()

    def __init_lobby_hub(self):
        lobby_hub = self.hub_user.connect_to_hub(self.lobby_hub_url, self.access_token)

        lobby_hub.on_open(self.__on_connected_to_lobby)
        lobby_hub.on_close(lambda: print("Lobby closed"))

        self.hub_user.on("LobbyUpdate", self.__on_lobby_update)
        lobby_hub.start()
        return lobby_hub

    def __init_game_hub(self):
        print('Connecting to GameHub...')
        game_hub_connection = self.hub_user.connect_to_hub(self.game_hub_url, self.access_token)
        game_hub = GameHub(self.hub_user, self.player_id)
        game_hub.on_exit(self.stop)
        game_hub.start()
        return game_hub_connection

    def __on_connected_to_lobby(self):
        print('Connected to Lobby')
        self.__request_sign_for_auto_match('Casual')

    def __on_lobby_update(self, messages):
        print('got LobbyUpdate')
        message = messages[0]
        argObj = json.loads(message)

        action = argObj['Action']
        print('LobbyUpdate: Action: ' + action)
        if action == 'Started':
            print('Lobby: STARTED! Connecting to game hub...')
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
        print('Signing for ' + game_mode + ' match...')
        headers = { "Authorization": 'Bearer ' + self.access_token }
        payload = { "gameMode": game_mode }
        r = self.http_client.post(url=self.sign_auto_url, json=payload, headers=headers, verify=False)
        print('sign_for_auto_match: ', r)

    def __wait(self):
        while self.is_waiting:
            # print('? wait iter')
            time.sleep(5)
