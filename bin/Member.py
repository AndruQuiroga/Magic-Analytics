from bin import MySQL


class Member:

    @staticmethod
    def re_rank(ranked_members):
        ranked_dict = {
            range(1, 900): "Bronze",
            range(900, 1050): "Silver",
            range(1050, 1100): "Gold",
            range(1100, 1150): "Platinum",
            range(1150, 1200): "Diamond"
        }
        ranked_members.sort(reverse=True)
        for rank, member in enumerate(ranked_members):

            for key in ranked_dict:
                if member.mmr in key:
                    member.rank = f"{rank + 1}|{ranked_dict[key]}|{member.mmr > member.last_mmr}"
            if rank <= 6 and member.mmr >= 1200:
                member.rank = f"{rank + 1}|Mythic|{member.mmr > member.last_mmr}"

    def __init__(self, name, id, winloss, created):

        self.name = name
        self.id = id
        self.career_wins = int(winloss[:3])
        self.career_losses = int(winloss[3:])
        self.created = created

    @property
    def winloss(self):
        return f'{self.career_wins:03}{self.career_losses:03}'

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nW/L: " \
            f"{self.career_wins}:{self.career_losses}\nCreated: {self.created}"


class RankedMember(Member):

    def __init__(self, name, id, mmr, ranked_winloss, created):
        super().__init__(name, id, ranked_winloss, created)
        self.mmr = int(mmr)
        self.last_mmr = 0
        self.rank = None

    def __str__(self):
        return super().__str__() + f"\nMMR: {self.mmr}"


class Player(Member):

    def __init__(self, member):
        super().__init__(member.name,
                         member.id,
                         member.winloss,
                         member.created,)

        self.current_wins = 0
        self.current_losses = 0
        self.bye = False
        self.blacklist = []

    def win(self, other):
        self.current_wins += 1
        self.career_wins += 1
        other.lost(self)
        print(self)

    def lost(self, other):
        self.current_losses += 1
        self.career_losses += 1

    def set_blacklist(self, other):
        self.blacklist = [other]
        other.blacklist = [self]

    def save(self):
        MySQL.update_normal((self.winloss, self.id))


class RankedPlayer(RankedMember):

    def __init__(self, member):
        super().__init__(member.name,
                         member.id,
                         member.mmr,
                         member.winloss,
                         member.created)

        self.bye = False
        self.blacklist = []

    def win(self, other):
        diff = self.mmr - other.mmr
        self.last_mmr = self.mmr
        if diff > 0:
            mmr_change = -diff // 16 + 20
            self.mmr += max(mmr_change, 10)
        else:
            mmr_change = -diff // 8 + 20
            self.mmr += min(mmr_change, 40)
        self.career_wins += 1
        other.lost(self)

    def lost(self, other):
        diff = self.mmr - other.mmr
        self.last_mmr = self.mmr
        if diff > 0:
            new_mmr = (diff // 8) + 15
            self.mmr -= min(new_mmr, 30)
        else:
            new_mmr = diff // 16 + 15
            self.mmr -= max(new_mmr, 5)
        self.career_losses += 1

    def set_blacklist(self, other):
        self.blacklist = [other]
        other.blacklist = [self]

    def save(self):
        MySQL.update_ranked((self.mmr, self.winloss, self.id))


if __name__ == '__main__':
    p1 = Member("Andru", 123548, '001002', "12/213/12")
