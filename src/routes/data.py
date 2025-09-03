from fastapi import FastAPI,APIRouter,Depends,UploadFile,status
from fastapi.responses import JSONResponse
from helpers.config import getSettings,Settings
from controllers import DataController
from controllers import ProjectController
from controllers import ProcessController
import os
import aiofiles
from models import ResponseSignal
import logging
from .schemes.data import ProcessRequest


logger = logging.getLogger("uvicorn.error")

dataRouter = APIRouter(
    prefix="/api/v1/data", # i cant use the get or any function lower  before use that prefix in the url  
)

@dataRouter.post("/upload/{projectId}")
async def upload(projectId:str,file:UploadFile,appSettings:Settings=Depends(getSettings)):
    DataControllerObj= DataController()
    
    isvalid,signal=DataControllerObj.validateUploadedFiles(file=file)
    
    if not isvalid:
    
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":signal})  
    
    projectDirPath=ProjectController().getProjectPath(projectId)
    filePath,fileId=DataControllerObj.generateUniqueFilename(orgFileName=file.filename,projectId=projectId)
    
    try:
    
        async with aiofiles.open(filePath,"wb") as f:
    
            while chunk := await file.read(appSettings.FILE_DEFAULT_CHUNK_SIZE):
    
                await f.write(chunk)
    
    except Exception as e:
    
        logger.error(f"Error While uploading file : {e}")



        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.FileUploadedFailed.value})  

        return 

    return JSONResponse(content={"signal":signal,"fileId":fileId})  

@dataRouter.post("/process/{projectId}")
async def processEndpoint(projectId:str,processReq:ProcessRequest):

    fileId= processReq.fileId
    chunkSize=processReq.chunkSize
    overlap=processReq.overlap
    processControllerObj = ProcessController(projectId=projectId)

    fileContent = processControllerObj.getFileContent(fileId)
    fileChunks = processControllerObj.processFileContent(
        fileContent,fileId,chunkSize,overlap
    )
    if fileChunks is None or len(fileChunks) < 1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.PROCESSING_FAILED})
    
    return fileChunks[0].page_content