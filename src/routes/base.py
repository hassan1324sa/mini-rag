from fastapi import FastAPI,APIRouter,Depends
from helpers.config import getSettings,Settings


baseRouter = APIRouter(
    prefix="/api/v1", # i cant use the get or any function lower  before use that prefix in the url  
)

@baseRouter.get("/")
async def welcome(appSettings:Settings=Depends(getSettings)):

    return{
        "name":appSettings.APP_NAME
    }
