from typing import Dict, Any
from sqlalchemy.orm import Session
from models.sqlalchemy_models.alchemy_mod import Request
from sqlalchemy import desc

class RequestRepository:

    def __init__(self, sess: Session):
        self.sess: Session = sess

    def insert_request(self, request: Request) -> bool:
        try:
            self.sess.add(request)
            print('add')
            self.sess.commit()
            print('commit')
            print(request.id_request)
            
        except:
            return False
        
        return True

    def update_request(self, id: int, details: Dict[str, Any]) -> bool:
        try:
            self.sess.query(Request).filter(Request.id_request == id).update(details)
            self.sess.commit()

        except:
            return False
        return True

    def delete_request(self, id: int) -> bool:
        try:
            request = self.sess.query(Request).filter(Request.id_request == id).delete()
            self.sess.commit()

        except:
            return False
        return True
    
    def get_request(self, id:int): 
        return self.sess.query(Request).filter(Request.id_request == id).one_or_none()

    def get_all_request(self):
        return self.sess.query(Request).all()