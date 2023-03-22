import mysql.connector




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
    sql = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
    val= (container_id, wieght, unit)
    
    cursor.execute(sql, val)
    db.commit
    
    
        


def insert_transaction_in(direction,truck,containers, truck_bruto,unit_of_measure_bruto,produce,datetime):
    db=get_connection()
    cursor=db.cursor()
    sql = "INSERT INTO transactions (direction, truck, containers, bruto, truckTara, neto, produce, datetime) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    val=(direction,truck,containers,truck_bruto,-1,-1,produce,datetime)
    
    cursor.execute(sql,val)
    db.commit
    register_container(container_id=containers,wieght=-1,unit=unit_of_measure_bruto)   
    
