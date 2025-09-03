from .baseController import BaseController
from .projectController import ProjectController
from fastapi import UploadFile
from models.enums.responseEnum import ResponseSignal
import re 
import os 
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.sizeScale = 1048576
    
    def validateUploadedFiles(self,file:UploadFile):
        if (file.content_type in self.appSettings.FILE_ALLOWED_EXTNSTIONS) and (file.size <= (self.appSettings.FILE_MAX_SIZE*self.sizeScale)):
            return True,ResponseSignal.FileUploadedSuccess.value

        else:
            return False ,ResponseSignal.fileTypeNotSupportedOrFileSizeExceeded.value

    def getCleanFileName(self,orgFileName):
        cleanedFileName =  re.sub(r'[^\w.]', '', orgFileName.strip())

        return cleanedFileName.replace(" ","_")
    
    def generateUniqueFilename(self,orgFileName:str,projectId:str):
        
        randomFileName =self.generateRandomString()
        
        projectPath = ProjectController().getProjectPath(projectId=projectId)
        
        cleanedFileName = self.getCleanFileName(orgFileName=orgFileName)
        
        newFilePath = os.path.join(projectPath,randomFileName+"_"+cleanedFileName)

        while os.path.exists(newFilePath):
        
            randomFileName = self.generateRandomString()
        
            newFilePath = os.path.join(projectPath,randomFileName+"_"+cleanedFileName)   
        
        return newFilePath,randomFileName+"_"+cleanedFileName
