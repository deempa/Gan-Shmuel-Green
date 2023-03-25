from flask import Flask, request, make_response, render_template, redirect, url_for, jsonify
import csv
import os, json
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename
import re
import connections
import requests

current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, '..', 'in')

ALLOWED_EXTENSIONS = set(['csv','json'])
#test comment1
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)
#8083


#test comment1
#test comment 2



app = Flask(__name__)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# @app.route('/')
# def root():
#     return redirect(url_for('new_transaction'))


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
        direction = request.form['direction']
        truck = request.form['truck_license']
        produce = request.form['product_delivered']
        truck_bruto = request.form['truck_bruto_weight']
        unit_of_measure_bruto = request.form['unit_of_measure_1']
        # date_time = datetime.now().strftime(r"%Y%m%d%H%M%S")
        force =  request.form['force']
        containers=request.form['container_id']
        if truck is None or truck == '' and direction != 'none':
            return ('Standalone containers must be inserted with Direction as none',400)
        if containers == '':
            return ('Container id is required',401)
        if produce == '':
            produce = 'na'
        if has_numbers(produce):
            return ("Invalid product! you cnnot have numbers in product's names",402)
        if re.search(r'\D', truck_bruto):
            return ("Invalid weight inserted to bruto weight",403)
        if truck_bruto == '':

            return 'You must enter truck weight'

        if direction == "in":
            return connections.handle_in(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        if direction == "out":
            return connections.handle_out(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        elif direction == "none":
            return connections.handle_none(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        
        return "hello"

    elif request.method == 'GET':

        now = datetime.now()
        from_date = request.args.get('from') 
        if from_date is None:
            from_date = datetime.combine(now.date(), datetime.min.time()).strftime('%Y%m%d%H%M%S')
        to_date = request.args.get('to') 
        if to_date is None:
            to_date = now.strftime('%Y%m%d%H%M%S')
        filter_str = request.args.get('filter') 
        if filter_str is None:
            filter_str = "in,out,none"
        print(from_date,to_date,filter_str)
        return connections.handle_get_data_between_dates(from_date, to_date, filter_str)

@app.route("/new-transaction")
def new_transaction():
    if request.method == 'GET':

        return render_template('index.html')

@app.route("/unknown")
def show_unknown():
   conts= connections.unknown()
   return conts

@app.route("/health")
def healthcheck():
    try:
        db=connections.get_connection()
        cursor = db.cursor()
        cursor.execute("SELECT 1")
        cursor.fetchall()
        cursor.close()
        db.close()
        return ("Connection established",200)
    except:
        return ("Connection failed",503)


@app.route("/session/<id>")
def sessiondata(id):
    output = connections.get_session_data(id)
    if output == '404':
        return "", 404
    return output

@app.route("/item/<id>")
def get_items(id):
    now = datetime.now()
    from_date = request.args.get('from') 
    if from_date is None:
        from_date = datetime.combine(now.date(), datetime.min.time()).strftime('%Y%m%d%H%M%S')
    to_date = request.args.get('to') 
    if to_date is None:
        to_date = now.strftime('%Y%m%d%H%M%S')
    output = connections.handle_get_item(id, from_date, to_date)
    if output == '404':
        return "", 404
    return output



if __name__ == "__main__":
    app.run(host="0.0.0.0")