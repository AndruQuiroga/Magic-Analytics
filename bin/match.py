import pickle
import datetime
import os
import random


def pick(players):
    num1 = random.randint(0, 3)
    num2 = random.randint(0, 3)
    while num2 == num1:
        num2 = random.randint(0, 3)
    if players[num2] in players[num1].blacklist:
        print("Blacklist!")
        pick(players)
    return players[num1], players[num2]


class Match:

    def __init__(self, current_players, round_number=1):

        for player in current_players:
            player.declared = 0

        self.roster = []
        self.roster += current_players
        self.roster.sort(reverse=True)
        self.round_number = round_number

        self.bye = False
        self.matches = []
        self.num_matches = len(self.matches)

        if not round_number == 0:
            self.pick_bye()
            self.pick_matches()
            self.export_round()
            self.save_round()

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

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}.txt"), "w") as file:
            self.matches.sort()

            for match in self.matches:
                file.write(f"{match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d}) "
                           f"vs {match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d})\n")

            file.write(f"====================================================================\n")

            for match in self.matches:
                file.write(f"{match[1].name:16} ({match[1].rank:8} #{match[1].rank_num:03d}) "
                           f"vs {match[0].name:16} ({match[0].rank:8} #{match[0].rank_num:03d})\n")

            if self.bye:
                file.write(f"\nBye: {self.bye.name}")

    def save_round(self):
        path = os.path.join("saves", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("saves")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f'round{self.round_number}.obj'), 'wb') as file:
            pickle.dump(self, file)
