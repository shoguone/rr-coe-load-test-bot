class RuntimeObject():
    def __init__(self, runtime_object, player_id):
        self.runtime_object = runtime_object
        self.player_id = player_id

    def __str__(self) -> str:
        return str(self.runtime_object)

    def __is_type(self, type_to_check):
        data_type = self.runtime_object['$type']
        return data_type == type_to_check

    def get_id(self) -> int:
        id = self.runtime_object['Id']
        return id

    def is_hero(self):
        return self.__is_type('CoE.Shared.GameCore.Models.HeroRuntimeData, CoE.Shared')

    def is_card(self):
        return self.__is_type('CoE.Shared.GameCore.Models.CardRuntimeData, CoE.Shared')

    def is_pet(self):
        return self.__is_type('CoE.Shared.Data.EthernalRuntimeData, CoE.Shared')

    def belongs_to_user(self, user_id):
        owner_id = self.runtime_object['OwnerUserId']
        return owner_id == user_id

    def is_owner_player(self):
        return self.belongs_to_user(self.player_id)

