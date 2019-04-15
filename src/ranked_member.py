import math


class RankedMember:

    def __init__(self, id=None, mmr=1000):

        self.id = id
        self.mmr = mmr

    def __str__(self):
        return f"ID: {self.id} MMR: {self.mmr}"

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

    def win(self, other):
        diff = self.mmr - other.mmr
        if diff > 0:
            new_mmr = -diff // 16 + 20
            self.mmr += self.lower_clamp(new_mmr, 10)
        else:
            new_mmr = -diff // 8 + 20
            self.mmr += self.upper_clamp(new_mmr, 40)

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
    p2 = RankedMember(3333, 1296)

    print(p2)
    p2.lost(p1)
    print(p2)



