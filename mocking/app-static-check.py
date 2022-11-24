import logging

from processors.message_processor import MessageProcessor
from my_mock import MyMock
from model.runtime_card import RuntimeCard

mock_instance = MyMock()
init_response = mock_instance.get_init_response()

my_id = '2d302546-46d1-433a-a535-dfe7eaf17510'

message_processor = MessageProcessor(my_id)
message_processor.handle_single_message_event(init_response)
context = message_processor.get_runtime_context()

message_processor.on_choose_card(lambda c:
    logging.debug('\tfire: on_choose_card', c))

message_processor.on_play_card(lambda c:
    logging.debug('\tfire: on_play_card', c))

message_processor.on_attack_target(lambda c, t:
    logging.debug('\tfire: on_attack_target', c, t))

message_processor.on_pass_turn(lambda:
    logging.debug('\tfire: on_pass_turn'))

for event in mock_instance.logic_events:
    message_processor.handle_single_message_event(event)

cards = context.cards
hand_cards = list(filter(RuntimeCard.is_state_in_hand, cards))
table_cards = list(filter(RuntimeCard.is_state_on_table, cards))
choose_cards = list(filter(RuntimeCard.is_state_in_choose, cards))
choose_my = list(filter(RuntimeCard.is_owner_player, choose_cards))

logging.debug('finish')