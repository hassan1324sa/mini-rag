from pydantic import BaseModel,Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id:Optional[ObjectId] = Field(None,alias="_id")
    chunkText:str=Field(...,min_length=1)
    chunkMetaData:dict
    chunkOrder:int = Field(...,gt=0)
    chunkProjectId:ObjectId
    chunkAssetId:ObjectId


    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name = True
    @classmethod
    def getIndexes(cls):
        return [
            {
                "key":[("chunkProjectId",1)],
                "name":"chunkProjectIdIndex1",
                "unique":False,
            }
<<<<<<< HEAD
        ]
=======
        ]

class RetrieveDocs(BaseModel):
    text:str
    score:float
>>>>>>> 03fc06c (Initial commit)
