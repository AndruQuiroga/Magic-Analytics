import datetime
import pickle
import random
from os import name as n
from os import system

import names

from bin.MySQL import *
from bin.html_writer import write_html
from bin.ranked.ranked_match import Match, RankedMatch
from bin.ranked.ranked_member import Member, RankedMember


def clear():
    if n == 'nt':
        system('cls')
    else:
        system('clear')


def pre_main(gu):
    global gui
    gui = gu
    global registered_players
    global current_players
    global current_match
    global match_type
    global member_type
    global spacer
    spacer = "==============================\n"

    event_tp = input("What Format?")

    if event_tp == "normal":
        match_type = Match
        member_type = Member
    else:
        match_type = RankedMatch
        member_type = RankedMember

    # test_players = [member_type(name=names.get_first_name(), id=i, mmr=random.randint(800, 1300), winloss='000000')
    #                 for i in range(28)]
    # for player in test_players:
    #     add_player((player.id, player.name, 1000, '000000', datetime.date.today()))

    registered_players = []
    for player in get_players():
        registered_players.append(
            member_type(id=player[0],
                        name=player[1],
                        mmr=player[2],
                        winloss=player[3],
                        created=player[4]))

    current_players = []
    current_players += registered_players
    current_match = match_type([], 0)

    gui.write_to_log("Pre-main done!")


def main_menu(put):
    # clear()

    global current_players
    global current_match

    put = put.lower()

    if put == "list" or put == "ls":
        if not current_players:
            gui.write_to_log("list is empty!")

        for player in current_players:
            gui.write_to_log(player.name)


    if put == "b":
        current_match.re_rank(registered_players)
        write_html(registered_players)

    if put in ("matchmake", "mm"):
        if current_match.num_matches != 0:
            if input("Not all matches have been concluded! ") == "force":
                current_match.re_rank(registered_players)
                write_html(registered_players)
                current_match = match_type(current_players, current_match.round_number + 1)
        else:
            current_match.re_rank(registered_players)
            write_html(registered_players)
            current_match = match_type(current_players, current_match.round_number + 1)


    if put == "reset":
        pre_main()


    if put == "clear":
        tmp = input("ARE YOU SURE YOU WANT TO CLEAR SQL DATABASE?!? ")
        if tmp == "ironisbronze":
            delete()
            pre_main()

        else:
            gui.write_to_log("INCORRECT PASSWORD")

    if put == "add" or put == "a":
        add()

    if put == "remove" or put == "r":
        remove()

    if put == "stats" or put == "s":
        stats()

    if put == "declare" or put == "d":
        declare()

    if put == "load":
        file = open(os.path.join("saves", str(datetime.date.today()), f"round{input('Round #: ')}.obj"), 'rb')
        current_match = pickle.load(file)

    if put == "help" or put == "?":
        gui.write_to_log(f"{spacer}Valid Commands:"
              f"\nAdd: Add a player to the roster"
              f"\nRemove: Remove a player from roster"
              f"\nMatchMake: Create matchups"
              f"\nStats: Look up Stats from id"
              f"\nDeclare: Declare a winner from matchup"
              f"\nList: Look up current Roster"
              f"\nX: to return back to main menu")

    else:
        gui.write_to_log("INVALID COMMAND! Try \'help\'.")


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
                gui.write_to_log(f"{spacer}Player Already Logged In!")
                gui.write_to_log(f"{spacer}Current Players: {len(current_players)}!")

            else:
                if not any(int(scan_id) == player.id for player in registered_players):
                    gui.write_to_log(f"{spacer}ID not found in database!")
                    tmp = input("Want to to create a new Account? ")
                    if tmp not in "yes":
                        continue
                    name = input("Create an Account name: ")
                    add_player((scan_id, name, 1000, '000000', datetime.date.today()))
                    current_players.append(member_type(name=name, id=scan_id, created=datetime.date.today()))
                    gui.write_to_log(f"{spacer}Account \'{current_players[-1].name}\' Created!")
                else:
                    for player in registered_players:
                        if int(scan_id) == player.id:
                            gui.write_to_log(f"{spacer}Welcome {player.name}!")
                            gui.write_to_log(f"{player.name} added to the current Roster")
                            current_players.append(player)
                            gui.write_to_log(f"{spacer}Current Players: {len(current_players)}!")
        except ValueError as e:
            gui.write_to_log("Invalid Command: " + e.__str__())


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
            gui.write_to_log(f"{spacer}Name not in roster!")
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
                    gui.write_to_log(f"Removed {player.name}")
                    current_players.remove(player)

            except StopIteration:
                gui.write_to_log(f"{spacer}Could NOT find player by the Keyword {name}!")

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

            gui.write_to_log(f"{spacer}Could NOT find player by the Keyword {name}!")
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

                found_player = 0
                for match in current_match.matches:
                    if player in match:
                        found_player = 1
                if found_player == 0:
                    gui.write_to_log(f"{player.name} has already concluded his/her match!")

                else:
                    tmp = input(f"Are you sure {player.name} won? ")
                    tmp = tmp.lower()
                    if tmp in "yes":
                        for match in current_match.matches:
                            if player in match:
                                match.remove(player)
                                loser = match[0]
                                gui.write_to_log(f"{spacer}{player.name} beat {loser.name}!!")
                                player.win(loser)
                                current_match.matches.remove(match)
                                current_match.save_round()

            except StopIteration:
                gui.write_to_log(f"{spacer}No more players by the Keyword {name}!")

            except Exception() as e:
                gui.write_to_log(e)
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
                    gui.write_to_log(f"{spacer}{str(player)}")
                    found = True

            if not found:
                gui.write_to_log(f"{spacer}Account not found!")

        except ValueError:
            gui.write_to_log("Invalid Command!")


if __name__ == '__main__':
    pre_main()
