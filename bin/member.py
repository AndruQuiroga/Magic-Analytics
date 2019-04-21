

class Member:

    def __init__(self, name="", id=None, winloss='000000', created=None):

        self.name = name
        self.id = int(id)
        self.wins = int(winloss[:3])
        self.losses = int(winloss[3:])
        self.created = created

        self.declared = 0
        self.bye = 0
        self.blacklist = []

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nW/L: {self.wins}:{self.losses}\nCreated: {self.created}"

    def __eq__(self, other):
        if self.id == other.id:
            return True
        return False

    def __gt__(self, other):
        if self.id > other.id:
            return True
        return False

    def __lt__(self, other):
        return not self.__gt__(other)
