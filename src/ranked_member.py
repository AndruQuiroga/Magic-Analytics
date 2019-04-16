import math

from MySQL import update


class RankedMember:

    def __init__(self, name="", id=None, mmr=1000, winloss='000000', created=None):

        self.name = name
        self.id = int(id)
        self.mmr = int(mmr)
        self.wins = int(winloss[:3])
        self.losses = int(winloss[3:])
        self.created = created
        self.bye = 0
        self.blacklist = []

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nMMR: {self.mmr}\nW/L: {self.wins}:{self.losses}\nCreated: {self.created}"

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
        update((self.mmr, winloss, self.id))

    def lost(self, other):
        print(f"----------\nBefore: {self}")
        diff = self.mmr - other.mmr
        if diff > 0:
            new_mmr = (diff // 8) + 15
            self.mmr -= self.upper_clamp(new_mmr, 30)
        else:
            new_mmr = diff // 16 + 15
            self.mmr -= self.lower_clamp(new_mmr, 5)
        self.losses += 1
        self.save()
        print(f"After: {self}\n----------")

    def win(self, other):
        print(f"----------\nBefore: {self}")
        diff = self.mmr - other.mmr
        if diff > 0:
            new_mmr = -diff // 16 + 20
            self.mmr += self.lower_clamp(new_mmr, 10)
        else:
            new_mmr = -diff // 8 + 20
            self.mmr += self.upper_clamp(new_mmr, 40)
        self.wins += 1
        self.save()
        print(f"After: {self}")
        other.lost(self)



    def upper_clamp(self, input, clamp):
        if input > clamp:
            return clamp
        return input

    def lower_clamp(self, input, clamp):
        if input < clamp:
            return clamp
        return input


if __name__ == '__main__':
    p1 = RankedMember(2222, 1372)
    p2 = RankedMember(3333, 1178)

    print(p2)
    p2.win(p1)
    print(p2)



