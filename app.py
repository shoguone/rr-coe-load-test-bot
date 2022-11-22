import json
import logging
import os
import signal
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
import sys
from game_hub import GameHub
sys.path.append("./")

base_url = 'https://localhost:7194'
lobby_hub_url = base_url + '/hubs/lobby'
game_hub_url = base_url + '/hubs/game'
login_url = base_url + '/api/v1/Identity/Login'
sign_auto_url = base_url + '/api/v1/Lobby/SignForAutoMatch'

class App():
    def __init__(self, login_url, login_data) -> None:
        self.login_url = login_url
        self.login_data = login_data
        self.current_hub_connection = None

    def start(self):
        self.__request_log_in()
        print('Login success, user id:', self.player_id, 'token:', self.access_token)

        self.current_hub_connection = self.__init_lobby_hub()

        self.__read()

    def __init_lobby_hub(self):
        lobby_hub = self.__connect_to_hub(lobby_hub_url)

        lobby_hub.on_open(self.__on_connected_to_lobby)
        lobby_hub.on_close(lambda: print("Lobby closed"))

        lobby_hub.on("LobbyUpdate", self.__on_lobby_update)
        lobby_hub.start()
        return lobby_hub

    def __init_game_hub(self):
        print('Connecting to GameHub...')
        game_hub_connection = self.__connect_to_hub(game_hub_url)
        game_hub = GameHub(game_hub_connection, self.player_id)
        game_hub.on_exit(self.__exit)
        game_hub.start()
        return game_hub_connection

    # handler = logging.StreamHandler()
    # handler.setLevel(logging.DEBUG)
    def __connect_to_hub(self, url):
        return HubConnectionBuilder()\
            .with_url(url, options={
                "access_token_factory": lambda: self.access_token,
                "verify_ssl": False
            }) \
            .with_automatic_reconnect({
                "type": "interval",
                "keep_alive_interval": 10,
                "intervals": [1, 3, 5, 6, 7, 87, 3]
            }) \
            .build()
            # .configure_logging(logging.DEBUG, socket_trace=True, handler=handler)

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
        r = requests.post(
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
        r = requests.post(url=sign_auto_url, json=payload, headers=headers, verify=False)
        print('sign_for_auto_match: ', r)

    def __read(self):
        message = None
        while message != "exit()":
            message = input()
            args = message.split()
            if len(args) > 0 and message != "exit()":
                method = args[0]
                self.current_hub_connection.send(method, args[1:])

        self.current_hub_connection.stop()
        sys.exit(0)

    def __exit(self):
        print('killing the process... SIGINT')
        os.kill(os.getpid(), signal.SIGINT)

email = 'player7@vovaa'
password = 'vovaa'
if len(sys.argv) > 1:
    email = sys.argv[1]
if len(sys.argv) > 2:
    password = sys.argv[2]

print(email)

login_data = {
    'email': email,
    'password': password
}

app = App(login_url, login_data)
app.start()
