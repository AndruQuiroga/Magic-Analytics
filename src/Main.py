import datetime
import msvcrt
from os import system
from MatchMaking import match_make
from MySQL import *
from ranked_member import RankedMember


def pre_main():
    global registered
    global current_players
    global matched
    global count
    global spacer
    spacer = "==============================\n"
    registered = get_players()
    current_players = []
    matched = []
    count = -1
    main()


def main():

    system("cls")
    while True:

        put = input(f"{spacer}Insert Command: ")
        put = put.lower()

        if put == "list" or put == "ls":
            for player in current_players:
                print(player.name)
            continue

        if put == "matchmake" or put == "mm":
            global count
            count += 1
            matched.append([])
            matched[count].append(match_make(current_players, count))
            continue

        if put == "reset":
            pre_main()
            break

        if put == "clear":
            tmp = input("ARE YOU SURE YOU WANT TO CLEAR SQL DATABASE?!?")
            if tmp == "ironisbronze":
                delete()
                pre_main()
                break
            else:
                print("INCORRECT PASSWORD")
                continue

        if put == "add" or put == "a":
            add()
            break

        if put == "remove" or put == "r":
            remove()
            break

        if put == "stats" or put == "s":
            stats()
            break

        if put == "declare" or put == "d":
            declare()

        if put == "help" or put == "?":
            print(f"{spacer}Valid Commands:"
                  f"\nAdd: Add a player to the roster"
                  f"\nRemove: Remove a player from roster"
                  f"\nMatchMake: Create matchups"
                  f"\nStats: Look up Stats from id"
                  f"\nDeclare: Declare a winner from matchup"
                  f"\nList: Look up current Roster"
                  f"\nX: to return back to main menu")

        else:
            print("INVALID COMMAND! Try \'help\'.")

def add():

    system("cls")
    global current_players
    while True:

        scan_id = input(f"{spacer}\nSwipe Card    ID:")

        if scan_id.lower() == "x":
            main()
            break

        try:
            if any(int(scan_id) == player.id for player in current_players):
                print(f"{spacer}Player Already Logged In!")
                print(f"{spacer}Current Players: {len(current_players)}!")

            else:
                if not any(scan_id in player for player in registered):
                    print(f"{spacer}ID not found in database!")
                    tmp = input("Want to to create a new Account? ")
                    if tmp.lower() in "yes":
                        name = input("Create an Account name: ")
                    else:
                        continue
                    add_player((scan_id, name, 1000, '000000', datetime.date.today()))
                    current_players.append(RankedMember(name=name, id=scan_id, created=datetime.date.today()))
                    print(f"{spacer}Account \'{current_players[-1].name}\' Created!")
                else:
                    for i, x in enumerate(registered):
                        if scan_id in x:
                            print(f"{spacer}Welcome {registered[i][1]}!")
                            print(f"{registered[i][1]} added to the current Roster")
                            print(f"{spacer}Current Players: {len(current_players)}!")
                            current_players.append(
                                RankedMember(id=registered[i][0],
                                             name=registered[i][1],
                                             mmr=registered[i][2],
                                             winloss=registered[i][3],
                                             created=registered[i][4]))
        except ValueError as e:
            print("Invalid Command: " + e.__str__())


def remove():

    system("cls")
    global current_players
    while True:
        name = input(f"{spacer}Enter name you wish to remove from roster: ")
        name = name.lower()

        if name == "x":
            main()
            break

        if not any(name in player.name.lower() for player in current_players):

            print(f"{spacer}Name not in roster!")
            continue

        else:
            try:
                finding_players = iter(current_players)
                answer = "no"
                player = None

                while answer not in "yes":
                    player = next(x for x in finding_players if name in x.name.lower())
                    answer = input(f"{spacer}looking for {player.name}? ")
                    answer.lower()

                tmp = input(f"Are you sure you want to remove {player.name} from the roster? ")
                tmp = tmp.lower()
                if tmp in "yes":
                    print(f"Removed {player.name}")
                    current_players.remove(player)

            except StopIteration:
                print(f"{spacer}Could NOT find player by the Keyword {name}!")

            except Exception():
                raise Exception


def declare():  # @TODO Only one declare per round

    system("cls")
    global count
    while True:
        name = input(f"{spacer}Enter name you wish to search from roster: ")
        name = name.lower()

        if name == "exit":
            main()
            break

        if not any(name in player.name.lower() for player in current_players):

            print(f"{spacer}Could NOT find player by the Keyword {name}!")
            continue

        else:
            try:
                finding_players = iter(current_players)
                answer = "no"
                player = None

                while answer not in "yes":
                    player = next(x for x in finding_players if name in x.name.lower())
                    answer = input(f"{spacer}looking for {player.name}? ")
                    answer.lower()

                tmp = input(f"Are you sure you want {player.name}? ")
                tmp = tmp.lower()
                if tmp in "yes":
                    for i, x in enumerate(matched[count][0]):
                        if player in x:
                            win = x.index(player)
                            if win == 1:
                                lost = 0
                            else:
                                lost = 1
                            loser = matched[count][0][i][lost]
                            print(f"{spacer}{player.name} beat {loser.name}!!")
                            player.win(loser)

            except StopIteration:
                print(f"{spacer}No more players by the Keyword {name}!")

            except Exception() as e:
                print(e)
                continue


def stats():

    system("cls")
    while True:
        scan_id = input(f"{spacer}\nSwipe Card    ID:")

        if scan_id.lower() == "x":
            main()
            break

        try:
            count = 0
            for i, x in enumerate(registered):
                if scan_id in x:
                    tmp = RankedMember(id=registered[i][0],
                                 name=registered[i][1],
                                 mmr=registered[i][2],
                                 winloss=registered[i][3],
                                 created=registered[i][4])
                    print(f"{spacer}{str(tmp)}")
                    count = 1

            if count == 0:
                print(f"{spacer}Account not found!")

        except ValueError:
            print("Invalid Command!")



if __name__ == '__main__':
    pre_main()
    input("Pause")