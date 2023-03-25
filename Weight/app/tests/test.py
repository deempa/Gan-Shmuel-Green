import pytest

import json



import requests

ENDPOINT="http://3.76.109.165:8089"
# ENDPOINT="http://127.0.0.1:5000"

## HEALTH TEST
def test_health():
    request=requests.get(ENDPOINT + "/health")
    assert request.status_code == 200




def test_weight():
    response = requests.get(ENDPOINT +'/weight')
    assert response.status_code == 200
def test_batch_weight():    
    response = requests.get(ENDPOINT +'/batch-weight')
    assert response.status_code == 200
def test_unknown():    
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
def test_empty_contaier():
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': ''}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
    

def test_invalid_product():
     #invalid product 
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': '123', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
def test_invalid_weight():
#invalid weight
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': 'asd', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
def test_empty_weight():
    payload = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400
def test_out_before_in():
    payload = {'direction': 'out', 'truck_license': '131313131', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': '123123123'}
    response = requests.post(ENDPOINT +'/weight', data=payload)
    assert response.status_code == 400



def test_get_session():
    response = requests.get(ENDPOINT +'/session/1')
    assert response.status_code == 200 or response.status_code==404


def test_get_item():
    response= requests.get(ENDPOINT + '/item/1')
    assert response.status_code == 200 or response.status_code==404

def test_main():
    response= requests.get(ENDPOINT + '/')
    assert response.status_code == 200 or response.status_code==404
