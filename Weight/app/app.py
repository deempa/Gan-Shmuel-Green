from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
import os, json
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename
import re

<<<<<<< HEAD
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
#8083
UPLOAD_FOLDER = './'
=======
UPLOAD_FOLDER = '../in'

ALLOWED_EXTENSIONS = set(['csv','json'])
>>>>>>> refs/remotes/origin/Weight



# db=mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="123",
#     database="weight"
# )
isconnected = 0
# if db.isconnected():
#     isconnected = 1
# else:
#     isconnected = 0

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

                with open(f'./{filename}', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        rows = print(row)
                return (f"{rows}")
            elif ext=='json':
                with open(f'./{filename}', 'r') as file:
                    data=json.load(file)  
                return (f"{data}")    
        else:
                return "Invalid file type"

@app.route("/weight", methods=["GET", "POST"])
def post_weight():
    if request.method == 'POST':
        if request.form['action'] == 'submit':
            direction = request.form['direction']
            truck_license = request.form['truck_license']
            product_delivered = request.form['product_delivered']
            truck_bruto_weight = request.form['truck_bruto_weight']
            unit_of_measure_bruto = request.form['unit_of_measure_1']
            truck_neto_weight = request.form['truck_neto_weight']
            unit_of_measure_neto = request.form['unit_of_measure_2']
            container_id = request.form['container_id']
            force = request.form['force']
            timestamp = datetime.now().strftime(r"%Y%m%d%H%M%S")
            if truck_license is None or truck_license is "":
                return "Truck license plate is empty, please insert a truck license number"
            if product_delivered.isnumeric() or has_numbers(product_delivered):
                return "Invalid product! you cnnot have numbers in product's names"
            if re.search('[a-zA-Z]', truck_bruto_weight) or truck_bruto_weight is None or truck_bruto_weight is "":
                return "Invalid weight inserted to bruto weight"
            if re.search('[a-zA-Z]', truck_neto_weight) or truck_neto_weight is None or truck_neto_weight is "":
                return "Invalid weight inserted to neto weight"
            

    elif request.method == 'GET':
        return render_template('index.html')


@app.route("/health")
def healthcheck():
    if isconnected == 1:
        return "The Server Is Healthy", 200
    else:
        return "Could Not Connect To The Database", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
