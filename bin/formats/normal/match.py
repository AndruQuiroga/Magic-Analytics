import datetime
import os
import pickle
import random

from bin.formats.normal.match_up import MatchUp

ranked_dict = {
    range(1, 1050): "Silver",
    range(1050, 1100): "Gold",
    range(1100, 1150): "Platinum",
    range(1150, 1800): "Diamond",
}


class Match:

    def __init__(self, current_players, round_number=1, type="Normal"):

        self.roster = []
        self.roster += current_players
        self.roster.sort(reverse=True)
        self.round_number = round_number

        self.type = type

        self.bye = None
        self.matches = []
        self.num_matches = len(self.matches)
        self.match_make()

    def __contains__(self, item):
        for match in self.matches:
            if item in match:
                return True
        return False


    def match_make(self):
        if not self.round_number == 0:
            self.pick_bye()
            self.pick_matches()
            self.export_round()
            self.save_round()

    @staticmethod
    def re_rank(players):
        players.sort(reverse=True)
        for rank, player in enumerate(players):
            player.prank_num = player.rank_num
            player.rank_num = rank + 1
            for key in ranked_dict:
                if player.mmr in key:
                    player.rank = ranked_dict[key]
            if player.rank_num < 6 and player.mmr >= 1200 :
                player.rank = "Mythic"

    def pick(self, players):
        while len(players) > 1:
            picks = random.sample(players, 2)
            if picks[1] in picks[0].blacklist:
                print("Blacklist!")
                return self.pick(players)
            picks[0].set_blacklist(picks[1])
            self.matches.append(MatchUp(picks[0], picks[1]))
            for pick in picks:
                self.roster.remove(pick)
                players.remove(pick)
            self.num_matches += 1
            return

    def pick_bye(self):
        if len(self.roster) % 2 == 1:
            self.bye = random.sample(self.roster, 1)
            while self.bye[0].bye == 1:
                print("Bye Blacklist!")
                return self.pick_bye()
            self.bye = self.bye[0]
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
