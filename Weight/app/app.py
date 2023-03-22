from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
import os, json
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename
import re
import connections
UPLOAD_FOLDER = '../in'

ALLOWED_EXTENSIONS = set(['csv','json'])

def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
#8083


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
    pass


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
        if request.form['action'] == 'submit':

            direction = request.form['direction']
            truck = request.form['truck_license'] 
            product_delivered = request.form['product_delivered']
            bruto = request.form['truck_bruto_weight']
            unit_of_measure_bruto = request.form['unit_of_measure_1']
            truck_tara = request.form['truck_neto_weight']
            unit_of_measure_neto = request.form['unit_of_measure_2']
            date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
            container_id=request.form['container_id']
            if truck is None or truck is "":
                return "Truck license plate is empty, please insert a truck license number"
            if product_delivered.isnumeric() or has_numbers(product_delivered):
                return "Invalid product! you cnnot have numbers in product's names"
            if re.search('[a-zA-Z]', bruto) or bruto is None or bruto is "":
                return "Invalid weight inserted to bruto weight"
            if re.search('[a-zA-Z]', bruto) or bruto is None or bruto is "":
                return "Invalid weight inserted to neto weight"
            if direction == "In":
                pass
            
            connections.register_truck(container_id=container_id,wieght=bruto,unit=unit_of_measure_bruto)
                
            return redirect(url_for("post_weight"))
            
                

    elif request.method == 'GET':
        return render_template('index.html')


@app.route("/health")
def healthcheck():
    try:
        db.is_connected
        return "The Server Is Healthy", 200
    except Exception:
        return "Could Not Connect To The Database", 500


if __name__ == "__main__":
    app.run(host="0.0.0.0")
