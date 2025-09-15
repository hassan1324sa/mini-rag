from abc import abstractmethod,ABC

class LLmInterface(ABC):
    def __init__(self):
        super().__init__()
    
    
    @abstractmethod
    def setGenerationModel(self,modelId:str):
        pass
    
    @abstractmethod
    def setEmbeddingModel(self,modelId:str,embeddingSize:int):
        pass

    @abstractmethod
    def generateText(self,chatHistory:list,prompt:str,maxOutputToken:int,temp:float):
        pass

    @abstractmethod
    def EmbedText(self,text:str,documentType:str=None):
        pass
    
    @abstractmethod
    def constructPrompt(self,prompt:str,role:str):
        pass
