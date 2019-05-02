import datetime
from tkinter import simpledialog, messagebox

# from bin import MySQL
# from bin.formats.commander.command_member import CommanderMember
from bin.formats.ranked.ranked_match import Match
from bin.formats.ranked.ranked_member import Member, RankedMember
from bin.test_players_offline import TestPlayers


class MainMenu:

    def __init__(self):
        self.registered_players = []
        self.current_players = []

        self.current_match = Match([], 0)

        # for player in MySQL.get_players():  ## online
        #     self.registered_players.append(
        #         Member(id=player[0],
        #                     name=player[1],
        #                     mmr=player[2],
        #                     winloss=player[3],
        #                     created=player[4]))

        self.registered_players = TestPlayers().test_players

        self.current_players += self.registered_players

        print("Pre-main done!")

    def add_player(self, info, scan_id):

        try:
            if any(int(scan_id) == player.id for player in self.current_players):
                info.set("Player Already Logged In!")

            else:
                if not any(int(scan_id) == player.id for player in self.registered_players):
                    name = simpledialog.askstring("ID not found in database!\nWant to to create a new Account? ",
                                                  "Create an Account name: ")
                    if name is None:
                        return
                    MySQL.add_player((scan_id, name, 1000, '000000', datetime.date.today()))
                    self.current_players.append(Member(name=name, id=scan_id, mmr=1000, winloss="000000", created=datetime.date.today()))
                    info.set(f"Account \'{self.current_players[-1].name}\' Created!")
                else:
                    for player in self.registered_players:
                        if int(scan_id) == player.id:
                            info.set(f"Welcome {player.name}!\n{player.name} added to the current Roster")
                            self.current_players.append(player)

        except ValueError:
            info.set("Invalid ID!")

    def declare(self, items):
        if items[0] == -1:
            match = self.current_match.matches[items[1]]
            winner = match[1]
            loser = match[0]
        else:
            match = self.current_match.matches[items[0]]
            winner = match[0]
            loser = match[1]

        if match.match_concluded:
            messagebox.showerror("Error", str(match))
            return

        answer = messagebox.askyesno("Declaring Winner:", f"Are you sure {winner.name} beat {loser.name}?")
        if answer:
            match.conclude_match(winner)
            self.current_match.save_round()

    def convert_current_players(self, member_type):
        for num, player in enumerate(self.current_players):
            self.current_players[num] = member_type(player.name, player.id, player.mmr, player.winloss, player.created)
