import pytest

import json



import requests

# ENDPOINT="https://3.76.109.165:8089"
ENDPOINT="http://127.0.0.1:5000"

## HEALTH TEST
def test_health():
    request=requests.get(ENDPOINT + "/health")
    assert request.status_code == 200




def test_api_endpoint():
    response = requests.get(ENDPOINT +'/weight')
    assert response.status_code == 200
    
    response = requests.get(ENDPOINT +'/batch-weight')
    assert response.status_code == 200
    
    response = requests.get(ENDPOINT +'/unknown')
    assert response.status_code == 200
    



def test_post():
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'
    json_data = response.json()

    assert 'bruto' in json_data
    assert 'id' in json_data
    assert 'truck' in json_data  
    
def test_post_bad_request():
   
#truck license is empty 
    payload = {'direction': 'in', 'truck_license': '', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
#Container id is required
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': ''}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
    
     #invalid product 
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': '123', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400

#invalid weight
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': 'asd', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
#empty weight
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400

    # payload = {'direction': 'out', 'truck_license': '131313131', 'product_delivered': 'apples', 
    #         'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
    #           'container_id': '123123123'}
    # response = requests.post(ENDPOINT +'/weight', data=payload)
    # assert response.status_code == 400



def get_session():
    response = requests.get(ENDPOINT +'/session/1')
    assert response.status_code == 200 or response.status_code==400


def get_item():
    response= requests.get(ENDPOINT + '/item/1')
    assert response.status_code == 200 or response.status_code==400
