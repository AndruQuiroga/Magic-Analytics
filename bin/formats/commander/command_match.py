import datetime
import os
import random

from bin.formats.commander.command_member import CommanderMember
from bin.formats.commander.commander_match_up import CommanderMatchUp
from bin.formats.normal.match import Match
from bin.main_menu_gui import MainMenu


class CommanderMatch(Match):

    def __init__(self, current_players, round_number=1):
        super().__init__(current_players, round_number, type="Commander")

    def pick(self, num_players):
        players = random.sample(self.roster, num_players)
        self.matches.append(CommanderMatchUp(players))
        for player in players:
            player.blacklist = players
            self.roster.remove(player)

    def pick_matches(self):
        if len(self.roster) % 4 == 0:
            while self.roster:
                self.pick(4)
        elif len(self.roster) % 3 == 0:
            while self.roster:
                self.pick(3)
        elif len(self.roster) % 3 == 2:
            self.pick(4)
            while self.roster:
                self.pick(3)
        else:
            self.pick(4)
            self.pick(4)
            while self.roster:
                self.pick(3)

    def export_round(self):
        path = os.path.join("logs", str(datetime.date.today()))
        if not os.path.exists(path):
            os.chdir("logs")
            os.system("mkdir " + str(datetime.date.today()))
            os.chdir("..")

        with open(os.path.join(path, f"Round{self.round_number}-{self.type}.txt"), "w") as file:
            for table, match in enumerate(self.matches):
                string = f"{match[0].name:16}({match[0].score:02d})"
                for player in match:
                    string += f" vs {player.name:16}({match[0].score:02d})"
                file.write(f"Table #{table + 1:02}:  {string}\n")

if __name__ == '__main__':
    main_menu = MainMenu()
    main_menu.convert_current_players(CommanderMember)
    p1 = CommanderMatch(main_menu.current_players)