

class RankedMember:

    def __init__(self, id=None, mmr=1000):

        self.id = id
        self.mmr = mmr

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
            self.mmr -