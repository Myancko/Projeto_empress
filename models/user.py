from pydantic import BaseModel

class User_req (BaseModel):
    
    id_user : int 
    name : str
    matricula : int 
    email : str
    password : str
    number : str
    role : int