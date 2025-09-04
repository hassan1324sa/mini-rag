from pydantic import BaseModel,Field,validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    _id:Optional[ObjectId]
    projectId:str=Field(...,min_length=1)
    @validator(projectId)
    def validateProjectId(cls,value):
        if not value.isalnum():
            raise ValueError("project id must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed=True
