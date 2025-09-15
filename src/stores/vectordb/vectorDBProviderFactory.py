from .providers import QdrantDB
from vectorDBEnum import VectorDBEnums
from controllers.baseController import BaseController

class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.baseController = BaseController()

    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
            db_path = self.baseController.getDatabasePath(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
            )
        
        return None