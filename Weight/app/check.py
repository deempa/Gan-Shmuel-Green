import os
import json
import csv

from app import app

current_dir = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(current_dir, '..', 'in')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def lbs_to_kgs(weight_lbs):

    weight_kgs = weight_lbs * 0.45359237
    return weight_kgs


def check_if_exists_in_file(container_id):

    for filename in os.listdir(app.config['UPLOAD_FOLDER']):
        if os.path.isfile(os.path.join(app.config['UPLOAD_FOLDER'], filename)):
            ext = filename.split(".")[-1]
            if ext == 'csv':

                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:

                    reader = csv.reader(file)
                    unit = ''
                    for row in reader:

                        if row[1] == 'kg':
                            unit = 'kg'
                        elif row[1] == 'lbs':
                            unit = 'lbs'
                        if row[0] == container_id:
                            weight = row[1]
                            if unit == 'kg':
                                return weight
                            elif unit == 'lbs':
                                weight = lbs_to_kgs(int(weight))
                                return weight
            if ext == 'json':


                with open(os.path.join(app.config['UPLOAD_FOLDER'], filename), 'r') as file:

                    data = json.load(file)
                    for line in data:
                        weight = line['weight']
                        unit = line['unit']

                        id = line['id']
                        if container_id == id:
                            if unit == 'lbs':
                                weight = lbs_to_kgs(weight)
                                return weight
                            else:
                                return weight
    return False


print(check_if_exists_in_file('C-65481'))

