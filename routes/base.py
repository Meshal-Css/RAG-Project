from fastapi import APIRouter

base_Router = APIRouter()

@base_Router.get("/")
def welcome():
    return {
        "message": "HI"
    }