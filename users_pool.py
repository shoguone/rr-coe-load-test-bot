class UsersPool():
    def __init__(self) -> None:
        self.emails = [
            'player1@vovaa',
            'player2@vovaa',
            'player3@vovaa',
            'player4@vovaa',
            'player5@vovaa',
            'player6@vovaa',
            'player7@vovaa',
            'player8@vovaa'
        ]
        self.index = 0

    def get_email(self):
        return self.emails[self.__get_index()]
        
    def __get_index(self):
        cur_index = self.index
        self.index += 1
        return cur_index % len(self.emails)
