import datetime
from tkinter import simpledialog, messagebox

from bin import MySQL
from bin.html_writer import write_html
from bin.ranked.ranked_match import Match, RankedMatch
from bin.ranked.ranked_member import Member, RankedMember


class MainMenu:

    def __init__(self):
        self.registered_players = []
        self.current_players = []
        global match_type
        global member_type

        event_tp = "normal"

        if event_tp == "normal":
            match_type = Match
            member_type = Member
        else:
            match_type = RankedMatch
            member_type = RankedMember

        self.current_match = match_type([], 0)

        # test_players = [member_type(name=names.get_first_name(), id=i, mmr=random.randint(800, 1300), winloss='000000')
        #                 for i in range(28)]
        # for player in test_players:
        #     add_player((player.id, player.name, 1000, '000000', datetime.date.today()))

        for player in MySQL.get_players():
            self.registered_players.append(
                member_type(id=player[0],
                            name=player[1],
                            mmr=player[2],
                            winloss=player[3],
                            created=player[4]))

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
                    self.current_players.append(member_type(name=name, id=scan_id, created=datetime.date.today()))
                    info.set(f"Account \'{self.current_players[-1].name}\' Created!")
                else:
                    for player in self.registered_players:
                        if int(scan_id) == player.id:
                            info.set(f"Welcome {player.name}!\n{player.name} added to the current Roster")
                            self.current_players.append(player)

        except ValueError:
            info.set("Invalid ID!")

    # def remove_player(self, info, name):
    #     name = name.lower()
    #
    #     if not any(name in player.name.lower() for player in self.current_players):
    #         info.set(f"Name not in roster!")
    #         return
    #
    #     else:
    #         try:
    #             finding_players = iter(self.current_players)
    #             answer = False
    #             player = None
    #
    #             while not answer:
    #                 player = next(x for x in finding_players if name in x.name.lower())
    #                 answer = messagebox.askyesno("Removing Player:", f"looking for {player.name}? ")
    #
    #             answer = messagebox.askyesno("Removing Player:",
    #               f"Are you sure you want to remove {player.name} from the roster?")
    #             if answer:
    #                 info.set(f"Removed {player.name}")
    #                 self.current_players.remove(player)
    #
    #         except StopIteration:
    #             info.set(f"Could NOT find a player by the Keyword {name}!")

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

    def get_current_players(self):
        string = ""
        for player in self.current_players:
            string += player.name
            string += "\n"
        return string