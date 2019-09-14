import csv
import datetime
import os
from bin import MySQL
import json


def make_last_session(mainmenu):
    print("Creating session config for future use!")
    data = {"last_known_session": str(datetime.date.today()),
            "last_known_status": mainmenu.status}
    with open(os.path.join("local", f"last_session.json"), "w") as file:
        json.dump(data, file)
    print("Done!")


def make_offline_members():
    print("Creating Members from last local-offline session!")
    with open(os.path.join("local", f"last_session.json"), "r") as file:
        date = json.load(file)["last_known_session"]
    with open(os.path.join("local", date, f"local_database.csv"), "r") as file:
        reader = csv.reader(file, delimiter=',')
        members = [member for member in reader]
        print("Done!")
        return members


def make_local_database(mainmenu):
    print("Making local-offline database!")
    path = os.path.join("local", str(datetime.date.today()))
    if not os.path.exists(path):
        os.chdir("local")
        os.system("mkdir " + str(datetime.date.today()))
        os.chdir("..")

    if mainmenu.status:
        # normal_members = MySQL.get_members("normal")
        # ranked_members = MySQL.get_members("ranked")
        members = MySQL.get_members()

        with open(os.path.join(path, f"local_database.csv"), "w") as file:
            writer = csv.writer(file)

            for member in members:
                writer.writerow([item for item in member])

        # with open(os.path.join(path, f"local_database_normal.csv"), "w") as file:
        #     writer = csv.writer(file)
        #
        #     for member in normal_members:
        #         writer.writerow([item for item in member])
        #
        # with open(os.path.join(path, f"local_database_ranked.csv"), "w") as file:
        #     writer = csv.writer(file)
        #
        #     for member in ranked_members:
        #         writer.writerow([item for item in member])

    else:
        members = mainmenu.registered_members

        with open(os.path.join(path, f"local_database_{mainmenu.format}.csv"), "w") as file:
            writer = csv.writer(file)

            if mainmenu.format == "normal":
                for member in members:
                    writer.writerow([member.id,
                                     member.name,
                                     f"{member.career_wins:03d}{member.career_losses:03d}",
                                     member.created])
            else:
                for member in members:
                    writer.writerow([member.id,
                                     member.name,
                                     member.mmr,
                                     f"{member.career_wins:03d}{member.career_losses:03d}",
                                     member.created])

    print("Done!")
