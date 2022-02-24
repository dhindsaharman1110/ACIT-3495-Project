import mysql.connector

db = mysql.connector.connect(
  host="54.190.110.228",
  user="backend_user",
  password="Password",
  database="events"
)

dbcursor = db.cursor(buffered=True)
dbcursor.execute("SELECT MAX(user_age) FROM readings;")
max_age = dbcursor.fetchall()

dbcursor.execute("SELECT MIN(user_age) FROM readings;")
min_age = dbcursor.fetchall()

dbcursor.execute("SELECT AVG(user_age) FROM readings;")
avg_age = dbcursor.fetchall()

dbcursor.execute("SELECT MAX(user_height) FROM readings;")
max_height = dbcursor.fetchall()

dbcursor.execute("SELECT MIN(user_height) FROM readings;")
min_height = dbcursor.fetchall()

dbcursor.execute("SELECT AVG(user_height) FROM readings;")
avg_height = dbcursor.fetchall()

dbcursor.execute("SELECT MAX(user_weight) FROM readings;")
max_weight = dbcursor.fetchall()

dbcursor.execute("SELECT MIN(user_weight) FROM readings;")
min_weight = dbcursor.fetchall()

dbcursor.execute("SELECT AVG(user_weight) FROM readings;")
avg_weight = dbcursor.fetchall()

dbcursor.execute("SELECT COUNT(*) FROM readings")
user_id = dbcursor.fetchall()

dbcursor.execute("SELECT user_BMR FROM readings WHERE id == %s;", (user_id))
user_BMR = dbcursor.fetchall()

db.commit()
db.close()

def calculate_bmr(weight, height, age):
    bmr_male = 66.5 + (13.75 * int(weight)) + (5 * int(height)) - (6.755 * int(age))
    bmr_female = 655.1 + (9.6 * int(weight)) + (1.8 * int(height)) - (4.7 * int(age))
    return bmr_male, bmr_female

print(max_age[0][0])

min_bmr_male, min_bmr_female = calculate_bmr(min_weight[0][0], min_height[0][0], min_age[0][0])
max_bmr_male, max_bmr_female = calculate_bmr(max_weight[0][0], max_height[0][0], max_age[0][0])
avg_bmr_male, avg_bmr_female = calculate_bmr(avg_weight[0][0], avg_height[0][0], avg_age[0][0])



from pymongo import MongoClient
  
try:
    conn = MongoClient()
    print("Connected successfully!!!")
except:  
    print("Could not connect to MongoDB")
  
# database
db = conn.events
  
# Created or Switched to collection names: my_gfg_collection
collection = db.readings
  
emp_rec1 = {
        "min_bmr_male": min_bmr_male,
        "min_bmr_female": min_bmr_female
        }
emp_rec2 = {
        "max_bmr_male": max_bmr_male,
        "max_bmr_female": max_bmr_female
        }
emp_rec3 = {
        "avg_bmr_male": avg_bmr_male,
        "avg_bmr_female": avg_bmr_female,
        }
emp_rec4 = {
        "user_BMR": user_BMR
        }


# Insert Data
rec_id1 = collection.insert_one(emp_rec1)
rec_id2 = collection.insert_one(emp_rec2)
rec_id3 = collection.insert_one(emp_rec3)
rec_id4 = collection.insert_one(emp_rec4)

print("Data inserted with record ids",rec_id1," ",rec_id2)
  
# Printing the data inserted
cursor = collection.find()
for record in cursor:
    print(record)
