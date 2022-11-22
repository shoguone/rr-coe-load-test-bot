import json
import random


class CmdParamsModel():
    def __init__(self, executor_id: int, target_ids: list[int]) -> None:
        self.id = random.randrange(0, 2**31-1)
        self.executor_id = executor_id
        self.target_ids = target_ids
        self.meta = None

    def __str__(self) -> str:
        json_obj = {
            "Id": self.id,
            "ExecutorObjectId": self.executor_id,
            "TargetObjectsIds": self.target_ids,
            "MetaJson": self.meta,
        }
        return json.dumps(json_obj)

    def set_meta_str(self, meta_str):
        self.meta = meta_str

    def set_meta_obj(self, meta_obj):
        self.meta = json.dumps(meta_obj)

    @staticmethod
    def create_mulligan_cmd_params():
        return ['MulliganReplaceCardsCmd', ""]

    @staticmethod
    def create_choose_card_cmd_params(card_id):
        return ['ChooseCardCmd', str(CmdParamsModel(card_id, [card_id]))]

    @staticmethod
    def create_play_card_cmd_params(card_id):
        params = CmdParamsModel(card_id, [])
        params.set_meta_obj({ "RelativePositionX": 0 })
        return ['PlayCardCmd', str(params)]

    @staticmethod
    def create_attack_target_cmd_params(card_id, target_id):
        params = CmdParamsModel(card_id, [target_id])
        params.set_meta_obj({ "EffectDataId": 'GenericAttack' })
        return ['PerformEffectCmd', str(params)]

    @staticmethod
    def create_pass_turn_cmd_params():
        return ['PassTurnCmd', ""]

