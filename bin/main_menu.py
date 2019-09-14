import datetime
import os
from tkinter import simpledialog
import csv

from bin import MySQL
from bin.Member import *
from bin.match import Match, RankedMatch
from bin.export import *


class MainMenu:

    format_dict = {"normal": Player,
                   "ranked": RankedPlayer}

    def __init__(self, format):
        self.registered_members = []
        self.current_players = []
        self.format = format
        self.status = MySQL.test_online()

        self.get_registered_members()
        self.current_players += [self.format_dict[self.format](member) for member in self.registered_members]  # test
        # self.current_players = []
        self.current_match = RankedMatch([], 0)
        make_last_session(self)

        print("=" * 40, "\nPre-main done!")
        print("=" * 40)

    def get_registered_members(self):
        if self.status:
            members = MySQL.get_members()
        else:
            members = make_offline_members(self.format)

        if self.format == "normal":
            for member in members:
                self.registered_members.append(
                    Member(id=member[0],
                           name=member[1],
                           winloss=member[3],
                           created=member[5]))
        else:
            for member in members:
                self.registered_members.append(
                    RankedMember(id=member[0],
                                 name=member[1],
                                 mmr=member[2],
                                 ranked_winloss=member[4],
                                 created=member[5]))

    def add_player(self, info_box, put):
        scan_id = put.get()
        put.delete(0, 'end')

        try:
            if any(int(scan_id) == player.id for player in self.current_players):
                info_box.set("Player Already Logged In!")

            else:
                if not any(int(scan_id) == player.id for player in self.registered_members):
                    name = simpledialog.askstring("ID not found in database!\nWant to to create a new Account? ",
                                                  "Create an Account name: ")
                    if not name:
                        return

                    if self.format == "normal":
                        MySQL.add_player((scan_id, name, 1000, '000000', '000000'))
                        self.registered_members.append(
                            Member(name=name, id=scan_id, winloss="000000",
                                   created=datetime.date.today()))
                    else:
                        MySQL.add_player((scan_id, name, 1000, '000000', '000000'))
                        self.registered_members.append(
                            RankedMember(name=name, id=scan_id, mmr=1000, ranked_winloss="000000",
                                         created=datetime.date.today()))
                    self.current_players.append(self.format_dict[self.format](self.registered_members[-1]))
                    info_box.set(f"Account \'{self.current_players[-1].name}\' Created!")

                else:
                    for player in self.registered_members:
                        if int(scan_id) == player.id:
                            info_box.set(f"Welcome {player.name}!\n{player.name} added to the current Roster")
                            self.current_players.append(self.format_dict[self.format](player))

        except ValueError as ve:
            info_box.set("Invalid ID!")
            print(ve)

    def make_match(self):
        # self.update_members()
        if self.format == "normal":
            self.current_match = Match(self.current_players, self.current_match.round_number + 1)
        else:
            self.current_match = RankedMatch(self.current_players, self.current_match.round_number + 1)

    def update_members(self):
        # for player in self.current_players:
        #     member = next(member for member in self.registered_members if member.id == player.id)
        #     member.career_wins = player.career_wins
        #     member.career_losses = player.career_losses
        #     if self.format == "ranked":
        #         member.mmr = player.mmr

        if self.status:
            print("=" * 40, "\nOnline-Saving Started!")
            for player in self.current_players:
                if self.format == "normal":
                    MySQL.update_normal(
                        (f"{player.career_wins:03d}{player.career_losses:03d}", str(player.id)))
                else:
                    MySQL.update_ranked(
                        (player.mmr, f"{player.career_wins:03d}{player.career_losses:03d}", str(player.id)))
            print("Online-Saving Finished!")
            print("=" * 40)

        print("=" * 40, "\nOffline-Saving Started!")
        make_local_database(self)
        print("Offline-Saving Finished!")
        print("=" * 40)
