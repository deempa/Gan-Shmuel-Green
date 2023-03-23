import pytest
from app import app

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
