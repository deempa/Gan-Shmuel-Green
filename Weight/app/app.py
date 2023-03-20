from flask import Flask, request, make_response, render_template
from db_con import showtables

app = Flask(__name__)


@app.route('/')
def root():
    
    
    pass

@app.route("/weight", methods=["GET","POST"])
def weight():
    return render_template("index.html")









if __name__ == "__main__":
    app.run(host="0.0.0.0")