import mysql.connector

database = mysql.connector.connect(
  host="localhost",
  user="Dreski",
  passwd="imidnightsnack15",
  database="mydatabase"
)

my_cursor = database.cursor()


# my_cursor.execute("SHOW TABLES")
#
# for x in my_cursor:
#   print(x)

#
# sql = "INSERT INTO players (id, name) VALUES (%s, %s)"
# val = [
#   ('00961715', 'Peter'),
#   ('00961845', 'Amy '),
#   ('00961145', 'Hannah'),
#   ('00967742', 'Michael'),
#   ('00962135', 'Sandy'),
#   ('00965588', 'Betty'),
#   ('00969845', 'Richard'),
#   ('00968452', 'Susan'),
#   ('00961254', 'Vicky'),
#   ('00961534', 'Ben'),
#   ('00968895', 'William'),
# ]
#
# my_cursor.executemany(sql, val)
#
# database.commit()
#
# print(my_cursor.rowcount, "was inserted.")


# my_cursor.execute("SELECT * FROM players")
#
# myresult = my_cursor.fetchall()
#
# for x in myresult:
#     print(x)

# my_cursor.execute("ALTER TABLE players ADD COLUMN mmr INT")


def get_players():
    my_cursor.execute("SELECT * FROM players")
    return my_cursor.fetchall()


def add_player(val):
    sql = "INSERT INTO players (id, name, mmr, winloss, created) VALUES (%s, %s, %s, %s, %s)"
    my_cursor.execute(sql, val)
    database.commit()
    print(my_cursor.rowcount, "record inserted.", val[1])


def update(val):
    sql = "UPDATE players SET mmr = %s, winloss = %s WHERE id = %s"
    my_cursor.execute(sql, val)
    database.commit()


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