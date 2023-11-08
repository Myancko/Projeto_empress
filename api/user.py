from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from sqlalchemy.orm import Session
from db_config.sqlalchemy_config import SessionFactory
from models.user import User_req
from repository.user import UserRepository
from models.sqlalchemy_models.alchemy_mod import User
from typing import List

import security


router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
        
    
@router.get("/signup/list")
async def list_accounts(sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_all_accounts()
    return result

@router.get("/signup/get/{id}")
async def get_account(id: int, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.get_account(id)
    return result

   
@router.post("/login/")
def login(matricula : str, password: str, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)

    owner_matricula = sess.query(User).filter(User.matricula == matricula)
    print(owner_matricula[0].password, '<<<<<<<<<<<<<<<<<<<<<<<<<')
    if owner_matricula:
        
        p = security.verify_password(password, owner_matricula[0].password)
        print(p, '>>>>>>>>>>>>>>>>>>>')
        
        if p == True:
            return JSONResponse(content={'message': 'td okay :3'}, status_code=200)
        
        else:
            return JSONResponse(content={'message': 'password or matricula is wrong'}, status_code=500)

    else:
        return JSONResponse(content={'message': 'password or matricula is wrong'}, status_code=500)



        
@router.post("/signup/add")
def create_account(req: User_req, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)

    signup = User(id_user=req.id_user,
                  name=req.name,
                  matricula=req.matricula,
                  email=req.email,
                  password = security.get_password_hash(req.password),
                  number=req.number,
                  role=req.role)
    
    
    result = repo.insert_user(signup)
    if result == True:
        return signup
    else:
        return JSONResponse(content={'message': 'create signup problem encountered, the email and the matrcula have to e different from an existing one'}, status_code=500)


@router.delete("/account/delete/{id}")
async def delete_account(id: int, sess: Session = Depends(sess_db)):
    repo: UserRepository = UserRepository(sess)
    result = repo.delete_user(id)
    if result:
        return JSONResponse(content={'message': 'login deleted successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'delete login error'}, status_code=500)
   
@router.patch("/account/update")
def update_account(id: int, req: User_req, sess: Session = Depends(sess_db)):
    
    request = req.dict(exclude_unset=True)
    print(request, '<<<<')
    request['password'] = security.get_password_hash(request['password'])
    repo: UserRepository = UserRepository(sess)
    result = repo.update_user(id, request)
    
    if result:
        return JSONResponse(content={'message': 'profile updated successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)