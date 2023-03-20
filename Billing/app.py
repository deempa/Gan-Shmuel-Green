from flask import Flask, make_response
import sqlalchemy

app = Flask(__name__)

""" @app.route('/provider')
def post_provider():
    return "in progres" """

@app.route('/health')
def check_health():
        return "OK", 200
        
engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server/billdb")


if __name__ == "__main__":
    app.run()