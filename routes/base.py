from fastapi import FastAPI,APIRouter
import os 



baseRouter = APIRouter(
    prefix="/api/v1", # i cant use the get or any function lower  before use that prefix in the url  
)

@baseRouter.get("/")
def welcome():
    Name=os.getenv("APP_NAME")
    return{
        "message":Name
    }
