import re
from runtime_card_state_enum import RuntimeCardState
from runtime_object import RuntimeObject

class RuntimeCard(RuntimeObject):
    # COE-0000005-Card-Creature search by regex
    def is_creature(self):
        data_id = self.runtime_object['DataId']
        m = re.match('COE-\d{7}-Card-Creature', data_id)
        return m is not None

    def __is_state(self, state):
        return self.runtime_object.get('State') == state

    def is_state_in_hand(self):
        return self.__is_state(self.runtime_object, RuntimeCardState.InHand.value)

    def is_state_in_deck(self):
        return self.__is_state(self.runtime_object, RuntimeCardState.InDeck.value)

    def has_imposing_effect(self, effect_name):
        imposing_effects = self.runtime_object.get('ImposingEffects')
        if imposing_effects is None or len(imposing_effects) < 1:
            return False
        return effect_name in imposing_effects

    def is_guardian(self):
        return self.has_imposing_effect('Guardian')

    def get_cost(self):
        mana = self.runtime_object.get('Mana')
        return 0 if mana is None else mana['Current']

    def set_state(self, state):
        if 'State' in self.runtime_object.keys():
            self.runtime_object['State'] = state
