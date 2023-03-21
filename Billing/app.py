from flask import Flask, make_response, request, jsonify
import sqlalchemy

import pandas as pd

app = Flask(__name__)

engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server/billdb")
#for local test (temp)
#engine = sqlalchemy.create_engine("mysql+pymysql://root:rootpass@localhost:3306/billdb")

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

@app.route('/rates', methods=["GET" "POST"])
def rates():
    if request.method == "GET":
        return "i got your get"
    elif request.method == "POST":
        filename = 'rates.xlsx'
        xlfile = pd.read_excel()
        xlfile.to_sql('Rates',con=engine,if_exists='replace')

        


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

