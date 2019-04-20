import datetime
import pickle
import random
from os import system
from os import name as n
import names
from bin.MySQL import *
from bin.match import Match
from bin.ranked_member import RankedMember


def clear():
    if n == 'nt':
        system('cls')
    else:
        system('clear')


def reorder():
    registered_players.sort(reverse=True)
    for rank, player in enumerate(registered_players):
        player.rank_num = rank+1


def pre_main():
    global registered_players
    global current_players
    global matched
    global spacer
    global current_match
    spacer = "==============================\n"

    test_players = [RankedMember(name=names.get_first_name(), id=i, mmr=random.randint(700, 1400), winloss='000000') for
                    i in range(18)]

    registered_players = []
    registered_players += test_players
    for player in get_players():
        registered_players.append(
            RankedMember(id=player[0],
                         name=player[1],
                         mmr=player[2],
                         winloss=player[3],
                         created=player[4]))

    reorder()
    current_players = []
    current_players += test_players
    current_match = Match([],0)
    matched = []
    print("Pre-main done!")
    main_menu()


def main_menu():
    clear()
    global current_match

    while True:

        put = input(f"{spacer}Insert Command: ")
        put = put.lower()

        if put == "list" or put == "ls":
            if not current_players:
                print("list is empty!")
                continue
            for player in current_players:
                print(player.name)
            continue

        if put == "debug":
            print(len(current_match.matches))

        if put in ("matchmake", "mm"):
            if current_match.num_matches != 0:
                if input("Not all matches have been concluded! ") == "force":
                    current_match = Match(current_players, current_match.round_number+1)
                else:
                    continue
            else:
                current_match = Match(current_players, current_match.round_number + 1)
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

        if put == "load":
            file = open(os.path.join(str(datetime.date.today()), f"round{input('Round #: ')}.obj"), 'rb')
            current_match = pickle.load(file)
            continue

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

    clear()
    global current_players
    while True:

        scan_id = input(f"{spacer}\nSwipe Card    ID:")

        if scan_id.lower() == "x":
            main_menu()
            break

        try:
            if any(int(scan_id) == player.id for player in current_players):
                print(f"{spacer}Player Already Logged In!")
                print(f"{spacer}Current Players: {len(current_players)}!")

            else:
                if not any(int(scan_id) == player.id for player in registered_players):
                    print(f"{spacer}ID not found in database!")
                    tmp = input("Want to to create a new Account? ")
                    name = input("Create an Account name: ")
                    add_player((scan_id, name, 1000, '000000', datetime.date.today()))
                    current_players.append(RankedMember(name=name, id=scan_id, created=datetime.date.today()))
                    print(f"{spacer}Account \'{current_players[-1].name}\' Created!")
                else:
                    for player in registered_players:
                        if int(scan_id) == player.id:
                            print(f"{spacer}Welcome {player.name}!")
                            print(f"{player.name} added to the current Roster")
                            current_players.append(player)
                            print(f"{spacer}Current Players: {len(current_players)}!")
        except ValueError as e:
            print("Invalid Command: " + e.__str__())


def remove():

    clear()
    global current_players
    while True:
        name = input(f"{spacer}Enter name you wish to remove from roster: ")
        name = name.lower()

        if name == "x":
            main_menu()
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


def declare():

    clear()
    if current_match == 0:
        input("No Current Matches!!")
        main_menu()

    while True:
        name = input(f"{spacer}Enter name you wish to search from roster: ")
        name = name.lower()

        if name == "x":
            main_menu()
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

                print(player.declared)

                if player.declared == 1:
                    print(f"{spacer}{player.name} already won this round!!")
                    continue
                if player.declared == -1:
                    print(f"{spacer}{player.name} already lost this round!!")
                    continue
                else:
                    tmp = input(f"Are you sure you want {player.name}? ")
                    tmp = tmp.lower()
                    if tmp in "yes":
                        found_player = 0
                        for match in current_match.matches:
                            if player in match:
                                found_player = 1
                                match.remove(player)
                                loser = match[0]
                                print(f"{spacer}{player.name} beat {loser.name}!!")
                                player.win(loser)
                                current_match.matches.remove(match)
                                current_match.save_round()
                        if found_player == 0:  # todo ranked objects do not retain self.declared
                            print("Could not find player in current match!")

            except StopIteration:
                print(f"{spacer}No more players by the Keyword {name}!")

            except Exception() as e:
                print(e)
                continue


def stats():

    clear()
    while True:
        scan_id = input(f"{spacer}\nSwipe Card    ID:")

        if scan_id.lower() == "x":
            main_menu()
            break

        try:
            found = False
            for player in registered_players:
                if int(scan_id) == player.id:
                    print(f"{spacer}{str(player)}")
                    found = True

            if not found:
                print(f"{spacer}Account not found!")

        except ValueError:
            print("Invalid Command!")


if __name__ == '__main__':
    pre_main()