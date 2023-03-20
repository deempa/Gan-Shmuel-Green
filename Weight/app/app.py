from flask import Flask, request, make_response

app = Flask(__name__)

@app.route('/')
def root():
    pass

@app.route("/weight", methods=["GET","POST"])
def weight():
    pass