class PlayerContext():
    def __init__(self, player_data) -> None:
        self.player_data = player_data

    def __str__(self) -> str:
        return str(self.player_data)

    def get_mana(self) -> int:
        mana = self.player_data.get('Mana')
        return 0 if mana is None else mana['Current']

    def get_user_id(self) -> str:
        return self.player_data.get('UserId')

    def get_is_first_mover(self) -> bool:
        return self.player_data.get('IsFirstMover')

    def is_user_id(self, user_id) -> bool:
        return self.get_user_id() == user_id

    def set_mana(self, value) -> None:
        if 'Mana' in self.player_data.keys():
            self.player_data['Mana']['Current'] = value
