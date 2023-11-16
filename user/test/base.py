from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..repository.user import UserRepository
from db_config.sqlalchemy_config import SessionFactory
from models.sqlalchemy_models.alchemy_mod import User
from fastapi.testclient import TestClient
from main import app

class Test_base_user:

    def sess_db():
        db = SessionFactory()
        try:
            yield db
        finally:
            db.close()
    
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
         
        return 'ok'

    def teardown():
        
        client = TestClient(app)
        client.delete("/account/delete/6969")