from fastapi import FastAPI
from routes.base import base_router 
from routes  import data

app = FastAPI()

app.include_router(base_router) 
app.include_router(data.data_router) 