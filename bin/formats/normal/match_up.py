
class MatchUp:

    def __init__(self, player1, player2, player3=None, player4=None):

        self.player1 = player1
        self.player2 = player2

        self.winner = None
        self.loser = None
        self.match_concluded = False

    def conclude_match(self, winner):
        self.winner = winner
        if self.winner == self.player1:
            self.loser = self.player2
        else:
            self.loser = self.player1
        self.winner.win(self.loser)
        self.match_concluded = True

    def __str__(self):
        if not self.match_concluded:
            return f"{self.player1.name} vs {self.player2.name}"
        return f"{self.winner.name} Already beat {self.loser.name}!"

    def __getitem__(self, item):
        list = [self.player1, self.player2]
        return list[item]