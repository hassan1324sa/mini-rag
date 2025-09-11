from .baseDataModel import BaseDataModel
from .dbSchemes import Project
from .enums.dataBaseEunm import DataBaseEnum


class ProjectModel(BaseDataModel):
    def __init__(self, dbClient:object):
        super().__init__(dbClient)
        self.collection = dbClient[DataBaseEnum.collectionProjectEnum.value]
    
    async def createProject(self,project:Project):
        result = await self.collection.insert_one(project.dict(by_alias=True,exclude_unset=True))
        project._id = result.inserted_id
        return project
    
    async def getProjectOrCreateOne(self,projectId:str):
        record = await self.collection.find_one({
            "projectId":projectId
        })
        if record is None:
            project = Project(projectId=projectId)
            project = await self.createProject(project)
            return project
        return Project(**record)
    
    async def getAllProjects(self,page:int=1,pageSize:int=10):
        totalDocuments = await self.collection.count_documents({})
        totalPages = totalDocuments // pageSize
        if (totalDocuments % pageSize) > 0:
            totalPages += 1
        cursor = self.collection.find().skip((page-1)* pageSize).limit(pageSize)
        projects = []
        async for document in cursor:
            projects.append(Project(**document))
        return projects,totalPages
    
