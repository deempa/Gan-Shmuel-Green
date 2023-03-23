import pytest
from app import app
import json

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client




def test_api_endpoint(client):
    response = client.get('/weight')
    assert response.status_code == 200
    
    response = client.get('/batch-weight')
    assert response.status_code == 200
    
    response = client.get('/unknown')
    assert response.status_code == 200
    


    response = client.get('/health')    
    assert response.status_code == 200



def test_post(client):
    data = {'direction': 'in', 'truck_license': 'lic10', 'product_delivered': 'apples', 
            'truck_bruto_weight': '12000', 'unit_of_measure_1': 'kg', 'force': 'True',
              'container_id': 'T-123'}
    response = client.post('/weight', data=data)
    assert response.status_code == 200
    assert response.content_type == 'application/json'
    json_data = response.get_json()
    assert 'bruto' in json_data
    assert 'id' in json_data
    assert 'truck' in json_data  
    