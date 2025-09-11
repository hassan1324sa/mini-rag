from pydantic import BaseModel,Field,field_validator
from typing import Optional
from bson.objectid import ObjectId


class Project(BaseModel):
    id:Optional[ObjectId] = Field(None,alias="_id")
    projectId:str=Field(...,min_length=1)
    
    @field_validator("projectId")
    def validateProjectId(cls,value):
        if not value.isalnum():
            raise ValueError("project id must be alphanumeric")
        return value

    class Config:
        arbitrary_types_allowed=True
        allow_population_by_field_name = True

