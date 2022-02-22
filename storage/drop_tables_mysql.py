import mysql.connector

db_conn = mysql.connector.connect(host="54.190.110.228", user="backend_user", 
password="Password", database="events") 
 
db_cursor = db_conn.cursor() 
 
db_cursor.execute(''' 
                  DROP TABLE readings 
                  ''') 
 
db_conn.commit() 
db_conn.close()