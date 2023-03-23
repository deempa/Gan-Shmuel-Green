from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
import os, json
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename
import re
import connections
import requests

UPLOAD_FOLDER = '/in'

ALLOWED_EXTENSIONS = set(['csv','json'])
#test comment1
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
#8083
db = mysql.connector.connect(
    host="localhost",
    user="root",
    port=3300,
    password="123",
    database="weight"
)

#test comment1
#test comment 2
isconnected=0
try:
    db=connections.get_connection()
except Exception:
    db=None


app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route('/')
def root():
    return redirect(url_for('post_weight'))


@app.route("/batch-weight", methods=["GET", "POST"])
def bw():
    if request.method == 'GET':
        return render_template("bw.html")
    elif request.method == 'POST':
        if 'file' not in request.files:
            return "no file part"
        file = request.files['file']
        if file.filename == '':
            return "No selected file"

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ext=filename.split(".")[-1]
        

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            if ext =='csv':

                with open(f'../in/{filename}', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        rows = print(row)
                return (f"{rows}")
            elif ext=='json':
                with open(f'../in/{filename}', 'r') as file:
                    data=json.load(file)  
                return (f"{data}")    
        else:
                return "Invalid file type"

@app.route("/weight", methods=["GET", "POST"])
def post_weight():
    if request.method == 'POST':
        direction = request.form['direction']
        truck = request.form['truck_license']
        produce = request.form['product_delivered']
        truck_bruto = request.form['truck_bruto_weight']
        unit_of_measure_bruto = request.form['unit_of_measure_1']
        # date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
        force =  request.form['force']
        containers=request.form['container_id']
        if truck is None or truck == '' and direction != 'none':
            return 'Standalone containers must be inserted with Direction as none'
        if containers == '':
            return 'Container id is required'
        if produce == '':
            produce = 'na'
        if has_numbers(produce):
            return "Invalid product! you cnnot have numbers in product's names"
        if re.search(r'\D', truck_bruto):
            return "Invalid weight inserted to bruto weight"
        if direction == "in":
            return connections.handle_in(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        if direction == "out":
            return connections.handle_out(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        return "hello"

    elif request.method == 'GET':
        return render_template('index.html')


@app.route("/health")
def healthcheck():
	return "", 200


if __name__ == "__main__":
    app.run(host="0.0.0.0")
