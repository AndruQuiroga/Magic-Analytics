import math


class RankedMember:

    def __init__(self, name="", id=None, mmr=1000):

        self.name = name
        self.id = int(id)
        self.mmr = int(mmr)
        self.blacklist = []

    def __str__(self):
        return f"NAME: {self.name} ID: {self.id} MMR: {self.mmr}"

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

    def lost(self, other):
        diff = self.mmr - other.mmr
        if diff > 0:
            new_mmr = (diff // 8) + 15
            self.mmr -= self.upper_clamp(new_mmr, 30)
        else:
            new_mmr = diff // 16 + 15
            self.mmr -= self.lower_clamp(new_mmr, 5)
        print(self)

    def win(self, other):
        diff = self.mmr - other.mmr
        if diff > 0:
            new_mmr = -diff // 16 + 20
            self.mmr += self.lower_clamp(new_mmr, 10)
        else:
            new_mmr = -diff // 8 + 20
            self.mmr += self.upper_clamp(new_mmr, 40)

        other.lost(self)
        print(self)


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



