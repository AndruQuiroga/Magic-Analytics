import copy
import random
import names
import os
import datetime
from ranked_member import RankedMember

test_players = [RankedMember(name=names.get_first_name(), id=i, mmr=random.randint(700, 1400), winloss='000000') for i in range(18)]


def pick(players):
    num1 = random.randint(0, 3)
    num2 = random.randint(0, 3)
    while num2 == num1:
        num2 = random.randint(0, 3)
    if players[num2] in players[num1].blacklist:
        print("Blacklist!")
        pick(players)
    return players[num1], players[num2]


def match_make(current_players, round_number):

    matched = []
    for player in current_players:
        player.declared = 0
    roster = copy.deepcopy(current_players)
    roster += test_players
    roster.sort(reverse=True)
    matches = 0

    if len(roster) % 2 == 1:
        bye = roster[random.randint(0, len(roster)-1)]
        while bye.bye == 1:
            print("Bye Blacklist!")
            bye = roster[random.randint(0, len(roster) - 1)]
        bye.bye = 1
        roster.remove(bye)
    else:
        bye = False

    while len(roster) >= 4:
        matched.append([])
        picks = pick(roster[0:4])
        picks[0].blacklist = []
        picks[1].blacklist = []
        picks[0].blacklist.append(picks[1])
        picks[1].blacklist.append(picks[0])
        roster.remove(picks[0])
        roster.remove(picks[1])
        matched[matches].append(picks[0])
        matched[matches].append(picks[1])
        matches += 1

    if len(roster) == 3:

        matched.append([])
        num = random.randint(0, 2)
        num2 = random.randint(0, 2)
        while num2 == num:
            num2 = random.randint(0, 2)
        matched[matches].append(roster[num])
        matched[matches].append(roster[num2])
        roster.remove(matched[matches][0])
        roster.remove(matched[matches][1])
        matches += 1

    if len(roster) == 2:
        matched.append([])
        matched[matches].append(roster[0])
        matched[matches].append(roster[1])
        roster[0].blacklist.append(roster[1])
        roster[1].blacklist.append(roster[0])
        roster.remove(roster[-1])
        roster.remove(roster[-1])
        matches += 1

    if not os.path.exists(str(datetime.date.today())):
        os.system("mkdir " + str(datetime.date.today()))
    with open(os.path.join(str(datetime.date.today()), f"Round{round_number+1}.txt"), "w") as file:
        matched.sort()
        for match in matched:
            file.write(f"{match[0].name:16} ({match[0].mmr:04d}) vs {match[1].name:16} ({match[1].mmr:04d})\n")
        file.write(f"==================================================\n")
        for match in matched:
            file.write(f"{match[1].name:16} ({match[1].mmr:04d}) vs {match[0].name:16} ({match[0].mmr:04d})\n")

        if bye:
            print(str(bye))
            file.write(f"\nBye: {bye.name}")


    file.close()

    return matched








