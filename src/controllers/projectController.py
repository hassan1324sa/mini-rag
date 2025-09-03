from .baseController import BaseController
from fastapi import UploadFile
from models.enums.responseEnum import ResponseSignal
import os

class ProjectController(BaseController):
    def __init__(self):
        super().__init__()

    def getProjectPath(self,projectId):
        projectDir = os.path.join(self.filesDir,str(projectId)) 


        if not os.path.exists(projectDir):
            os.makedirs(projectDir)

        return projectDir
