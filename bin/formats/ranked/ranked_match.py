import datetime
import os
import random

from bin.formats.normal.match import Match
from bin.formats.normal.match_up import MatchUp


class RankedMatch(Match):

    def __init__(self, current_players, round_number=1):
        super().__init__(current_players, round_number, type="Ranked")

    def pick(self, players):
        picks = random.sample(players, 2)
        if len(self.roster) != 2:
            if picks[1] in picks[0].blacklist:
                print("Blacklist!")
                return self.pick(players)
        picks[0].set_blacklist(picks[1])
        self.matches.append(MatchUp(picks[0], picks[1]))
        for pick in picks:
            self.roster.remove(pick)
        self.num_matches += 1
        return

    def pick_matches(self):
        while len(self.roster) >= 4:
            self.pick(self.roster[0:4])
        self.pick(self.roster)

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}-{self.type}.txt"), "w") as file:

            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}: {match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d}) "
                           f"vs {match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d})\n")

            file.write(f"====================================================================\n")

            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}: {match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d}) "
                           f"vs {match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d})\n")

            if self.bye:
                file.write(f"\nBye: {self.bye.name}")
