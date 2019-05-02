import datetime
import os
import pickle
import random
import names

from bin.formats.normal.member import Member


class TestPlayers:

    def __init__(self, firsttime=False):
        if firsttime:
            self.create_players()
            self.save_players()
        else:
            self.test_players = []
            self.load_players()

    def load_players(self):
        with open(os.path.join("saves", "playerdata.obj"), 'rb') as file:
            tmp = pickle.load(file)
            self.test_players = tmp.test_players

    def save_players(self):
        with open(os.path.join("saves", "playerdata.obj"), 'wb') as file:
            pickle.dump(self, file)
            print("done")

    def create_players(self):
        self.test_players = [Member(name=names.get_first_name(),
                                    id=i,
                                    mmr=random.randint(800, 1300),
                                    winloss='000000',
                                    created=datetime.date.today())
                             for i in range(28)]
