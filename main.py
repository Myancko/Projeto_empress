from fastapi import FastAPI
from api import user, request

app = FastAPI ()
app.include_router(user.router)
app.include_router(request.router)