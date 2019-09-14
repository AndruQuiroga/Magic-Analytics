import random
import os
import datetime

class Match:

    def __init__(self, roster, round_number):

        self.roster = roster.copy()
        self.sort_players()
        self.round_number = round_number

        self.match_ups = []
        self.num_matches = len(self.match_ups)
        self.bye = None

        self.pick_bye()
        self.pick_matches()
        self.export_round()

    def sort_players(self):
        self.roster.sort(reverse=True, key=lambda x: x.current_wins)

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

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}.txt"), "w") as file:
            for table, match in enumerate(self.match_ups):
                file.write(f"Table #{table + 1:02}:  {match[0].name:16} ({match[0].current_wins}:{match[0].current_losses}) "
                           f"vs {match[1].name:16} ({match[1].current_wins}:{match[1].current_losses})\n")

            file.write(f"====================================================================\n")

            for table, match in enumerate(self.match_ups):
                file.write(f"Table #{table + 1:02}:  {match[1].name:16} ({match[1].current_wins}:{match[1].current_losses}) "
                           f"vs {match[0].name:16} ({match[0].current_wins}:{match[0].current_losses})\n")

            if self.bye:
                file.write(f"\nBye: {self.bye.name}")


class RankedMatch(Match):

    def __init__(self, roster, round_number=1):
        super().__init__(roster, round_number)

    def sort_players(self):
        self.roster.sort(reverse=True, key=lambda x: x.mmr)

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
        self.player1.save()
        self.player2.save()
        self.match_concluded = True

    def __str__(self):
        if not self.match_concluded:
            return f"{self.player1.name} vs {self.player2.name}"
        return f"{self.winner.name} already beat {self.loser.name}!"

    def __getitem__(self, item):
        list = [self.player1, self.player2]
        return list[item]
