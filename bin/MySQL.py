import os
import time
import zipfile

import mysql.connector

host = "overtimegaming.us.to"
username = "dreski"
password = "imidnightsnack15"
data = "magic_players"

database = mysql.connector.connect(
    host=f"{host}",
    user=f"{username}",
    passwd=f"{password}",
    database=f"{data}"
)

my_cursor = database.cursor()


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
    my_cursor.execute("CREATE TABLE players \
                          (id VARCHAR(255) PRIMARY KEY, \
                          name VARCHAR(40), \
                          mmr INT, \
                          winloss VARCHAR(20), \
                          created VARCHAR(40))")
    print("DONE!")


def get_players():
    my_cursor.execute("SELECT * FROM players")
    return my_cursor.fetchall()


def add_player(val):
    sql = "INSERT INTO players (id, name, mmr, winloss, created) VALUES (%s, %s, %s, %s, %s)"
    my_cursor.execute(sql, val)
    database.commit()
    print(my_cursor.rowcount, "record inserted.", val[1])


def update_normal(val):
    sql = "UPDATE players SET winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


def update_ranked(val):
    sql = "UPDATE players SET mmr = %s, winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


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
    my_cursor.execute("CREATE TABLE players \
                      (id VARCHAR(255) PRIMARY KEY, \
                      name VARCHAR(40), \
                      mmr INT, \
                      winloss VARCHAR(20), \
                      created VARCHAR(40))")
    print("DONE!")


if __name__ == '__main__':
    pass
