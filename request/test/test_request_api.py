from fastapi import FastAPI
from fastapi.testclient import TestClient
from request.api import request
from .base import Test_base_request
import random
import json

app = FastAPI()

app.include_router(request.router)


client = TestClient(app)

def test_get_requests():
    """ Testa o list de requests """
    
    response = client.get("http://127.0.0.1:8000/request/list")
    assert response.status_code == 200
    
def test_get_request():
    """ Testa o get de requests """
    
    Test_base_request.setup()
    
    response = client.get("http://127.0.0.1:8000/request/get/6969")
    
    assert response.status_code == 200 
    assert response.json()['id_request'] == 6969 
    
    Test_base_request.teardown()
    
def test_post_request():
    """ Testa o post de request """
        
    Test_base_request.setup()
    id = random.randint(2000000, 9000000)
    data = {
    'id_request': id,
    'owner': 6969,
    'color': True,
    'data': ':dasd',
    'two_sided': True,
    'quantity': 10,
    'status' : 'going',
    'date': '2023-11-03'
}

    
    files = {
    'file': open('request/test/test_file/test.rtf', 'rb')
    }
     
    response = client.post("http://127.0.0.1:8000/request/add", params=data, files=files)
   
    assert response.status_code == 200
    response = client.get(f"http://127.0.0.1:8000/request/get/{id}")
    assert response.json()['id_request'] == id
    
    client.delete(f"/request/delete/{id}")
    
    Test_base_request.teardown()
    
def test_delete_request():
    """ Testa o delete de request """
    
    Test_base_request.setup()
    
    response = client.get("http://127.0.0.1:8000/request/get/6969")
    
    assert response.status_code == 200 
    assert response.json()['id_request'] == 6969 
    
    Test_base_request.teardown()
    
def test_update_request():
    
    Test_base_request.setup()
    
    id = random.randint(2000000, 9000000)
    data = {
    'id_request': id,
    'owner': 6969,
    'color': True,
    'data': ':dasd',
    'two_sided': True,
    'quantity': 10,
    'status' : 'going',
    'date': '2023-11-03'
}
    
    files = {
    'file': open('request/test/test_file/test.rtf', 'rb')
    }
    
    
    response = client.post("http://127.0.0.1:8000/request/add", params=data, files=files)
   
    assert response.status_code == 200
    response = client.get(f"http://127.0.0.1:8000/request/get/{id}")
    assert response.json()['id_request'] == id
    assert response.json()['status'] == 'going'
    print(response.json()['data'], '<<<<<<<<<')
    
    patch = {
    'id_request': id,
    'owner': 6969,
    'color': True,
    'data': response.json()['data'],
    'two_sided': True,
    'quantity': 10,
    'status' : 'gone',
    'date': '2023-11-04'
}

    response = client.patch(f"http://127.0.0.1:8000/request/update/{id}", json=patch)
    print(response.json(), ' <<<<<<<<<<<')
    print(response.text , '<<<<<<<<<<<<')
    
    assert response.status_code == 201
    response = client.get(f"http://127.0.0.1:8000/request/get/{id}")
    assert response.json()['date'] == "2023-11-04"
    assert response.json()['status'] == 'gone'
    
    client.delete(f"/request/delete/{id}")
    
    Test_base_request.teardown()