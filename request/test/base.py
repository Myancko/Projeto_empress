from fastapi.testclient import TestClient
from main import app

class Test_base_request:

    
    def setup():
        
        client = TestClient(app)
       
        signup = {
        "id_user": 6969,
        "name": "test_user",
        "matricula": 11111123,
        "email": "test_user@gmail.com",
        "password": "test_user",
        "number": "test_user",
        "role": -1
    }
        
        client.post("/account/add", json=signup)
        
        data = {
        'id_request': 6969,
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
        
        return 'ok'

    def teardown():
        
        client = TestClient(app)
        client.delete("/account/delete/6969")
        client.delete("/request/delete/6969")