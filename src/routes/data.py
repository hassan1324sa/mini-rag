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
from models.dbSchemes import DataChunk,Asset
from models.assetModel import AssetModel
from models.chunkModel import ChunkModel
from models.enums.assetTypeEnum import AssetTypeEnum


logger = logging.getLogger("uvicorn.error")

dataRouter = APIRouter(
    prefix="/api/v1/data", # i cant use the get or any function lower  before use that prefix in the url  
)

@dataRouter.post("/upload/{projectId}")
async def upload(request:Request,projectId:str,file:UploadFile,appSettings:Settings=Depends(getSettings)):

    dbClient =request.app.db_client
    projectModel = await ProjectModel.createInstance(dbClient=dbClient)


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


        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.FileUploadedFailed.value})  
    assetModel = await AssetModel.createInstance(dbClient=dbClient)
    assetResource = Asset(assetProjectId=project.id,assetType=AssetTypeEnum.FILE.value,assetName=fileId,assetSize=os.path.getsize(filePath))
    assetRecord = await assetModel.createAsset(asset=assetResource)
    fileId =str(assetRecord.id)+str(os.path.splitext(file.filename)[1])

    return JSONResponse(content={"signal":signal,"fileId":fileId}) 


@dataRouter.post("/process/{projectId}")
async def processEndpoint(request:Request,projectId:str,processReq:ProcessRequest):

    fileId= processReq.fileId
    chunkSize=processReq.chunkSize
    overlap=processReq.overlap
    dbClient = request.app.db_client
    doReset = processReq.doReset


    projectModel =await ProjectModel.createInstance(dbClient=dbClient)
    chunkModel = await ChunkModel.createInstance(dbClient=dbClient)
    assetModel = await AssetModel.createInstance(dbClient=dbClient)
    project = await projectModel.getProjectOrCreateOne(projectId=projectId)

    projectFilesIds = {}

    if processReq.fileId :
        assetRecord = await assetModel.getAssetRecord(assetProjectId=project.id,assetName=processReq.fileId)
        
        if assetRecord is  None:
            return JSONResponse(content={
            "signal":ResponseSignal.fileIdError.value
        },status_code=status.HTTP_404_NOT_FOUND)
    
        projectFilesIds = {assetRecord.id:assetRecord.assetName}

    else:
        


        projectFiles = await assetModel.getAllProjectAssets(assetProjectId=project.id,assetType=AssetTypeEnum.FILE.value)
        

        projectFilesIds = {i.id: i.assetName 
                            for i in projectFiles}

    if len(projectFilesIds)==0:
        return JSONResponse(content={
            "signal":ResponseSignal.noFilesError.value
        },status_code=status.HTTP_404_NOT_FOUND)
    


    processControllerObj = ProcessController(projectId=projectId)
    noRecorders = 0
    noFiles = 0

    if doReset==1:
        await chunkModel.deleteChunksByProjectId(projectId=project.id)


    for assetId,fileId in projectFilesIds.items():
        fileContent = processControllerObj.getFileContent(fileId)
        if fileContent is None :
            logger.error(f"error while processing file :{fileId}")
            continue
        fileChunks = processControllerObj.processFileContent(
            fileContent,fileId,chunkSize,overlap
        )
        if fileChunks is None or len(fileChunks) < 1:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.processingFailed.value})
        
        fileChunksRecords = [
            DataChunk(chunkText=chunk.page_content,chunkMetaData=chunk.metadata,chunkOrder=i+1,chunkProjectId=project.id,chunkAssetId=assetId) 
            for i,chunk in enumerate(fileChunks)
            ]

        noRecorders += await chunkModel.insertManyChunks(chunks=fileChunksRecords)
        noFiles += 1

    return JSONResponse(content={"signal":ResponseSignal.processingSuccess.value,"inserted chunks":noRecorders,"number of Files":noFiles})