from fastapi import FastAPI, APIRouter
from request.api import request
from user.api import user

app = FastAPI ()

app.include_router(user.router)
app.include_router(request.router)