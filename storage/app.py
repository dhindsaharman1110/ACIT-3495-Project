# from platform import python_branch
# import connexion
# from connexion import NoContent
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
# import datetime
# import json
# import os.path
# import logging
# import yaml
# import logging.config
# from base import Base
# from age_n_gender import Age_n_gender
# from height_weight import Height_n_weight
# from random import random


# with open('app_config.yml', 'r') as f:
#     app_config = yaml.safe_load(f.read())



# with open('log_conf.yml', 'r') as f:
#     log_config = yaml.safe_load(f.read())
#     logging.config.dictConfig(log_config)
#     logger = logging.getLogger("basicLogger")

# DB_ENGINE = create_engine(f"mysql+pymysql://{app_config['datastore']['user']}:{app_config['datastore']['password']}@{app_config['datastore']['hostname']}:{app_config['datastore']['port']}/{app_config['datastore']['db']}")
# Base.metadata.bind = DB_ENGINE
# DB_SESSION = sessionmaker(bind=DB_ENGINE)

# def trace_id(time_stamp):
#     return str(f"{time_stamp}{str(random())}")


# def report_age_n_gender_reading(body):
#     trace_rec = trace_id(body['timestamp'])
#     session = DB_SESSION()
#     agd = Age_n_gender(body['user_id'],
#                        body['user_name'], 
#                        body['user_age'], 
#                        body['user_gender'],
#                        body['timestamp'],
#                        body['trace_id'])
#     session.add(agd)
#     session.commit()
#     session.close()
#     logger.info(f"Stored event 'age_n_gender_reading' request with a trace id of {body['trace_id']}")
#     return NoContent, 201


# def report_height_n_weight_reading(body):
#     trace_rec = trace_id(body['timestamp'])
#     session = DB_SESSION()
#     hnw = Height_n_weight(body['user_id'],
#                        body['user_name'], 
#                        body['user_height'], 
#                        body['user_weight'],
#                        body['timestamp'])
#     session.add(hnw)
#     session.commit()
#     session.close()

#     logger.info(f"Stored event 'height_n_weight_reading' request with a trace id of {body['trace_id']}")
#     return NoContent, 201




# app = connexion.FlaskApp(__name__, specification_dir='')
# app.add_api("openapi.yml", strict_validation=True, validate_responses=True)


# if __name__ == "__main__":
#     app.run(port=8090)



import mysql.connector
from connexion import NoContent




from flask import Flask, render_template, request
# from flask_mysqldb import MySQL
app = Flask(__name__)


app.config['MYSQL_HOST'] = '54.190.110.228'
app.config['MYSQL_USER'] = 'backend_user'
app.config['MYSQL_PASSWORD'] = 'Password'
app.config['MYSQL_DB'] = 'events'

# mysql = MySQL(app)

@app.route('/readings', methods=['GET', 'POST'])
def index():
    db_conn = mysql.connector.connect(host="54.190.110.228", user="backend_user", password="Password", database="events")
    db_cursor = db_conn.cursor()
    print(request.json)
    if request.method == 'POST':
        
        user_fname = request.json['user_fname']
        print(user_fname)
        user_lname = request.json['user_lname']
        user_age = request.json['user_age']
        user_gender = request.json['user_gender']
        user_height = request.json['user_height']
        user_weight = request.json['user_weight']
        db_cursor.execute("INSERT INTO events.readings (user_fname, user_lname, user_age, user_gender, user_height, user_weight) VALUES (%s, %s, %s, %s, %s, %s)", (user_fname, user_lname, user_age, user_gender, user_height, user_weight))
        db_conn.commit()
        db_conn.close()
        return 'success'




if __name__ == '__main__':
    app.run(port=8090)