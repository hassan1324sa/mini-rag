from enum import Enum

class LLmEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"

class OpenAiEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"