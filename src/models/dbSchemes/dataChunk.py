from pydantic import BaseModel,Field
from typing import Optional
from bson.objectid import ObjectId

class DataChunk(BaseModel):
    id:Optional[ObjectId] = Field(None,alias="_id")
    chunkText:str=Field(...,min_length=1)
    chunkMetaData:dict
    chunkOrder:int = Field(...,gt=0)
    chunkProjectId:ObjectId


    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name = True
