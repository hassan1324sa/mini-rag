from llmEnum import LLMEnums
from providers import openAiProvider, CohereProvider
from .llmEnum import LLmEnums
from .providers import openAiProvider, CohereProvider

class LLMProviderFactory:
    def __init__(self, config: dict):
        self.config = config

    def create(self, provider: str):
        if provider == LLmEnums.OPENAI.value:
            return openAiProvider(
                apiKey = self.config.OPENAI_API_KEY,
                apiUrl = self.config.OPENAI_API_URL,
                maxCharactersInputs=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                maxCharactersOutputs=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                temp=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        if provider == LLMEnums.COHERE.value:
            return CohereProvider(
                apiKey = self.config.COHERE_API_KEY,
                maxCharactersInputs=self.config.INPUT_DAFAULT_MAX_CHARACTERS,
                maxCharactersOutputs=self.config.GENERATION_DAFAULT_MAX_TOKENS,
                temp=self.config.GENERATION_DAFAULT_TEMPERATURE
            )

        return None