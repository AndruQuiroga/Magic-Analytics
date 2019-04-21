import datetime
import os
import pickle
import random


class Match:

    def __init__(self, current_players, round_number=1, type="Normal"):

        for player in current_players:
            player.declared = 0

        self.roster = []
        self.roster += current_players
        self.roster.sort(reverse=True)
        self.round_number = round_number

        self.type = type

        self.bye = False
        self.matches = []
        self.num_matches = len(self.matches)
        self.match_make()

    def match_make(self):
        if not self.round_number == 0:
            self.pick_bye()
            self.pick_matches()
            self.export_round()
            self.save_round()

    def pick(self, players):
        if len(players) < 2:
            return
        elif len(players) == 2:
            p1 = players[0]
            p2 = players[1]
            p1.blacklist = [p2]
            p2.blacklist = [p1]
            self.matches.append([p1, p2])
            self.roster.remove(p1)
            self.roster.remove(p2)
            players.remove(p1)
            players.remove(p2)
            self.num_matches += 1
            return
        else:
            num1 = random.randint(0, len(players) - 1)
            num2 = random.randint(0, len(players) - 1)
            while num2 == num1:
                num2 = random.randint(0, len(players) - 1)
            if players[num2] in players[num1].blacklist:
                print("Blacklist!")
                self.pick(players)
                return
            p1 = players[num1]
            p2 = players[num2]
            p1.blacklist = [p2]
            p2.blacklist = [p1]
            self.matches.append([p1, p2])
            self.roster.remove(p1)
            self.roster.remove(p2)
            players.remove(p1)
            players.remove(p2)
            self.num_matches += 1
            return

    def pick_bye(self):
        if len(self.roster) % 2 == 1:
            self.bye = self.roster[random.randint(0, len(self.roster) - 1)]
            while self.bye.bye == 1:
                print("Bye Blacklist!")
                self.bye = self.roster[random.randint(0, len(self.roster) - 1)]
            self.bye.bye = 1
            self.roster.remove(self.bye)

    def pick_matches(self):
        while self.roster:
            current = self.roster[1]
            player_list = [player for player in self.roster if
                           player.wins == current.wins and player.losses == current.losses]
            if self.roster[0] not in player_list:
                player_list.append(self.roster[0])
            self.pick(player_list)

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}-{self.type}.txt"), "w") as file:
            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}:  {match[0].name:16} ({match[0].wins}:{match[0].losses}) "
                           f"vs {match[1].name:16} ({match[1].wins}:{match[1].losses})\n")

            file.write(f"====================================================================\n")

            for table, match in enumerate(self.matches):
                file.write(f"Table #{table + 1:02}:  {match[1].name:16} ({match[1].wins}:{match[1].losses}) "
                           f"vs {match[0].name:16} ({match[0].wins}:{match[0].losses})\n")

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
