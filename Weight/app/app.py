from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
import os, json
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename
import re
import connections
# from check import check_if_exists_in_file # <------- call this fuction to check if the container exist in the files
                                          #   pass container_id as argument, returns None if does not exist,
                                          # if exists, returns weight in kgs   

current_dir = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.join(current_dir, '..', 'in')



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
            
        

            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return "File uploaded"

            
        else:
                return "Invalid file type"

@app.route("/weight", methods=["GET", "POST"])
def post_weight():
    if request.method == 'POST':
        if request.form['action'] == 'submit':

            direction = request.form['direction']
            truck = request.form['truck_license'] 
            produce = request.form['product_delivered']
            truck_bruto = request.form['truck_bruto_weight']
            unit_of_measure_bruto = request.form['unit_of_measure_1']
            truck_neto = request.form['truck_neto_weight']
            unit_of_measure_neto = request.form['unit_of_measure_2']
            date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
            containers=request.form['container_id'].split(',')
            force=request.form['force']
            # if truck is None or truck is "":
            #     return "Truck license plate is empty, please insert a truck license number"
            # if product_delivered.isnumeric() or has_numbers(product_delivered):
            #     return "Invalid product! you cnnot have numbers in product's names"
            # if re.search('[a-zA-Z]', truck_bruto) or truck_bruto is None or truck_bruto is "":
            #     return "Invalid weight inserted to bruto weight"
            # if re.search('[a-zA-Z]', truck_bruto) or truck_bruto is None or truck_bruto is "":
            #     return "Invalid weight inserted to neto weight"
            # if direction == "In":
            #     pass
            
            
            connections.insert_transaction(direction=direction,truck=truck,containers=containers,
                                           truck_bruto=truck_bruto,
                                           unit_of_measure_bruto=unit_of_measure_bruto,
                                           produce=produce,datetime=date_time,
                                           force=force)

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

@app.route("/unknown")
def show_unknown():
   conts= connections.unknown()
   return conts


if __name__ == "__main__":
    app.run(host="0.0.0.0")
