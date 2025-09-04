from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    _id:Optional[ObjectId]
    chunkText:str=Field(...,min_length=1)
    chunkMetaData:dict
    chunkOrder:int = Field(...,gt=0)
    chunkProjectId:ObjectId


    class Config:
        arbitrary_types_allowed=True
