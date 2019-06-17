import json
import os
import time
import zipfile

import mysql.connector
from bin.export import *

host = "overtimegaming.us.to"
username = "dreski"
password = "imidnightsnack15"
data = "magic_players"

try:
    database = mysql.connector.connect(
        host=f"{host}",
        user=f"{username}",
        passwd=f"{password}",
        database=f"{data}"
    )

    my_cursor = database.cursor()
    online = True
    print("Server is ONLINE!!")
    print("=" * 40)

except mysql.connector.Error as e:
    print(e)
    online = False
    print("Server is Offline!")
    print("=" * 40)


# my_cursor.execute("SHOW TABLES")
#
# for x in my_cursor:
#   print(x)

# my_cursor.execute("CREATE DATABASE magic_players")


# my_cursor.execute("SELECT * FROM players")
#
# myresult = my_cursor.fetchall()
#
# for x in myresult:
#     print(x)

# my_cursor.execute("ALTER TABLE players ADD COLUMN mmr INT")


def first_time():
    print("Creating new Database...")
    my_cursor.execute("CREATE TABLE normal_members \
                          (id VARCHAR(255) PRIMARY KEY, \
                          name VARCHAR(40), \
                          winloss VARCHAR(20), \
                          created VARCHAR(40))")

    my_cursor.execute("CREATE TABLE ranked_members \
                              (id VARCHAR(255) PRIMARY KEY, \
                              name VARCHAR(40), \
                              mmr INT, \
                              winloss VARCHAR(20), \
                              created VARCHAR(40))")
    print("DONE!")


def test_online():
    if online:
        try:
            with open(os.path.join("local", f"last_session.json"), "r") as file:
                if not json.load(file)["last_known_status"]:
                    print("Last Known Status OFFLINE!")
                    update_database()
        except FileNotFoundError:
            print("Last_session not found!\nSkipping Update")
    return online


def get_members(format):
    if format == "Normal":
        my_cursor.execute("SELECT * FROM normal_members")
        return my_cursor.fetchall()
    else:
        my_cursor.execute("SELECT * FROM ranked_members")
        return my_cursor.fetchall()


def add_player_normal(val):
    sql = "INSERT INTO normal_members (id, name, winloss, created) VALUES (%s, %s, %s, %s)"
    my_cursor.execute(sql, val)
    database.commit()
    print(my_cursor.rowcount, "record inserted.", val[1])


def add_player_ranked(val):
    sql = "INSERT INTO ranked_members (id, name, mmr, winloss, created) VALUES (%s, %s, %s, %s, %s)"
    my_cursor.execute(sql, val)
    database.commit()


def update_normal(val):
    sql = "UPDATE normal_members SET winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


def update_ranked(val):
    sql = "UPDATE ranked_members SET mmr = %s, winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


def update_database():
    print("=" * 40, "\nUpdating database from last local-offline session!")
    normal = make_offline_members("Normal")
    for member in normal:
        update_normal((member[2], member[0]))
    print(len(normal), "record(s) updated.")

    ranked = make_offline_members("Ranked")
    for member in ranked:
        update_ranked((member[2], member[3], member[0]))
    print(len(ranked), "record(s) updated.")
    print("Successfully updated Online Database!\n", "=" * 40)


def backup():
    filestamp = time.strftime('%Y-%m-%d-%I-%M')
    os.popen(f"mysqldump --all-databases -u {username} -p{password} -c -h {host} > {data}_{filestamp}.sql")

    os.system("mkdir " + filestamp)
    zipf = zipfile.ZipFile(os.path.join(filestamp, f'{data}.zip'), 'w', zipfile.ZIP_DEFLATED)
    zipf.write(f'{data}_{filestamp}.sql')
    zipf.close()


def delete():
    print("Deleting Database...")
    my_cursor.execute("DROP TABLE players")
    print("Creating new Database...")
    # my_cursor.execute("CREATE TABLE players \
    #                   (id VARCHAR(255) PRIMARY KEY, \
    #                   name VARCHAR(40), \
    #                   mmr INT, \
    #                   winloss VARCHAR(20), \
    #                   created VARCHAR(40))")
    print("DONE!")


if __name__ == '__main__':
    # delete()
    # first_time()
    pass
