from flask import Flask
import sqlalchemy

app=Flask(__name__)

engine = sqlalchemy.create_engine("mysql+pymysql://billdbuser:billdbpass@mysql-server/billdb")


if __name__ == "__main__":
    app.run()