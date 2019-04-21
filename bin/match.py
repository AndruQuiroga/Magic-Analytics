import datetime
import os
import pickle


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
