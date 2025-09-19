from ..llmInterface import LLmInterface
from ..llmEnum import CohereEnum,DocumentTypeEnum
import cohere
import logging

class CohereProvider(LLmInterface):
    def __init__(self,apiKey:str,
                      maxCharactersInputs:int=1000,
                      maxCharactersOutputs:int=1000,
                      temp:float=0.2):
        super().__init__()
        self.apiKey =  apiKey
        self.maxCharactersInputs =  maxCharactersInputs
        self.maxCharactersOutputs =  maxCharactersOutputs
        self.temp =  temp
        self.generationModelId = None
        self.embeddingModelId = None
        self.embeddingSize = None
        self.client = cohere.Client(api_key=apiKey)
        self.enums = CohereEnum
        self.logger = logging.getLogger(__name__)
    
    def setGenerationModel(self, modelId):
        self.generationModelId = modelId


    def setEmbeddingModel(self, modelId, embeddingSize):
        self.embeddingModelId =modelId 
        self.embeddingSize =embeddingSize

    def processText(self,text):
        return text[:self.maxCharactersInputs].strip()

    def generateText(self,chatHistory:list, prompt, maxOutputToken:int = None, temp:float=None):
        if not self.client:
            self.logger.error("cohere was not set ")
            
        if not self.generationModelId:
            self.logger.error("Model Id was not set ")
        
        maxOutputToken = maxOutputToken if maxOutputToken is not None else self.maxCharactersOutputs
        temp = temp if temp else self.temp

        chatHistory.append(self.constructPrompt(prompt=prompt,role=CohereEnum.USER.value))
        response = self.client.chat(
            model = self.generationModelId,
            chat_history= chatHistory,
            message=self.processText(prompt),
            max_tokens=maxOutputToken,
            temperature=temp
        )

        if not response or not response.text:
            self.logger.error("error while generating text with openAi")
            return None
        
        return response.text

    def EmbedText(self, text, documentType=None):
        
        if not self.client:
            self.logger.error("openAI client was not set ")
        
        if not self.embeddingModelId:
            self.logger.error("embedding Model Id was not set ")
        inputType= CohereEnum.DOCUMENt.value
        if documentType == DocumentTypeEnum.QUERY:
            inputType = CohereEnum.QUERY
        response = self.client.embed(model=self.embeddingModelId,texts=[self.processText(text)],input_type=inputType,embedding_types=['float'])
        if not response or not response.embeddings or not response.embeddings.float:
            self.logger.error("error while embedding text with cohere")
            return None
        return response.embeddings.float[0]



    def constructPrompt(self, prompt: str, role):
        return {
            "role": role,
            "message": self.processText(prompt) 
        }