import datetime
import os
import random

from bin.normal.match import Match


class RankedMatch(Match):

    def __init__(self, current_players, round_number=1):
        super().__init__(current_players, round_number, type="Ranked")

    def pick(self, players):
        num1 = random.randint(0, 3)
        num2 = random.randint(0, 3)
        while num2 == num1:
            num2 = random.randint(0, 3)
        if players[num2] in players[num1].blacklist:
            print("Blacklist!")
            self.pick(players)
        return players[num1], players[num2]

    def pick_matches(self):
        while len(self.roster) >= 4:
            picks = self.pick(self.roster[0:4])
            picks[0].blacklist = [picks[1]]
            picks[1].blacklist = [picks[0]]
            self.roster.remove(picks[0])
            self.roster.remove(picks[1])
            self.matches.append([picks[0], picks[1]])
            self.num_matches += 1

        if len(self.roster) == 2:
            self.matches.append([self.roster[0], self.roster[1]])
            self.roster[0].blacklist = [self.roster[1]]
            self.roster[1].blacklist = [self.roster[0]]
            self.roster.remove(self.roster[-1])
            self.roster.remove(self.roster[-1])
            self.num_matches += 1

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}-{self.type}.txt"), "w") as file:
            self.matches.sort()

            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}: {match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d}) "
                           f"vs {match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d})\n")

            file.write(f"====================================================================\n")

            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}: {match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d}) "
                           f"vs {match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d})\n")

            if self.bye:
                file.write(f"\nBye: {self.bye.name}")
