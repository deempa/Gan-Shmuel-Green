import pytest

import json



import requests


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
    data = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = requests.post(ENDPOINT +'/weight', data=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    json_data = response.get_json()
    assert 'bruto' in json_data
    assert 'id' in json_data
    assert 'truck' in json_data  
    