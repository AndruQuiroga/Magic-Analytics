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


# my_cursor.execute("SELECT * FROM normal_members")
#
# myresult = my_cursor.fetchall()

# for x in myresult:
#     print(x)

# my_cursor.execute("ALTER TABLE players ADD COLUMN mmr INT")


def first_time():
    print("Creating new Database...")
    my_cursor.execute("CREATE TABLE members \
                          (id VARCHAR(255) PRIMARY KEY, \
                          name VARCHAR(40), \
                          mmr INT, \
                          total_winloss VARCHAR(20), \
                          ranked_winloss VARCHAR(20), \
                          created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, \
                          updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP)")

    # my_cursor.execute("CREATE TABLE ranked_members \
    #                           (id VARCHAR(255) PRIMARY KEY, \
    #                           name VARCHAR(40), \
    #                           mmr INT, \
    #                           winloss VARCHAR(20), \
    #                           created VARCHAR(40))")
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


def get_members():
    # if format == "Normal":
    #     my_cursor.execute("SELECT * FROM normal_members")
    #     return my_cursor.fetchall()
    # else:
    #     my_cursor.execute("SELECT * FROM ranked_members")
    #     return my_cursor.fetchall()
    my_cursor.execute("SELECT * FROM members")
    return my_cursor.fetchall()


def add_player(val):
    sql = "INSERT INTO members (id, name, mmr, total_winloss, ranked_winloss) VALUES (%s, %s, %s, %s, %s)"
    my_cursor.execute(sql, val)
    database.commit()

# def add_player_normal(val):
#     sql = "INSERT INTO normal_members (id, name, winloss, created) VALUES (%s, %s, %s, %s)"
#     my_cursor.execute(sql, val)
#     database.commit()
#     print(my_cursor.rowcount, "record inserted.", val[1])
#
#
# def add_player_ranked(val):
#     sql = "INSERT INTO ranked_members (id, name, mmr, winloss, created) VALUES (%s, %s, %s, %s, %s)"
#     my_cursor.execute(sql, val)
#     database.commit()


def update_normal(val):
    sql = "UPDATE members SET total_winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


def update_ranked(val):
    sql = "UPDATE members SET mmr = %s, ranked_winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


def update_database():
    print("=" * 40, "\nUpdating database from last local-offline session!")
    online_members = get_members()
    members = make_offline_members()
    for member, old_member in zip(members, online_members):
        if str(old_member[6]) < member[6]:
            update_ranked((member[2], member[0]))
        else:
            print("Up-To-Date Player")
    print(len(members), "record(s) updated.")

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
    my_cursor.execute("DROP TABLE ranked_members")
    my_cursor.execute("DROP TABLE normal_members")
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
    update_database()
    pass
