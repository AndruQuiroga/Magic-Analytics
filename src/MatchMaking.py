import random
from src.ranked_member import RankedMember


def pick(players):
    num1 = random.randint(0, 3)
    num2 = random.randint(0, 3)
    while num2 == num1:
        num2 = random.randint(0, 3)
    if players[num2] in players[num1].blacklist:
        print("Blacklist!")
        pick(players)
    return players[num1], players[num2]


if __name__ == '__main__':

    matched = []
    current_players = [RankedMember(i, random.randint(700, 1400)) for i in range(10)]
    current_players.sort(reverse=True)
    matches = 0

    for players in current_players:
        current_players[0].blacklist.append(players)
    print(current_players[0].blacklist)

    while len(current_players) >= 4:
        matched.append([])
        picks = pick(current_players[0:4])
        picks[0].blacklist.append(picks[1])
        picks[1].blacklist.append(picks[0])
        current_players.remove(picks[0])
        current_players.remove(picks[1])
        matched[matches].append(picks[0].mmr)
        matched[matches].append(picks[1].mmr)
        matches += 1

    if len(current_players) == 3:

        matched.append([])
        num = random.randint(0, 2)
        num2 = random.randint(0, 2)
        while num2 == num:
            num2 = random.randint(0, 2)
        matched[matches].append(current_players[num].mmr)
        matched[matches].append(current_players[num2].mmr)
        current_players.remove(current_players[num])
        current_players.remove(current_players[num2])
        matches += 1

    if len(current_players) == 2:
        matched.append([])
        matched[matches].append(current_players[0].mmr)
        matched[matches].append(current_players[1].mmr)
        current_players.remove(current_players[-1])
        current_players.remove(current_players[-1])
        matches += 1

    for players in current_players:
        print("By: " + players.mmr)
    print(matched)
    print(matches)










