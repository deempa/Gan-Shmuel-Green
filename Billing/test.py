
from flask import Flask, make_response, request, jsonify, send_from_directory
import sqlalchemy, datetime, os, json
from openpyxl import Workbook, load_workbook
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select

engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server:3306/billdb")

def js_name(prov_id):
    conn=engine.connect()
    result=conn.execute(sqlalchemy.text(f"SELECT name FROM Provider WHERE id = {prov_id}")).fetchone()
    conn.close()
    prov_name=result[0]  
    return prov_name

def js_truckCount(provider_id,per):
    conn=engine.connect()

    if per == "trk":
        result = conn.execute(sqlalchemy.text(f"SELECT COUNT(*) FROM Trucks WHERE provider_id = {provider_id}")).fetchone()
        truck_count = result[0]
        conn.close()
        return truck_count
   
    elif per == "sess":
        result = conn.execute(sqlalchemy.text(f"SELECT id FROM Trucks WHERE provider_id = {provider_id}")).fetchall()
        truck_ids = [{r[0]} for r in result]
        conn.close()
        return truck_ids 


def js_prod_and_pay(provider_id,per):
    #set total_pay and products_list
    total_pay = 0

    products_list = []

    conn=engine.connect()

    #making dictionaries of products
    result=conn.execute(sqlalchemy.text(f"SELECT product_id FROM Rates WHERE scope = {provider_id} OR scope = 'All'")).fetchall()
 
    for row in result:
        prod_id = row[0]
        prod_sess = "13"
        amount_kg = 3
        rate_res=conn.execute(sqlalchemy.text(f"SELECT rate FROM Rates WHERE product_id = '{prod_id}'")).fetchone()
        rate = rate_res[0]
        pay = amount_kg * rate
        total_pay += pay
        products_list.append({"product": prod_id, "count": prod_sess, "amount": amount_kg, "rate": rate, "pay": pay})
    
    conn.close()

    if per == "prod":
        return products
    elif per == "total":
        return total_pay 

#main
prov_id = input("enter the id: ")
t1 = input("enter t1: ")
t2 = input("enter t2: ")

if t1 == "" or t2 == "":
    #defult time for the bill
    t1=datetime.datetime.now().strftime("%Y%m01000000")
    t2=datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    
#vars
prov_name = js_name(prov_id)
time_1 = datetime.datetime.strptime(t1, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
time_2 = datetime.datetime.strptime(t2, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
truck_count = js_truckCount(prov_id,"trk")
session_count = js_truckCount(prov_id,"sess")
products = js_prod_and_pay(prov_id,"prod")
total_pay = js_prod_and_pay(prov_id,"total")

# Create the dictionary
bill = {
    "id": prov_id, 
    "name": prov_name, 
    "from": time_1, 
    "to": time_2, 
    "truckCount": truck_count, 
    "sessionCount": 30,  #tmp 
    "products": products,
    "total": total_pay 
}

# convert the dictionary to a JSON string 
bill_json = json.dumps(bill, indent=4)

print(bill_json)
print("--------------------------------------")
print(session_count)