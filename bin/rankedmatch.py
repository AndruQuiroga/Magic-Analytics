import pickle
import datetime
import os
import random
from bin.match import Match


def pick(players):
    num1 = random.randint(0, 3)
    num2 = random.randint(0, 3)
    while num2 == num1:
        num2 = random.randint(0, 3)
    if players[num2] in players[num1].blacklist:
        print("Blacklist!")
        pick(players)
    return players[num1], players[num2]


class RankedMatch(Match):

    def __init__(self, current_players, round_number=1):

        super().__init__(current_players, round_number)


    def pick_bye(self):
        if len(self.roster) % 2 == 1:
            self.bye = self.roster[random.randint(0, len(self.roster) - 1)]
            while self.bye.bye == 1:
                print("Bye Blacklist!")
                self.bye = self.roster[random.randint(0, len(self.roster) - 1)]
            self.bye.bye = 1
            self.roster.remove(self.bye)

    def pick_matches(self):
        while len(self.roster) >= 4:
            self.matches.append([])
            picks = pick(self.roster[0:4])
            picks[0].blacklist = []
            picks[1].blacklist = []
            picks[0].blacklist.append(picks[1])
            picks[1].blacklist.append(picks[0])
            self.roster.remove(picks[0])
            self.roster.remove(picks[1])
            self.matches[self.num_matches].append(picks[0])
            self.matches[self.num_matches].append(picks[1])
            self.num_matches += 1

        if len(self.roster) == 2:
            self.matches.append([])
            self.matches[self.num_matches].append(self.roster[0])
            self.matches[self.num_matches].append(self.roster[1])
            self.roster[0].blacklist.append(self.roster[1])
            self.roster[1].blacklist.append(self.roster[0])
            self.roster.remove(self.roster[-1])
            self.roster.remove(self.roster[-1])
            self.num_matches += 1


