from fastapi import FastAPI,APIRouter,status ,Request
from fastapi.responses import JSONResponse
from helpers.config import getSettings,Settings
import logging
from routes.schemes.nlp import PushReq,SearchReq
from models.projectModdel import ProjectModel
from models.chunkModel import ChunkModel 
from controllers.nlpController import NlpController
from models import ResponseSignal

logger=logging.getLogger("uvicorn.error")


nlpRouter = APIRouter(prefix="/api/v1/nlp")


@nlpRouter.post("/index/push/{projectId}")
async def indexProject(request:Request,projectId:str,pushReq:PushReq):
    
    projectModel = await ProjectModel.createInstance(dbClient=request.app.db_client)
    chunkModel = await ChunkModel.createInstance(dbClient=request.app.db_client)
    project =  await projectModel.getProjectOrCreateOne(projectId=projectId)
    if not project:
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.projectNotFound.value})
    
    nlpController = NlpController(vectorDBclient=request.app.vectorDBClient,
                                  generationClient=request.app.generationClient,
                                  embeddingClient=request.app.embeddingClient)
    hasRecords = True
    pageNo =1 
    idx=0
    insertedItemsCount=0
    while hasRecords:
        pageChunks =  await chunkModel.getProjectChunks(projectId=project.id,pageNo=pageNo,pageSize=50)
        if len(pageChunks):
            pageNo+=1
        if not pageChunks or len(pageChunks)==0:
            hasRecords=False
            break
        chunkIds = list(range(idx,idx+len(pageChunks)))
        idx+=len(pageChunks)

        isInserted = nlpController.indexIntoVectorDB(project=project,chunks=pageChunks,doReset=pushReq.doReset,chunksId=chunkIds)
        if  not  isInserted:
            return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.insertIntoVectorDBError.value})
        insertedItemsCount +=len(pageChunks)
    return JSONResponse(content={"signal":ResponseSignal.insertIntoVectorDBSuccess.value,"inserted Items Count":insertedItemsCount})

@nlpRouter.get("/index/info/{projectId}")
async def indexProject(request:Request,projectId:str):
    projectModel = await ProjectModel.createInstance(dbClient=request.app.db_client)
    project =  await projectModel.getProjectOrCreateOne(projectId=projectId)
    nlpController = NlpController(vectorDBclient=request.app.vectorDBClient,
                                  generationClient=request.app.generationClient,
                                  embeddingClient=request.app.embeddingClient)
    collectionInfo = nlpController.getVectorDBcollectionInfo(project=project)
    return JSONResponse(content={"signal":ResponseSignal.insertIntoVectorDBSuccess.value,
                        "collection Info":collectionInfo
                        })


@nlpRouter.post("/index/search/{projectId}")
async def indexProject(request:Request,projectId:str,searchReq:SearchReq):
    projectModel = await ProjectModel.createInstance(dbClient=request.app.db_client)
    project =  await projectModel.getProjectOrCreateOne(projectId=projectId)
    nlpController = NlpController(vectorDBclient=request.app.vectorDBClient,
                                  generationClient=request.app.generationClient,
                                  templateParser=request.app.templateParser,
                                  embeddingClient=request.app.embeddingClient,)
    result = nlpController.searchVectorDBcollection(project=project,text=searchReq.text,limit=searchReq.limit)
    if not result:
        JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.vectorDBSearchError.value,
                        "collection Info":result})
    return JSONResponse(content={"signal":ResponseSignal.vectorDBSearchSuccess.value,
                        "result":result
                        })



@nlpRouter.post("/index/answer/{projectId}")
async def answerRag(request:Request,projectId:str,searchReq:SearchReq):
    projectModel = await ProjectModel.createInstance(dbClient=request.app.db_client)
    project =  await projectModel.getProjectOrCreateOne(projectId=projectId)
    nlpController = NlpController(vectorDBclient=request.app.vectorDBClient,
                                  generationClient=request.app.generationClient,
                                  embeddingClient=request.app.embeddingClient,
                                  templateParser=request.app.templateParser
                                  )
    answer , fullPrompt , chatHistory = nlpController.answerRagQuery(project=project,query=searchReq.text,limit=searchReq.limit)
    if not answer:
        return   JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,content={"signal":ResponseSignal.errorWhileAnswering.value,})
    return JSONResponse(content={"signal":ResponseSignal.successAnswering.value,"answer":answer,"fullPrompt":fullPrompt,"chatHistory":chatHistory})



