from .baseController import BaseController
from fastapi import UploadFile
class DataController(BaseController):
    def __init__(self):
        super().__init__()
        self.sizeScale = 1048576
    
    def validateUploadedFiles(self,file:UploadFile):
        if (file.content_type in self.appSettings.FILE_ALLOWED_EXTNSTIONS) and (file.size <= (self.appSettings.FILE_MAX_SIZE*self.sizeScale)):
            return True,"success"

        else:
            return False ,"file type is not supported or file size exceeded"
        