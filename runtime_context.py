from typing import Tuple
from player_context import PlayerContext
from runtime_card import RuntimeCard
from runtime_object import RuntimeObject


class RuntimeContext():
    def __init__(self, player_id, init_game_message) -> None:
        self.self_id = player_id

        players_contexts = init_game_message['PlayerContexts']
        runtime_data = init_game_message['RuntimeData']

        self.player, self.opponent = self.__get_players(players_contexts)
        self.cards, self.heroes, self.pets = self.__get_runtime_data(runtime_data)

        self.timer_owner = self.player.get_user_id() \
            if self.player.get_is_first_mover() \
            else self.opponent.get_user_id()
        self.timer_state = 'Mulligan'
        print('  ** self.timer_owner', self.timer_owner)
    
    def is_player_turn(self):
        return self.timer_owner == self.self_id

    def is_mulligan(self):
        return self.timer_state == 'Mulligan'

    def set_timer_params(self, owner_id, state):
        self.timer_owner = owner_id
        self.timer_state = state

    def get_runtime_object_by_id(self, runtime_id):
        cards = list(filter(lambda c: c.get_id() == runtime_id, self.cards))
        if len(cards) > 0:
            return cards[0]

        heroes = list(filter(lambda h: h.get_id() == runtime_id, self.heroes))
        if len(heroes) > 0:
            return heroes[0]

        pets = list(filter(lambda p: p.get_id() == runtime_id, self.pets))
        if len(pets) > 0:
            return pets[0]

    def __get_players(self, players_contexts) -> Tuple[PlayerContext, PlayerContext]:
        player = None
        opponent = None
        for item in players_contexts:
            player_context = PlayerContext(item)
            if player_context.is_user_id(self.self_id):
                player = player_context
            else:
                opponent = player_context
        return player, opponent

    def __get_runtime_data(self, runtime_data) -> Tuple[list[RuntimeCard], list[RuntimeObject], list[RuntimeObject]]:
        cards = []
        heroes = []
        pets = []
        for item in runtime_data:
            runtime_object = RuntimeObject(item, self.self_id)
            if runtime_object.is_card():
                cards.append(RuntimeCard(item, self.self_id))
                del runtime_object
            elif runtime_object.is_hero():
                heroes.append(runtime_object)
            elif runtime_object.is_pet():
                pets.append(runtime_object)
        return cards, heroes, pets
