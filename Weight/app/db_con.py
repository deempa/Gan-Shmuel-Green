import mysql.connector
def showtables():
    
    mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="weight"
)

    print(mydb)

    mycursor=mydb.cursor()  

    mycursor.execute("SHOW TABLES")
    for x in mycursor:
        print(x) 