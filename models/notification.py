from pydantic import BaseModel

class Notification (BaseModel):
    
    id_notification : int 
    writer : int
    receiver : int 
    message : str
    about : int
    seen : bool