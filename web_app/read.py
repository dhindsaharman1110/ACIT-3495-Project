import mysql.connector

db = mysql.connector.connect(
  host="54.190.110.228",
  user="backend_user",
  password="Password",
  database="events"
)

dbcursor = db.cursor()

max_age = dbcursor.execute("SELECT MAX(user_age) FROM readings;")
min_age = dbcursor.execute("SELECT MIN(user_age) FROM readings;")
avg_age = dbcursor.execute("SELECT AVG(user_age) FROM readings;")

max_height = dbcursor.execute("SELECT MAX(user_height) FROM readings;")
min_height = dbcursor.execute("SELECT MIN(user_height) FROM readings;")
avg_height = dbcursor.execute("SELECT AVG(user_height) FROM readings;")

max_weight = dbcursor.execute("SELECT MAX(user_weight) FROM readings;")
min_weight = dbcursor.execute("SELECT MIN(user_weight) FROM readings;")
avg_weight = dbcursor.execute("SELECT AVG(user_weight) FROM readings;")

myresult = dbcursor.fetchall()

db.commit()
db.close()


