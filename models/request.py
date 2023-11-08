from datetime import date
from pydantic import BaseModel, FilePath
from fastapi import  File, UploadFile
from typing import Optional

class Request_req (BaseModel):
    
    id_request : int 
    owner : int
    data : Optional[str]
    color : bool
    two_sided : bool
    quantity : int
    status : str
    date : Optional[date]