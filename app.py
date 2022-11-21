import json
import logging
import requests
from signalrcore.hub_connection_builder import HubConnectionBuilder
import sys
sys.path.append("./")

from game_signal_enum import GameSignal
from message_handler import MessageProcessor

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

base_url = 'https://localhost:7194'
lobby_hub_url = base_url + '/hubs/lobby'
game_hub_url = base_url + '/hubs/game'
login_url = base_url + '/api/v1/Identity/Login'
sign_auto_url = base_url + '/api/v1/Lobby/SignForAutoMatch'

game_hub = None

local_context = {}

def log_in():
    r = requests.post(url=login_url, json=login_data, verify=False)
    response_json = r.json()
    access_token = response_json['accessToken']
    id = response_json['id']
    return id, access_token

def sign_for_auto_match(game_mode):
    print('Signing for ' + game_mode + ' match...')
    headers = { "Authorization": 'Bearer ' + token }
    payload = { "gameMode": game_mode }
    r = requests.post(url=sign_auto_url, json=payload, headers=headers, verify=False)
    print('sign_for_auto_match: ', r)

# handler = logging.StreamHandler()
# handler.setLevel(logging.DEBUG)
def connect_to_hub(url):
    return HubConnectionBuilder()\
        .with_url(url, options={
            "access_token_factory": lambda: token,
            "verify_ssl": False
        }) \
        .with_automatic_reconnect({
            "type": "interval",
            "keep_alive_interval": 10,
            "intervals": [1, 3, 5, 6, 7, 87, 3]
        }) \
        .build()
        # .configure_logging(logging.DEBUG, socket_trace=True, handler=handler)

def on_connected_to_lobby():
    print('Connected to Lobby')
    sign_for_auto_match('Casual')

def on_lobby_update(messages):
    print('got LobbyUpdate')
    message = messages[0]
    argObj = json.loads(message)

    action = argObj['Action']
    print('LobbyUpdate: Action: ' + action)
    if action == 'Started':
        print('Lobby: STARTED! Connecting to game hub...')
        lobby_hub.stop()
        init_game_hub()

def init_game_hub():
    print('gonna start game')
    game_hub = connect_to_hub(game_hub_url)

    def on_connected_to_game():
        print('connected to Game, sending ReadyToPlay...')
        game_hub.send('ReadyToPlay', [])

    game_hub.on_open(on_connected_to_game)
    game_hub.on_close(lambda: print("Game closed"))
    for signal_type_enum in GameSignal:
        game_hub.on(signal_type_enum.value, \
            lambda msgs: on_game_message(signal_type_enum.value, msgs))
    game_hub.start()


def on_game_message(signal_type, message_list):
    print('--- got signal ' + signal_type)
    for message in message_list:
        message_type = type(message)
        if message_type is str:
            message = json.loads(message)

        message_type = type(message)
        if message_type is list:
            for item in message:
                # item_type = type(item)
                handle_single_message_event(item)
        elif message_type is dict:
            handle_single_message_event(message)

def handle_single_message_event(message):
    message_processor = local_context.get('message_processor')
    if message_processor is None:
        message_processor = MessageProcessor()
        local_context['message_processor'] = message_processor
    message_processor.handle_single_message_event(message)


user_id, token = log_in()
print('Login success, user id:', user_id, 'token:', token)

lobby_hub = connect_to_hub(lobby_hub_url)

lobby_hub.on_open(on_connected_to_lobby)
lobby_hub.on_close(lambda: print("Lobby closed"))

lobby_hub.on("LobbyUpdate", on_lobby_update)
lobby_hub.start()

message = None

# Do login

while message != "exit()":
    message = input()
    args = message.split()
    if len(args) > 0 and message != "exit()":
        method = args[0]
        lobby_hub.send(method, message[1:])

lobby_hub.stop()
game_hub.stop()

sys.exit(0)