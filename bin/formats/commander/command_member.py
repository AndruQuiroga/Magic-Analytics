from bin.formats.normal.member import Member


class CommanderMember(Member):

    def __init__(self, name, id, mmr, winloss, created):
        super().__init__(name, id, mmr, winloss, created)
        self.score = 0
        self.concluded = False