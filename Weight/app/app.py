from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
import os
from datetime import datetime, date
import mysql.connector
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = './'

ALLOWED_EXTENSIONS = set(['csv'])


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
    pass


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
            timestamp = datetime.now().strftime(r"%Y%m%d%H%M%S")
            return (f"{direction},{truck_license},{product_delivered},{truck_bruto_weight},{unit_of_measure_bruto},{truck_neto_weight},{unit_of_measure_neto},{timestamp}")
        
        elif request.form['action'] == 'upload':
            if 'file' not in request.files:
                return "no file part"
            file = request.files['file']
            if file.filename == '':
                return "No selected file"

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                with open(f'./{filename}', 'r') as file:
                    reader = csv.reader(file)
                    for row in reader:
                        rows = print(row)

            return redirect(url_for('post_weight'))
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
