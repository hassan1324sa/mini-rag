from .providers import QdrantDB
<<<<<<< HEAD
from vectorDBEnum import VectorDBEnums
=======
from .vectorDBEnum import VectorDBEnums
>>>>>>> 03fc06c (Initial commit)
from controllers.baseController import BaseController

class VectorDBProviderFactory:
    def __init__(self, config):
        self.config = config
        self.baseController = BaseController()

    def create(self, provider: str):
        if provider == VectorDBEnums.QDRANT.value:
<<<<<<< HEAD
            db_path = self.baseController.getDatabasePath(db_name=self.config.VECTOR_DB_PATH)

            return QdrantDB(
                db_path=db_path,
                distance_method=self.config.VECTOR_DB_DISTANCE_METHOD,
=======
            dbPath = self.baseController.getDatabasePath(dbName=self.config.VECTOR_DB_PATH)

            return QdrantDB(
                dbPath=dbPath,
                distanceMethod=self.config.VECTOR_DB_DISTANCE_METHOD,
>>>>>>> 03fc06c (Initial commit)
            )
        
        return None