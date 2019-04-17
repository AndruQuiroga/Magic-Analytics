import math

from src.MySQL import update

ranked_dict = {
    range(1, 900): "Bronze",
    range(900, 1050): "Silver",
    range(1050, 1100): "Gold",
    range(1100, 1150): "Platinum",
    range(1150, 1200): "Diamond",
    range(1200, 1800): "Mythic",
}

def upper_clamp(input, clamp):
    if input > clamp:
        return clamp
    return input


def lower_clamp(input, clamp):
    if input < clamp:
        return clamp
    return input


class RankedMember:

    def __init__(self, name="", id=None, mmr=1000, winloss='000000', created=None):

        self.name = name
        self.id = int(id)
        self.mmr = int(mmr)
        self.wins = int(winloss[:3])
        self.losses = int(winloss[3:])
        self.created = created

        for key in ranked_dict:
            if self.mmr in key:
                self.rank = ranked_dict[key]
        self.declared = 0
        self.bye = 0
        self.blacklist = []

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nRank: {self.rank}\nW/L: {self.wins}:{self.losses}\nCreated: {self.created}"  # @todo add rank number

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __gt__(self, other):
        if self.mmr > other.mmr:
            return True
        return False

    def __lt__(self, other):
        return not self.__gt__(other)

    def save(self):
        winloss = "{:03d}{:03d}".format(self.wins, self.losses)
        update((str(self.mmr), winloss, str(self.id)))

    def lost(self, other):
        diff = self.mmr - other.mmr
        bmmr = self.mmr
        if diff > 0:
            new_mmr = (diff // 8) + 15
            self.mmr -= upper_clamp(new_mmr, 30)
        else:
            new_mmr = diff // 16 + 15
            self.mmr -= lower_clamp(new_mmr, 5)
        self.losses += 1
        self.declared = -1
        self.save()
        print(f"==============================\n{self.name}\n{bmmr} ---> {self.mmr}")

    def win(self, other):
        diff = self.mmr - other.mmr
        bmmr = self.mmr
        if diff > 0:
            new_mmr = -diff // 16 + 20
            self.mmr += lower_clamp(new_mmr, 10)
        else:
            new_mmr = -diff // 8 + 20
            self.mmr += upper_clamp(new_mmr, 40)
        self.wins += 1
        self.declared = 1
        self.save()
        print(f"==============================\n{self.name}\n{bmmr} ---> {self.mmr}")
        other.lost(self)
