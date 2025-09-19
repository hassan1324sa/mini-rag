from llmInterface import LLmInterface
from llmEnum import OpenAiEnum
from ..llmInterface import LLmInterface
from ..llmEnum import OpenAiEnum
from openai import OpenAI
import logging

class OpenAiProvider(LLmInterface):
    def __init__(self,apiKey:str,apiUrl:str=None,
                      maxCharactersInputs:int=1000,
                      maxCharactersOutputs:int=1000,
                      temp:float=0.2):
        super().__init__()
        self.apiKey =  apiKey
        self.apiUrl =  apiUrl
        self.maxCharactersInputs =  maxCharactersInputs
        self.maxCharactersOutputs =  maxCharactersOutputs
        self.temp =  temp
        self.generationModelId = None
        self.embeddingModelId = None
        self.embeddingSize = None
        self.client = OpenAI(api_key=apiKey,api_url=apiUrl)
        self.enums = OpenAiEnum
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
            self.logger.error("openAI client was not set ")
        
        if not self.embeddingModelId:
            self.logger.error("Model Id was not set ")
        
        maxOutputToken = maxOutputToken if maxOutputToken is not None else self.maxCharactersOutputs
        temp = temp if temp else self.temp

        chatHistory.append(self.constructPrompt(prompt=prompt,role=OpenAiEnum.USER.value))
        response = self.client.chat.completions.create(
            model = self.generationModelId,
            messages = chatHistory,
            max_tokens=maxOutputToken,
            temperature=temp
        )

        if not response or not response.choices or len(response.choices) < 1 or not response.choices[0].message:
            self.logger.error("error while generating text with openAi")
            return None
        return response.choices[0].message["content"]

    def EmbedText(self, text, documentType=None):
        
        if not self.client:
            self.logger.error("openAI client was not set ")
        
        if not self.embeddingModelId:
            self.logger.error("embedding Model Id was not set ")
        
        response = self.client.embedding.create(
            model=self.embeddingModelId,
            input=text,
        )
        
        if not response or not response.data or len(response.data)<1 or response.data[0].embedding:

            self.logger.error("error while embedding text ")
            return None
        return response.data[0].embedding

    def constructPrompt(self, prompt, role):
        return {
            "OpenAiEnum":role,
            "prompt":self.processText(prompt)
        }