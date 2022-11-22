from threading import Thread
import time
from typing import Callable


class BehaviourProcessor():
    def __init__(self, player_id, runtime_context) -> None:
        self.player_id = player_id
        self.has_fired_mulligan = False
        self.ctx = runtime_context
        self.handlers = {
            'on_mulligan': [],
            'on_choose_card': [],
            'on_play_card': [],
            'on_attack_target': [],
            'on_pass_turn': []
        }

        self.worker_period_secs = 3
        self.worker_enemy_period_secs = 6
        self.stop_worker = False
        self.worker_thread = Thread(target=self.__worker_tick)

    def start(self):
        self.worker_thread.start()

    def on_mulligan(self, callback_function: Callable):
        self.handlers['on_mulligan'].append(callback_function)

    def on_choose_card(self, callback_function: Callable):
        self.handlers['on_choose_card'].append(callback_function)

    def on_play_card(self, callback_function: Callable):
        self.handlers['on_play_card'].append(callback_function)

    def on_attack_target(self, callback_function: Callable):
        self.handlers['on_attack_target'].append(callback_function)

    def on_pass_turn(self, callback_function: Callable):
        self.handlers['on_pass_turn'].append(callback_function)


    def __process(self):
        print('== process ==')

        if self.__try_perform_mulligan():
            return

        if not self.ctx.is_player_turn():
            print(' = not my turn')
            return

        if self.__try_perform_choose_card():
            return

        if self.__try_perform_play_card():
            return

        if self.__try_perform_attack_target():
            return

        self.__fire_event('on_pass_turn')

    def __try_perform_mulligan(self):
        if self.ctx.is_mulligan() and not self.has_fired_mulligan:
            self.has_fired_mulligan = True
            self.__fire_event('on_mulligan')
            return True
        return False

    def __try_perform_choose_card(self):
        player_choose_cards = list(filter(lambda c:
            c.is_owner_player() and c.is_state_in_choose(),
            self.ctx.cards))
        if len(player_choose_cards) > 0:
            card = player_choose_cards[0]
            self.__fire_event('on_choose_card', card.get_id())
            return True
        return False

    def __try_perform_play_card(self):
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
            return True
        return False

    def __try_perform_attack_target(self):
        player_all_table_cards = list(filter(lambda c:
            c.is_owner_player() and c.is_state_on_table(),
            self.ctx.cards))

        player_available_table_cards = list(filter(lambda c:
            c.has_attack_hero_moves() and c.has_moves(),
            player_all_table_cards))
        if len(player_available_table_cards) > 0:
            card = player_available_table_cards[0]
            enemy_table_guardian_cards = list(filter(lambda c:
                not c.is_owner_player() and c.is_state_on_table() and c.is_guardian(),
                self.ctx.cards))
            target = enemy_table_guardian_cards[0] \
                if len(enemy_table_guardian_cards) > 0 \
                else list(filter(lambda h: not h.is_owner_player(), self.ctx.heroes))[0]
            self.__fire_event('on_attack_target', (card.get_id(), target.get_id()))
            return True
        return False


    def __worker_tick(self):
        while not self.stop_worker:
            try:
                self.__process()
            except Exception as ex:
                print('!!! behaviour exception', ex)
            time.sleep(self.__get_tick_period())

    def __get_tick_period(self):
        return self.worker_period_secs \
            if self.ctx.is_player_turn() \
            else self.worker_enemy_period_secs

    def __fire_event(self, event_name, argument = None):
        if argument is None:
            for handler in self.handlers[event_name]:
                handler()
        else:
            for handler in self.handlers[event_name]:
                handler(argument)

    def stop(self):
        self.stop_worker = True
