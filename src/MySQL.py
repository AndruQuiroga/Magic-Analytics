import mysql.connector

database = mysql.connector.connect(
  host="localhost",
  user="Dreski",
  passwd="imidnightsnack15",
  database="mydatabase"
)

my_cursor = database.cursor()

# my_cursor.execute("CREATE TABLE players (id INT PRIMARY KEY, name VARCHAR(40))")

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

my_cursor.execute("SELECT * FROM players")

myresult = my_cursor.fetchall()

for x in myresult:
    print(x)
