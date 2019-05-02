# from bin.MySQL import update_normal


class Member:

    def __init__(self, name, id, mmr, winloss, created):

        self.name = name
        self.id = int(id)
        self.career_wins = int(winloss[:3])
        self.career_losses = int(winloss[3:])
        self.winloss = f"{self.career_wins:03d}{self.career_losses:03d}"
        self.wins = 0
        self.losses = 0
        self.created = created
        self.mmr = int(mmr)
        self.rank_num = 999
        self.rank = None
        self.prank_num = 999

        self.bye = 0
        self.blacklist = []

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nW/L: {self.career_wins}:{self.career_losses}\nCreated: {self.created}"

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __gt__(self, other):
        if self.wins > other.wins:
            return True
        return False

    def __lt__(self, other):
        return not self.__gt__(other)

    def save(self):
        winloss = "{:03d}{:03d}".format(self.career_wins, self.career_losses)
        # update_normal((winloss, str(self.id))) ##online


    def lost(self, other):
        self.losses += 1
        self.career_losses += 1
        self.save()
        print(f"==============================\n{self.name} Lost!")

    def win(self, other):
        print(f"{self.name} Won!")
        self.wins += 1
        self.career_wins += 1
        self.save()
        other.lost(self)

    def set_blacklist(self, other, repeat=False):
        self.blacklist = [other]
        if not repeat:
            other.set_blacklist(self, True)
