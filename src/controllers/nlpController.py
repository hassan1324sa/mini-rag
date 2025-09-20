from .baseController import BaseController
from models.dbSchemes import Project,DataChunk
from stores.llm.llmEnum import DocumentTypeEnum
from typing import List
import json

class NlpController(BaseController):
    def __init__(self,vectorDBclient,generationClient,embeddingClient,templateParser):
        super().__init__()
        self.vectorDBclient=vectorDBclient
        self.generationClient=generationClient
        self.embeddingClient=embeddingClient
        self.templateParser=templateParser
    
    def createCollectionName(self,projectId):
        return f"collection_{projectId}".strip()
    
    def resetVectorDBCollection(self,project:Project):
        collectionName =self. createCollectionName(projectId=project.projectId)
        return self.vectorDBclient.deleteCollection(collectionName=collectionName)

    def getVectorDBcollectionInfo(self,project:Project):
        collectionName = self.createCollectionName(projectId=project.projectId)
        info = self.vectorDBclient.getCollectionInfo(collectionName=collectionName)
        return json.loads(
                        json.dumps(info,default= lambda  x:  x.__dict__)
                        )
    
    def indexIntoVectorDB(self,project:Project,chunks:list[DataChunk],doReset:bool=False,chunksId:list[int]=[]):
        collectionName =self. createCollectionName(projectId=project.projectId)
        texts = [i.chunkText for i in chunks]
        metadata = [i.chunkMetaData for i in chunks]
        vector = [self.embeddingClient.EmbedText(text=i,documentType=DocumentTypeEnum.DOCUMENt.value) for i in texts]
        _=self.vectorDBclient.createCollection(collectionName,embeddingSize=self.embeddingClient.embeddingSize,doReset=doReset)
        _ =self.vectorDBclient.insertMany(collectionName,texts,vector,metadata,recordIds=chunksId)
        return True
    
    def searchVectorDBcollection(self,project,text,limit=10):
        collectionName =self. createCollectionName(projectId=project.projectId)
        vector = self.embeddingClient.EmbedText(text=text,documentType=DocumentTypeEnum.QUERY.value)
        if not vector or len(vector)<1:
            return False
        result = self.vectorDBclient.searchByVector(collectionName,vector,limit)
        if not result:
            return False
        return json.loads(
                        json.dumps(result,default= lambda  x:  x.__dict__)
                        )
    
    def answerRagQuery(self,project,query,limit):
        answer,fullPrompt,chatHistory=None,None,None
        ragResults = self.searchVectorDBcollection(project=project,text=query,limit=limit)
        if not  ragResults or len(ragResults)<1:
            return answer,fullPrompt,chatHistory
        systemPrompt=self.templateParser.get("rag","system_prompt")
        
        docPrompt="\n".join([self.templateParser.get("rag","document_prompt",{"doc_num":idx+1,"chunk_text":doc["text"]})
                           for idx,doc in enumerate(ragResults)])
        footerPrompt = self.templateParser.get("rag","footer_prompt",{"query":query})
        chatHistory = [self.generationClient.constructPrompt(prompt=systemPrompt,role=self.generationClient.enums.SYSTEM.value)]
        fullPrompt = "\n\n".join([docPrompt,footerPrompt])
        answer = self.generationClient.generateText(
            prompt= fullPrompt,
            chatHistory=chatHistory
        )
        return answer,fullPrompt,chatHistory
