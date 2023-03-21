from flask import Flask, make_response, request, jsonify
import sqlalchemy
from openpyxl import Workbook, load_workbook
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData, select
import os


app = Flask(__name__)

engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server/billdb")

def is_provider_exist(name):
     conn=engine.connect()
     is_exist=conn.execute(sqlalchemy.text(f"select name from Provider where name='{name}'"))
     conn.close()
     if is_exist.first() != None:
          return True
     else:
          return False

def is_provider_id_exist(id):
    conn=engine.connect()
    is_exist=conn.execute(sqlalchemy.text(f"select id from Provider where id={id}"))
    conn.close()
    if is_exist.first() != None:
        return True
    else:
        return False

def is_truck_id_exist(id):
    conn=engine.connect()
    is_exist=conn.execute(sqlalchemy.text(f"select id from Trucks where id={id}"))
    conn.close()
    if is_exist.first() != None:
        return True
    else:
        return False


@app.route('/provider', methods=["POST"])
def post_provider():
    if request.is_json and request.method == "POST":
      data=request.json
      provider_name=data.get('name')
      if isproviderexist(provider_name):
          return make_response("Provider exists", 400)
      else:
           conn=engine.connect()
           conn.execute(sqlalchemy.text(f"INSERT INTO Provider (name) VALUES ('{provider_name}')"))
           conn.commit()
           getid=conn.execute(sqlalchemy.text(f"select id from Provider where name='{provider_name}'"))
           conn.close()
           response={"id" : getid.first()[0]}
           return make_response(jsonify(response), 200)
    else:
         return make_response("Bad Request",400)


@app.route('/provider/<id>', methods=["PUT"])
def update_provider_name(id):
    if request.is_json and request.method=="PUT":
        data=request.json
        name_to_update = data.get('name')
        if not is_provider_id_exist(id):
            return make_response("id does not exist",400)
        else:
            conn=engine.connect()
            conn.execute(sqlalchemy.text(f"UPDATE Provider SET name='{name_to_update}' WHERE id={id}"))
            conn.commit()
            conn.close()
            return make_response("Provider id updated", 200)
    else:
        return make_response("Bad Request",400)
    

@app.route('/truck', methods=["POST"])
def post_truck():
    if request.is_json:
        data=request.json
        provider_id = data.get('provider')
        truck_id = data.get('id')
        if not provider_id or not truck_id:
            return make_response("Missing provider or truck ID", 400)
        conn=engine.connect()
        provider_exists = conn.execute(sqlalchemy.text(f"select id from Provider id={provider_id}")).first()
        if not provider_exists:
            conn.close()
            return make_response("Provider not found", 404)
        truck_exists = conn.execute(sqlalchemy.text(f"select id from truck license_plate='{truck_id}'")).first()
        if truck_exists:
            conn.close()
            return make_response("Truck already registered", 400)
        conn.execute(sqlalchemy.text(f"Insert into truck (provider_id, license_plate) VALUES ('{provider_id}', '{truck_id}')"))
        conn.commit()
        getid=conn.execute(sqlalchemy.text(f"Select id from Truck license_plate='{truck_id}'"))
        truck_id = getid.first()[0]
        conn.close()
        response={"id" : truck_id}
        return make_response(jsonify(response), 200)
    else:
        return make_response("Bad Request",400)



@app.route('/truck/<id>', methods=["PUT"])
def get_put_truck(id):
    if request.method == "PUT" and  is_truck_id_exist(id):
        if request.is_json:
            data=request.json
            provider_id=data.get('provider_id')
            if is_provider_id_exist(provider_id):
               conn=engine.connect()
               conn.execute(sqlalchemy.text(f"UPDATE Trucks SET provider_id={provider_id} WHERE id={id}"))
               conn.commit()
               conn.close()
               return make_response("Updated truck provider",200)
            else:
                return make_response("Provider doesn't exist", 400)
        else:
            return make_response("Bad Request", 400)
    else:
        return make_response("Bad Request", 400)


@app.route('/rates', methods=["GET","POST"])
def rates():
    # define database metadata
    metadata = MetaData()

    # define Rates table schema
    rates_table = Table('Rates', metadata,
        Column('product_id', String),
        Column('rate', Integer),
        Column('scope', String)
        )
    
    if request.method == "GET":
        # load all records from Rates table
        with engine.connect() as conn:
            select_stmt = select(rates_table)
            result = conn.execute(select_stmt)
            data = result.fetchall()

        # create a new Excel workbook and worksheet
        wb = Workbook()
        ws = wb.active

        # write the data to the worksheet
        ws.append(['product_id', 'rate', 'scope'])
        for row in data:
            ws.append(list(row))

        # save the workbook to the "in" folder
        folder_path = "in"
        filename = os.path.join(folder_path, "export_rates.xlsx")
        wb.save(filename=filename)
        
        return make_response("see your data in/export_rates.xlsx", 200)

    elif request.method == "POST":
        # load Excel file from the "in" folder
        folder_path = "in"
        filename = os.path.join(folder_path, "rates.xlsx")
        wb = load_workbook(filename=filename, read_only=True)

        # delete all records from Rates table
        with engine.connect() as conn:
            conn.execute(rates_table.delete())
        
        # insert records from Excel file to Rates table
        ws = wb.active
        for row in ws.iter_rows(min_row=2):
            product_id = row[0].value
            rate = row[1].value
            scope = row[2].value
            with engine.connect() as conn:
                conn.execute(rates_table.insert().values(product_id=product_id, rate=rate, scope=scope))
        
        return make_response("saved", 200)
            
        
@app.route('/health', methods=["GET"])
def check_health():
        try:
              conn=engine.connect()
              conn.execute(sqlalchemy.text("select 1"))
              conn.close()
              return make_response("OK", 200)
        except:
              return make_response("Failure", 500)


if __name__ == "__main__":
    app.run(debug=True)

