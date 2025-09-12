from pydantic import BaseModel,Field,field_validator
from typing import Optional
from bson.objectid import ObjectId
from datetime import datetime

class Asset(BaseModel):
    id:Optional[ObjectId] = Field(None,alias="_id")
    assetProjectId:ObjectId
    assetType:str=Field(...,min_length=1)
    assetName:str=Field(...,min_length=1)
    assetSize:int=Field(ge=0,default=None)
    assetConfig:dict=Field(default=None)
    assetPushedAt:datetime= Field(default=datetime.utcnow())

    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name = True

    @classmethod
    def getIndexes(cls):
        return [
            {
                "key":[("assetProjectId",1)],
                "name":"assetProjectIdIndex1",
                "unique":False,
            },
            {
                "key":[("assetProjectId",1),
                       ("assetName",1)],
                "name":"assetProjectIdNameIndex1",
                "unique":True,
            },
        ]

