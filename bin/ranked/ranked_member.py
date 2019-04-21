from bin import my_math
from bin.MySQL import update_ranked
from bin.normal.member import Member

ranked_dict = {
    range(1, 900): "Bronze",
    range(900, 1050): "Silver",
    range(1050, 1100): "Gold",
    range(1100, 1150): "Platinum",
    range(1150, 1200): "Diamond",
    range(1200, 1800): "Mythic",
}


class RankedMember(Member):

    def __init__(self, name="", id=None, mmr=1000, winloss='000000', created=None):

        super().__init__(name, id, mmr, winloss, created)

        for key in ranked_dict:
            if self.mmr in key:
                self.rank = ranked_dict[key]
        self.rank_num = 999

    def __str__(self):
        return f"NAME: {self.name}\nID: {self.id}\nRank: {self.rank} : {self.rank_num}\nW/L: {self.career_wins}:{self.career_losses}\nCreated: {self.created}"

    def __gt__(self, other):
        if self.mmr > other.mmr:
            return True
        return False

    def save(self):
        winloss = "{:03d}{:03d}".format(self.career_wins, self.career_losses)
        update_ranked((str(self.mmr), winloss, str(self.id)))

    def lost(self, other):
        diff = self.mmr - other.mmr
        bmmr = self.mmr
        if diff > 0:
            new_mmr = (diff // 8) + 15
            self.mmr -= my_math.upper_clamp(new_mmr, 30)
        else:
            new_mmr = diff // 16 + 15
            self.mmr -= my_math.lower_clamp(new_mmr, 5)
        self.career_losses += 1
        self.save()
        print(f"==============================\n{self.name}\n{bmmr} ---> {self.mmr}")

    def win(self, other):
        diff = self.mmr - other.mmr
        bmmr = self.mmr
        if diff > 0:
            new_mmr = -diff // 16 + 20
            self.mmr += my_math.lower_clamp(new_mmr, 10)
        else:
            new_mmr = -diff // 8 + 20
            self.mmr += my_math.upper_clamp(new_mmr, 40)
        self.career_wins += 1
        self.save()
        print(f"==============================\n{self.name}\n{bmmr} ---> {self.mmr}")
        other.lost(self)
