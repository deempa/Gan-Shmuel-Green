import mysql.connector
from flask import Flask



def get_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="weight"
    )

    return db




def register_container(container_id,wieght,unit):
    db=get_connection()
    cursor=db.cursor()
    sql= "SELECT * FROM containers_registered"
    cursor.execute(sql)
    data=cursor.fetchall()
    for i in data:
        if i[0] == container_id:
            return (f"Container with id {container_id} already exist, skipped")
        
    
    sql = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
    val= (container_id, wieght, unit)
    
    cursor.execute(sql, val)
    db.commit
    
        


def insert_transaction(direction,truck,containers, truck_bruto,
                       unit_of_measure_bruto,produce,datetime,force):
    if direction=="in":
        
        
        db=get_connection()
        cursor=db.cursor()
        sql = "INSERT INTO transactions (direction, truck, containers, bruto, truckTara, neto, produce, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        containers_str=",".join(containers)
    
        val=(direction,truck,containers_str,truck_bruto,-1,-1,produce,datetime)
        
        cursor.execute(sql,val)
        db.commit
        
        
        for i in containers:
            register_container(container_id=i,wieght=-1,unit=unit_of_measure_bruto)

            
        sql= "SELECT * FROM transactions"
        cursor.execute(sql)
        data=cursor.fetchall()
        for row in data:
            print (row)

        sql= "SELECT * FROM containers_registered"
        cursor.execute(sql)
        data= cursor.fetchall()
        for i in data:
            print(i)


def unknown():
    arr=[]
    db=get_connection()
    cursor=db.cursor()
    sql= "SELECT * FROM containers_registered"
    cursor.execute(sql)
    data=cursor.fetchall()
    for i in data:
        if i[1]==-1:
            arr.append(i[0])

    return arr