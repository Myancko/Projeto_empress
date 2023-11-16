from fastapi import FastAPI
from fastapi.testclient import TestClient
from user.api import user
from .base import Test_base_user
import random

app = FastAPI()

app.include_router(user.router)


client = TestClient(app)

def test_get_users():
    
    """ Testa o list de users """
    
    response = client.get("http://127.0.0.1:8000/account/list")
    assert response.status_code == 200
    
def test_get_user():
    
    """ Testa o get de users """
    
    Test_base_user.setup()
    
    response = client.get("/account/get/6969")
    assert response.status_code == 200
    assert response.json()['matricula'] == 11111123
    assert response.json()['password'] != "test_user"
    
    Test_base_user.teardown()
    
def test_add_user():
    
    """ testa o post de users """
    
    id = random.randint(2000000, 9000000)
    matricula = random.randint(2000000, 9000000)
    
    post = {
        "id_user": id,
        "name": "test_user",
        "matricula": matricula,
        "email": "test_user@gmail.com",
        "password": "test_user",
        "number": "test_user",
        "role": -1
    }
    
    post_test = client.post("/account/add", json=post)
    response = client.get(f"/account/get/{id}")
    
    assert post_test.status_code == 200
    assert response.json()['id_user'] == id
    assert response.json()['matricula'] == matricula
    assert response.json()['password'] != "test_user"
    
    client.delete(f"/account/delete/{id}")
    response = client.get(f"/account/get/{id}")
    assert response.json() == None
    
def test_user_delete():
    
    """ testa o delete de users """
    
    Test_base_user.setup()
    response = client.delete("/account/delete/6969")
    assert response.status_code == 200
    
def test_patch_user():
    
    Test_base_user.setup()
    
    patch = {
        "id_user": 6969,
        "name": "test_user",
        "matricula": 11111123,
        "email": "patches@gmail.com",
        "password": "test_user",
        "number": "test_user",
        "role": -1
    }
    
    response = client.patch(f"/account/update/6969", json=patch)
    assert response.status_code == 201
    response = client.get(f"/account/get/6969")
    assert response.json()['email'] == "patches@gmail.com"
    
    Test_base_user.teardown()