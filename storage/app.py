import mysql.connector
#from connexion import NoContent

import pymongo
import requests

import json

from flask import Flask, render_template, request
# from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '54.190.110.228'
app.config['MYSQL_USER'] = 'backend_user'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'events'

# mysql = MySQL(app)

def calculate_bmr_o(weight, height, age, gender):
    if gender == "Male":
        bmr_male = 66.5 + (13.75 * int(weight)) + (5 * int(height)) - (6.755 * int(age))
        return bmr_male
    elif gender == "Female":
        bmr_female = 655.1 + (9.6 * int(weight)) + (1.8 * int(height)) - (4.7 * int(age))
        return bmr_female
    else:
        return "Unexpected value of gender"


@app.route('/readings', methods=['GET', 'POST'])
def index():
    db_conn = mysql.connector.connect(host="54.190.110.228", user="backend_user", password="Password", database="events")
    db_cursor = db_conn.cursor()
    print(request.json)
    if request.method == 'POST':
        
        user_fname = request.json['user_fname']
        print(user_fname)
        user_lname = request.json['user_lname']
        user_email = request.json['user_email']
        user_phone = request.json['user_phone']
        user_age = request.json['user_age']
        user_gender = request.json['user_gender']
        user_height = request.json['user_height']
        user_weight = request.json['user_weight']

        user_bmr = calculate_bmr_o(user_weight, user_height, user_age, user_gender)


        db_cursor.execute("INSERT INTO events.readings (user_fname, user_lname, user_email, user_phone, user_age, user_gender, user_height, user_weight, user_BMR) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (user_fname, user_lname, user_email, user_phone, user_age, user_gender, user_height, user_weight, user_bmr))
        db_conn.commit()
        db_conn.close()







    

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
    

    
        dbcursor.execute("SELECT user_BMR FROM readings WHERE id = %s;", (user_id[0]))
        user_BMR = dbcursor.fetchall()
        user_BMR = round(user_BMR[0][0])
        print("------")
        print(user_BMR)
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



        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["events"]
        col = db["readings"]

        x = col.find()
    
        myobj = {}

        for data in x:
            for key, value in data.items():
                temp=value
               # print(type(value))

                if key != "_id":
                    myobj[key] = str(value)
                else:
                    pass
        print(myobj)
        json_object = json.dumps(myobj, indent =4)
        print(json_object)
        r=requests.post("http://127.0.0.1:8080/result", json=json_object)
        return 'success'




if __name__ == '__main__':
    app.run(port=8090)
