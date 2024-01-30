import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="studentrecordsystem"
)

mycursor = mydb.cursor()

mycursor.execute("SELECT * FROM RESULTS")

for data in mycursor.fetchall():
    print(data)