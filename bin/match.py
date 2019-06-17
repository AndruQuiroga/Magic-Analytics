import random


class Match:

    def __init__(self, roster, round_number):

        self.roster = roster.copy()
        self.roster.sort(reverse=True, key=lambda x: x.current_wins)
        self.round_number = round_number

        self.match_ups = []
        self.num_matches = len(self.match_ups)
        self.bye = None

        self.pick_bye()
        self.pick_matches()

    def pick_bye(self):
        if len(self.roster) % 2 != 0:
            self.bye = random.sample(self.roster, 1)[0]
            while self.bye.bye is True:
                print("Bye Blacklist!")
                return self.pick_bye()
            self.bye.bye = True
            self.roster.remove(self.bye)

    def pick_matches(self):

        while self.roster:
            chosen_one = self.roster[1]
            player_list = [player for player in self.roster
                           if player.current_wins == chosen_one.current_wins
                           and player.current_losses == chosen_one.current_losses]
            if self.roster[0] not in player_list:
                player_list.append(self.roster[0])

            self.pick(player_list)

    def pick(self, players):
        while len(players) > 1:
            picks = random.sample(players, 2)
            if picks[1] in picks[0].blacklist:
                print("Blacklist!")
                return self.pick(players)

            picks[0].set_blacklist(picks[1])
            self.match_ups.append(MatchUp(picks))
            for pick in picks:
                self.roster.remove(pick)
                players.remove(pick)

        return


class RankedMatch(Match):

    def __init__(self, roster, round_number=1):
        super().__init__(roster, round_number)

    def pick_matches(self):
        while len(self.roster) >= 4:
            self.pick(self.roster[0:4])
        self.pick(self.roster)


class MatchUp:

    def __init__(self, players):
        self.player1 = players[0]
        self.player2 = players[1]
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
        return f"{self.winner.name} already beat {self.loser.name}!"

    def __getitem__(self, item):
        list = [self.player1, self.player2]
        return list[item]
