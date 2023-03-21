from flask import Flask, make_response, request, Response, jsonify
import sqlalchemy

app = Flask(__name__)

engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server/billdb")
#for local test (temp)
#engine = sqlalchemy.create_engine("mysql+pymysql://root:rootpass@localhost:3306/billdb")

def isproviderexist(name):
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


@app.route('/provider', methods=["POST"])
def post_provider():
    if request.is_json:
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
    if request.is_json:
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

