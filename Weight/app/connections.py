import mysql.connector




def get_connection():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123",
        database="weight"
    )

    return db




def register_truck(container_id,wieght,unit):
    db=get_connection()
    cursor=db.cursor()
    sql = "INSERT INTO containers_registered (container_id, weight, unit) VALUES (%s, %s, %s)"
    val= (container_id, wieght, unit)
    try:
        cursor.execute(sql, val)
        db.commit
    
        print(cursor.rowcount, "record inserted")
    except Exception:
        print("insertion failed")





# def Database_check():
#     mycur=connection.cursor()
#     mycur.execute("SHOW DATABASES")
# # Fetch all the rows in a list of lists result
#     result = mycur.fetchall()
#     for r in result:
#         if "weight" not in r:
#             with open('weightdb.sql','r') as f:
#                 sql_command = f.read()
#                 mycur.execute(sql_command,multi=True)
#                 connection.commit()
#                 connection.close()
#         else:
#             mycur.execute("use weight")
# def execute(query):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(str(query))
#     cur.close()
#     conn.close()

# def execute_commit(query):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(str(query))
#     conn.commit()
#     cur.close()
#     conn.close()

# def fetchall(query):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(str(query))
#     res = cur.fetchall()
#     cur.close()
#     conn.close()
#     return res

# def fetchone(query):
#     conn = get_connection()
#     cur = conn.cursor()
#     cur.execute(str(query))
#     res = cur.fetchone()
#     cur.close()
#     conn.close()
#     return res

# def db_health_check():
#     try:
#         with get_connection().cursor() as cursor:
#             sql = "select 1"
#             cursor.execute(sql)

#         return True
#     except Exception:
#         return False
