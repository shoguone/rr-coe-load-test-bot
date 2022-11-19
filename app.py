import logging
import sys
sys.path.append("./")
from signalrcore.hub_connection_builder import HubConnectionBuilder
import requests
import json
from game_signal_enum import GameSignal

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

# game_signals = [
#     'None',
#     'Ping',
#     'LobbyUpdate',
#     'GameAction',
#     'GameVisual',
#     'Direct',
#     'LogicEvents',
#     'Colosseum',

#     'TimeOut',
#     'Error',
#     'DropConnection'
# ]

init_game_event = 'CoE.Shared.GameCore.LogicEvents.InitializeGame, CoE.Shared'

game_hub = None

def get_token():
    r = requests.post(url=login_url, json=login_data, verify=False)
    access_token = r.json()['accessToken']
    print('Login success, token: ' + access_token)
    return access_token

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
    print('messages type ', type(messages))
    message = messages[0]
    print('messages[0] type ', type(message))
    argObj = json.loads(message)
    # print('LobbyUpdate: ', argObj)

    action = argObj['Action']
    print('LobbyUpdate: Action: ' + action)
    if action == 'Started':
        print('STARTED!')
        lobby_hub.stop()
        init_game_hub()

def init_game_hub():
    print('gonna start game')
    game_hub = connect_to_hub(game_hub_url)

    def on_connected_to_game():
        print('connected to Game')
        print('game_hub type ', type(game_hub))
        print('gonna send ReadyToPlay')
        game_hub.send('ReadyToPlay', [])

    game_hub.on_open(on_connected_to_game)
    game_hub.on_close(lambda: print("Game closed"))
    # for signal_type in game_signals:
    for signal_type_enum in GameSignal:
        game_hub.on(signal_type_enum.name, \
            lambda msgs: on_game_message(signal_type_enum.name, msgs))
    game_hub.start()


def on_game_message(signal_type, message_list):
    print('got signal ' + signal_type)
    for message in message_list:
        # print('message', message)
        message_type = type(message)
        print('message type', message_type)
        if message_type is str:
            print('message is str, deserializing...')
            message = json.loads(message)

        message_type = type(message)
        if message_type is list:
            print('message is list, let`s see each item...')
            for item in message:
                item_type = type(item)
                print('item type', item_type)
                handle_single_message_event(item)
        elif message_type is dict:
            print('message is dict, OK')
            handle_single_message_event(message)

def handle_single_message_event(message):
    # message is supposed to be dict
    print('handle message')
    # print('handle message', message)
    message_type = type(message)
    print('message type', message_type)
    message_type1_field = message.get('Type')
    message_type2_field = message.get('$type')
    event_type = None
    if message_type1_field is not None:
        print('Type: ', message_type1_field)
        event_type = message_type1_field
    if message_type2_field is not None:
        print('$type: ', message_type2_field)
        event_type = message_type2_field
    
    if event_type == init_game_event:
        print("INIT!")


token = get_token()

lobby_hub = connect_to_hub(lobby_hub_url)

lobby_hub.on_open(on_connected_to_lobby)
lobby_hub.on_close(lambda: print("Lobby closed"))

lobby_hub.on("LobbyUpdate", on_lobby_update)
lobby_hub.start()

message = None

# Do login

while message != "exit()":
    message = input(">> ")
    if message is not None and message != "" and message != "exit()":
        lobby_hub.send("SendMessage", [message])

lobby_hub.stop()
game_hub.stop()

sys.exit(0)