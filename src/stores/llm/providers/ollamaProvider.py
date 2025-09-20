import requests
import logging
from ..llmInterface import LLmInterface
from ..llmEnum import OllamaEnums
class OllamaProvider(LLmInterface):
    def __init__(self, baseUrl: str = "http://localhost:11434",
                       maxCharactersInputs: int = 1000,
                       maxCharactersOutputs: int = 1000,
                       temp: float = 0.2):
        super().__init__()
        self.baseUrl = baseUrl
        self.maxCharactersInputs = maxCharactersInputs
        self.maxCharactersOutputs = maxCharactersOutputs
        self.temp = temp
        self.generationModelId = None
        self.embeddingModelId = None
        self.embeddingSize = None
        self.logger = logging.getLogger(__name__)
        self.enums = OllamaEnums

    def setGenerationModel(self, modelId):
        self.generationModelId = modelId

    def setEmbeddingModel(self, modelId, embeddingSize):
        self.embeddingModelId = modelId
        self.embeddingSize = embeddingSize

    def processText(self, text):
        return text[:self.maxCharactersInputs].strip()

    def generateText(self, chatHistory: list, prompt: str, maxOutputToken: int = None, 
                     temp: float = None, stream: bool = False):
        if not self.generationModelId:
            self.logger.error("Ollama generation model not set")
            return None

        url = f"{self.baseUrl}/api/chat"
        payload = {
            "model": self.generationModelId,
            "messages": chatHistory + [
                {"role": "user", "content": self.processText(prompt)}
            ],
            "options": {
                "temperature": temp if temp else self.temp,
                "num_predict": maxOutputToken if maxOutputToken else self.maxCharactersOutputs
            },
            "stream": stream
        }

        try:
            resp = requests.post(url, json=payload, stream=stream)
            resp.raise_for_status()

            if not stream:
                data = resp.json()
                return data["message"]["content"]

            final_text = ""
            for line in resp.iter_lines():
                if line:
                    data = line.decode("utf-8")
                    try:
                        chunk = requests.utils.json.loads(data)
                        if "message" in chunk and "content" in chunk["message"]:
                            final_text += chunk["message"]["content"]
                    except Exception as e:
                        self.logger.warning(f"skip line parse error: {e}")
            return final_text

        except Exception as e:
            self.logger.error(f"Ollama request failed: {e}")
            return None

    def EmbedText(self, text, documentType=None):
        if not self.embeddingModelId:
            self.logger.error("Ollama embedding model not set")
            return None

        url = f"{self.baseUrl}/api/embeddings"
        payload = {
            "model": self.embeddingModelId,
            "input": self.processText(text)
        }

        try:
            resp = requests.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["embedding"]
        except Exception as e:
            self.logger.error(f"Ollama embedding failed: {e}")
            return None
    def constructPrompt(self, prompt, role):
        return {
            "role": role,
            "content": self.processText(prompt)
        }