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
            return ('You must enter truck weight',403)
        if truck == '':
            return ('You must enter truck license',400)
        if direction == "in":
            return connections.handle_in(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        if direction == "out":
            return connections.handle_out(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        if direction == "none":
            return connections.handle_none(direction,truck,produce,truck_bruto,unit_of_measure_bruto,force,containers)
        return "hello"

    elif request.method == 'GET':
        db=connections.get_connection()
        cursor = db.cursor()
        t1_str = request.args.get('from', default=datetime.now().strftime('%Y%m%d') + '000000', type=str)
        t2_str = request.args.get('to', default=datetime.now().strftime('%Y%m%d%H%M%S'), type=str)
        direction_filter = request.args.get('filter', default='in,out,none', type=str)
        directions = direction_filter.split(',')
        t1_obj = datetime.strptime(t1_str, '%Y%m%d%H%M%S')
        t2_obj = datetime.strptime(t2_str, '%Y%m%d%H%M%S')
        t1 = datetime.strftime(t1_obj, '%Y-%m-%d %H:%M:%S')
        t2 = datetime.strftime(t2_obj, '%Y-%m-%d %H:%M:%S')

        
        query = "SELECT * FROM transactions  WHERE datetime>= %s AND datetime<= %s AND direction IN ({})".format(','.join(['%s'] * len(directions)))
        params = [t1, t2]
        params.extend(directions)
        print(f"{t1} , {t2} , {directions}")
        cursor.execute(query, tuple(params))


        results = cursor.fetchall()
        weights = []
        for row in results:
            id=row[0]
            direction=row[2]
            bruto=row[4]
            neto=row[6]
            produce=row[7]
            container_query = f"SELECT container_id FROM container_in_transaction  WHERE transaction_id_in ='{id}' OR transaction_id_out ='{id}' "
            cursor.execute(container_query)
            containers = [c[0] for c in cursor.fetchall()]
            weights.append({
                'id': id,
                'direction': direction,
                'bruto': bruto,
                'neto' : neto if neto is not None else 'na',
                'produce':produce,
                'containers': containers

            })
        return jsonify(weights)
        
        
        
        
        # return render_template('index.html')

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


# @app.route('/item/<id>')
# def get_item(id):
#     db=connections.get_connection()
#     cursor=db.cursor()
#     t1=request.args.get('from', default='1'+'0' *12 ,type=str)
#     t2=request.args.get('to', default='',type=str)
    
#     if t2:
#         query=f"SELECT * FROM  transactions WHERE id='{id}' AND datetime>='{t1}' AND datetime<='{t2}'"
#     else:
#         query = f"SELECT * FROM transactions where id='{id}' AND datetime>='{t1}'"

#     cursor.execute(query)
#     sessions = [row[0] for row in cursor.fetchall()]
#     cursor.close()


#     if sessions
   




if __name__ == "__main__":
    app.run(host="0.0.0.0")