from fastapi import FastAPI,APIRouter,Depends,UploadFile
from helpers.config import getSettings,Settings
from controllers import DataController


dataRouter = APIRouter(
    prefix="/api/v1/data", # i cant use the get or any function lower  before use that prefix in the url  
)

@dataRouter.post("/upload/{projectId}")
async def upload(projectId:str,file:UploadFile,appSettings:Settings=Depends(getSettings)):
    isvalid=DataController().validateUploadedFiles(file=file)
    
    return isvalid