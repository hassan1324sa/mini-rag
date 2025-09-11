from fastapi import FastAPI,APIRouter,Depends,UploadFile,status ,Request
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
from models.projectModdel import ProjectModel
from models.dbSchemes import DataChunk
from models.chunkModel import ChunkModel


logger = logging.getLogger("uvicorn.error")

dataRouter = APIRouter(
    prefix="/api/v1/data", # i cant use the get or any function lower  before use that prefix in the url  
)

@dataRouter.post("/upload/{projectId}")
async def upload(request:Request,projectId:str,file:UploadFile,appSettings:Settings=Depends(getSettings)):

    dbClient =request.app.db_client
    projectModel = ProjectModel(dbClient=dbClient)


    project = await projectModel.getProjectOrCreateOne(projectId=projectId)


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

    return JSONResponse(content={"signal":signal,"fileId":fileId,}) 


@dataRouter.post("/process/{projectId}")
async def processEndpoint(request:Request,projectId:str,processReq:ProcessRequest):

    fileId= processReq.fileId
    chunkSize=processReq.chunkSize
    overlap=processReq.overlap
    processControllerObj = ProcessController(projectId=projectId)
    doReset = processReq.doReset

    dbClient = request.app.db_client
    projectModel = ProjectModel(dbClient=dbClient)
    project = await projectModel.getProjectOrCreateOne(projectId=projectId)



    fileContent = processControllerObj.getFileContent(fileId)
    fileChunks = processControllerObj.processFileContent(
        fileContent,fileId,chunkSize,overlap
    )
    if fileChunks is None or len(fileChunks) < 1:
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.PROCESSING_FAILED})
    
    fileChunksRecords = [DataChunk(chunkText=chunk.page_content,chunkMetaData=chunk.metadata,chunkOrder=i+1,chunkProjectId=project.id) for i,chunk in enumerate(fileChunks)]
    chunkModel = ChunkModel(dbClient=dbClient)
    if doReset==1:
        await chunkModel.deleteChunksByProjectId(projectId=project.id)
    noRecorders = await chunkModel.insertManyChunks(chunks=fileChunksRecords)

    return JSONResponse(content={"signal":ResponseSignal.PROCESSING_SUCCESS.value,"inserted chunks":noRecorders})