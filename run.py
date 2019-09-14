from bin import main_menu
import os


def check_if_folders_exist():   
    if not os.path.exists("local"):
        os.system("mkdir local")


if __name__ == '__main__':

    check_if_folders_exist()
    main = main_menu.MainMenu("normal")
    for player in main.current_players:
        player.career_wins += 1
        main.update_members()
        print(player)
