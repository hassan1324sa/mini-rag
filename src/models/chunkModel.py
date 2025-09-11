from .baseDataModel import BaseDataModel
from .dbSchemes import Project
from .dbSchemes import DataChunk
from .enums.dataBaseEunm import DataBaseEnum
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):
    def __init__(self, dbClient:object):
        super().__init__(dbClient)
        self.collection = dbClient[DataBaseEnum.collectionChunkName.value]
    
    async def createChunk(self,chunk:DataChunk):
        result = await self.collection.insert_one(chunk.dict(by_alias=True,exclude_unset=True))
        chunk._id = result.inserted_id
        return chunk

    async def getChunk(self,chunkId:str):
        result = await self.collection.find_one({
            "_id": ObjectId(chunkId)
        })
        if result is None:
            return None
        return DataChunk(**result)
    
    async def insertManyChunks(self,chunks:list,batchSize:int=100):
        for i in range(0,len(chunks),batchSize):
            batch = chunks[i:i+batchSize]
            ops=[InsertOne(chunk.dict(by_alias=True,exclude_unset=True)) for chunk in batch]
            await self.collection.bulk_write(ops)

        return len(chunks)
    async def deleteChunksByProjectId(self,projectId:ObjectId):
        result = await self.collection.delete_many({
            "chunkProjectId":projectId
        })
        return result.deleted_count

    