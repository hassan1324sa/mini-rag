from .baseController import BaseController
from .projectController import ProjectController
import os 
from langchain_community.document_loaders import TextLoader
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from models import ProcessingEnum

class ProcessController(BaseController):
    def __init__(self,projectId:str):
        
        super().__init__()
        
        self.projectId = projectId

        self.projectPath = ProjectController().getProjectPath(projectId=self.projectId)
    
    def getFileExtension(self,fileName:str):
        return os.path.splitext(fileName)[-1]
    
    def getFileLoader(self,fileId:str,):
        fileExt =self.getFileExtension(fileId)
        filePath = os.path.join(self.projectPath,fileId)
        if fileExt == ProcessingEnum.TXT.value:
            return TextLoader(filePath,encoding="utf-8")
        if fileExt == ProcessingEnum.PDF.value:
            return PyMuPDFLoader(filePath)
        return None
    
    def getFileContent(self,fileId:str):
        loader  = self.getFileLoader(fileId=fileId)
        return loader.load()
    
    def processFileContent(self,fileContent:list,fileId:str,chunkSize:int=100,overlapSize:int=20):
        
        textSplitter = RecursiveCharacterTextSplitter(chunk_size=chunkSize,chunk_overlap=overlapSize,length_function=len)
        
        fileContentTexts=[i.page_content for i in fileContent]
        
        fileContentMetadata=[i.metadata for i in fileContent]
        
        chunks = textSplitter.create_documents(fileContentTexts,fileContentMetadata)
        
        return chunks