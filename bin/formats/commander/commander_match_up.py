from bin.formats.normal.match_up import MatchUp

class CommanderMatchUp(MatchUp):

    def __init__(self, list_players):
        player1 = list_players[0]
        player2 = list_players[1]
        super().__init__(player1, player2)
        self.player3 = list_players[2]
        if len(list_players) == 3:
            self.player4 = None
        else:
            self.player4 = list_players[3]
        self.score = 1

    def conclude_match(self, player):
        player.score += self.score
        player.concluded = True
        self.score += 1
        if self.score == 5:
            self.match_concluded = True

    def __str__(self):
        if not self.match_concluded:
            return super().__str__() + f"{self.player3.name} vs {self.player4.name}"
        return f"Match Concluded"

    def __getitem__(self, item):
        list = [self.player1, self.player2, self.player3, self.player4]
        return list[item]
