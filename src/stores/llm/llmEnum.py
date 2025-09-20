from enum import Enum

class LLmEnums(Enum):
    OPENAI = "OPENAI"
    COHERE = "COHERE"
    OLLAMA = "OLLAMA"

class OpenAiEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class CohereEnum(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    DOCUMENt = "search_document"
    QUERY = "search_query"
class OllamaEnums(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"

class DocumentTypeEnum(Enum):
    DOCUMENt = "document"
    QUERY = "query"
