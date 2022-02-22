import mysql.connector

db_conn = mysql.connector.connect(host="54.190.110.228", user="backend_user", password="Password", database="events")
db_cursor = db_conn.cursor()

db_cursor.execute(''' 
          CREATE TABLE readings
          (id INT NOT NULL AUTO_INCREMENT, 
           user_fname VARCHAR(250) NOT NULL,
           user_lname VARCHAR(250) NOT NULL,
           user_age VARCHAR (3) NOT NULL,
           user_gender VARCHAR(250) NOT NULL, 
           user_height VARCHAR(3) NOT NULL,
           user_weight VARCHAR(3) NOT NULL,
           CONSTRAINT reading_pk PRIMARY KEY (id)) 
          ''')

db_conn.commit()
db_conn.close()