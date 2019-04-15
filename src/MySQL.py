import mysql.connector

database = mysql.connector.connect(
  host="localhost",
  user="Dreski",
  passwd="imidnightsnack15",
  database="mydatabase"
)

my_cursor = database.cursor()

# my_cursor.execute("CREATE TABLE mmr (id VARCHAR(255) PRIMARY KEY, mmr INT)")

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

def get_players():
    my_cursor.execute("SELECT * FROM players")
    return my_cursor.fetchall()


def add_player(val):
    sql = "INSERT INTO players (id, name) VALUES (%s, %s)"
    my_cursor.execute(sql, val)
    database.commit()
    print(my_cursor.rowcount, "record inserted.")


def get_mmr():
    sql = "SELECT \
      id \
      FROM players \
      INNER JOIN mmr ON players.id = mmr.id"
    my_cursor.execute(sql)
    return my_cursor.fetchall()

if __name__ == '__main__':
    get_mmr()