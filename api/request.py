from fastapi import APIRouter, Depends, UploadFile, File, Form
from fastapi.responses import JSONResponse

import datetime
from sqlalchemy.orm import Session
from db_config.sqlalchemy_config import SessionFactory
from models.request import Request_req
from repository.request import RequestRepository
from models.sqlalchemy_models.alchemy_mod import Request, User
from typing import Annotated
import os


router = APIRouter()


def sess_db():
    db = SessionFactory()
    try:
        yield db
    finally:
        db.close()
        
@router.get("/request/list")
async def list_requests(sess: Session = Depends(sess_db)):
    repo: RequestRepository = RequestRepository(sess)
    result = repo.get_all_request()
    return result

@router.get("/request/get/{id}")
async def get_request(id: int, sess: Session = Depends(sess_db)):
    repo: RequestRepository = RequestRepository(sess)
    result = repo.get_request(id)
    return result
      
@router.post("/request/add")
async def add_request(req: Request_req = Depends(),
                      file: UploadFile = File(...),
                      sess: Session = Depends(sess_db)):
    
    file_ext = file.filename.split('.').pop()
    f_name =  file.filename
    
    owner_matricula = sess.query(User).filter(User.id_user == req.owner)
    print(owner_matricula[0].matricula, '<<<<<<<<<<<<<')
    
    f_path = f"requests/{owner_matricula[0].matricula}/{req.id_request}/{f_name}"
    dir_path = os.path.dirname(f_path)
    
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    with open(f_path, 'wb') as f:
        content = await file.read()
        f.write(content)
    print('ok <<<<<<')

    repo: RequestRepository = RequestRepository(sess)

    request = Request(id_request=req.id_request,
                  owner=req.owner,
                  data=f_path,
                  color=req.color,
                  two_sided = req.two_sided,
                  quantity=req.quantity,
                  date=datetime.date.today())
    
    result = repo.insert_request(request)
    

    if result == True:
        return request
    else:
        return JSONResponse(content={'message': 'create request problem encountered'}, status_code=500)
    
@router.delete("/request/delete/{id}")
async def delete_request(id: int, sess: Session = Depends(sess_db)):
    repo: RequestRepository = RequestRepository(sess)
    result = repo.delete_request(id)
    if result:
        return JSONResponse(content={'message': 'login deleted successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'delete login error'}, status_code=500)
    
@router.patch("/request/update")
def update_request(id: int, req: Request_req, sess: Session = Depends(sess_db)):
    
    request = req.dict(exclude_unset=True)
    repo: RequestRepository = RequestRepository(sess)
    result = repo.update_request(id, request)
    
    if result:
        return JSONResponse(content={'message': 'profile updated successfully'}, status_code=201)
    else:
        return JSONResponse(content={'message': 'update profile error'}, status_code=500)
    