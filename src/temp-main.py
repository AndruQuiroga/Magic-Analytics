from src.ranked_member import RankedMember
id = 222
mmr = 1020
current_players = []

while True:
    name = input("NAME: ")


    if name == "STOP":
        find = "And"
        Finding_players = iter(current_players)
        answer = ""
        try:
            while answer != "y":
                player = next(x for x in Finding_players if find in x.name)
                answer = input(f"Are you {player.name}?")
        except StopIteration:
            print(f"Could NOT find player by the name {find}")

        break

    id = input("ID: ")
    mmr = input("MMR: ")

    if mmr == "":
        current_players.append(RankedMember(name=name, id=id))
    else:
        current_players.append(RankedMember(name=name, id=id, mmr=mmr))


