from flask import Flask, request, make_response, render_template, redirect, url_for
import csv
from io import StringIO
import os
from datetime import datetime,date

isconnected = 0

app = Flask(__name__)

@app.route('/')
def root():
    pass

@app.route("/weight", methods=["GET","POST"])
def post_weight():
    if request.method == 'POST':
        direction = request.form['direction']
        truck_license = request.form['truck_license']
        product_delivered = request.form['product_delivered']
        truck_bruto_weight = request.form['truck_bruto_weight']
        unit_of_measure_bruto = request.form['unit_of_measure_1']
        truck_neto_weight = request.form['truck_neto_weight']
        unit_of_measure_neto = request.form['unit_of_measure_2']
        timestamp = datetime.now().strftime(r"%Y%m%d%H%M%S")
    #     file = request.files['csv_file']
    #     if 'csv_file' not in request.files:
    #         return 'No file uploaded', 400
    #     file = request.files['csv_file']
    #     if file.filename == '':
    #         return 'No file selected', 400

    # # Save the file to the local folder
    #     folder_path = '/csv_files'
    #     if not os.path.exists(folder_path):
    #         os.makedirs(folder_path)
    #     file_path = os.path.join(folder_path, file.filename)
    #     file.save(file_path)
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