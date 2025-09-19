<<<<<<< HEAD
from vecotrDBInterface import VectorDBInterFace
import logging
from vectorDBEnum import DistanceMethodEnums
from qdrant_client import QdrantClient,models

=======
from ..vecotrDBInterface import VectorDBInterFace
import logging
from ..vectorDBEnum import DistanceMethodEnums
from qdrant_client import QdrantClient,models
from models.dbSchemes import RetrieveDocs
>>>>>>> 03fc06c (Initial commit)

class QdrantDB(VectorDBInterFace):
    def __init__(self,dbPath:str,distanceMethod:str):
        super().__init__()
        self.client = None
        self.dbPath = dbPath

        if distanceMethod == DistanceMethodEnums.COSINE.value:
<<<<<<< HEAD
            self.distance_method = models.Distance.COSINE
        elif distanceMethod == DistanceMethodEnums.DOT.value:
            self.distance_method = models.Distance.DOT
=======
            self.distanceMethod = models.Distance.COSINE
        elif distanceMethod == DistanceMethodEnums.DOT.value:
            self.distanceMethod = models.Distance.DOT
>>>>>>> 03fc06c (Initial commit)
        self.logger = logging.getLogger(__name__)
    
    def connect(self):
        self.client = QdrantClient(path=self.dbPath)
    
    def disconnect(self):
        self.client = None
    
    def isCollectionExisted(self, collectionName):
        return self.client.collection_exists(collection_name=collectionName)
    
    def listAllCollections(self):
        return self.client.get_collections()

    def getCollectionInfo(self, collectionName):
        return self.client.get_collection(collection_name=collectionName)
    
    def deleteCollection(self, collectionName):
        return self.client.delete_collection(collection_name=collectionName) if self.isCollectionExisted(collectionName=collectionName) else None
    
    def createCollection(self, collectionName, embeddingSize, doReset = False):
        if doReset:
            _ = self.deleteCollection(collectionName=collectionName)
        if not self.isCollectionExisted(collectionName=collectionName):
<<<<<<< HEAD
            _=self.client.create_collection(collection_name=collectionName,vectors_config=models.VectorParams(size=embeddingSize))
=======
            _=self.client.create_collection(collection_name=collectionName,vectors_config=models.VectorParams(size=embeddingSize,distance=self.distanceMethod))
>>>>>>> 03fc06c (Initial commit)
            return True
        return False
    
    def insertOne(self, collectionName, text, vector, metadata = None, recordId = None):
        if not self.isCollectionExisted(collectionName=collectionName):
            self.logger.error(f"can not insert new record to non-existed collection {collectionName}")
            return False
        try:
            _ = self.client.upload_records(
                collection_name=collectionName,
                records=[
<<<<<<< HEAD
                    models.Record(vector=vector,payload={"text":text,"metadata":metadata})
=======
                    models.Record(vector=vector,payload={"text":text,"metadata":metadata},id=[recordId])
>>>>>>> 03fc06c (Initial commit)
                ]
            )
        except Exception as e:
                self.logger.error(f"error while inserting batch : {e}")
                return False
        return True
    
    def insertMany(self, collectionName, texts, vector, metadata = None, recordIds = None, batchSize = 50):
        if metadata is None:
            metadata = [None] * len(texts)
        if recordIds is None:
            recordIds = [None] * len(texts)
        for i in range(0,len(texts),batchSize):
            batchEnd = i + batchSize
            batchText = texts[i:batchEnd]
            batchVectors = vector[i:batchEnd]
            batchMetaData = metadata[i:batchEnd]
<<<<<<< HEAD
            batchRecords = [
                models.Record(vector=batchVectors[x],payload={"text":batchText[x],"metadata":batchMetaData[x]})
=======
            batchRecordsIds = recordIds[i:batchEnd]
            batchRecords = [
                models.Record(id=batchRecordsIds[x],vector=batchVectors[x],payload={"text":batchText[x],"metadata":batchMetaData[x]})
>>>>>>> 03fc06c (Initial commit)
                for x in range(len(batchText))
                ]
            try:
                _ = self.client.upload_records(collection_name=collectionName,records=batchRecords)
            except Exception as e:
                self.logger.error(f"error while inserting batch : {e}")
                return False
        return True
    
<<<<<<< HEAD
    def searchByVector(self, collectionName, vector, limit):
        return self.client.search(collection_name=collectionName,query_vector=vector,limit=limit)
=======
    def searchByVector(self, collectionName, vector, limit=5):
        results = self.client.search(collection_name=collectionName,query_vector=vector,limit=limit)
        if not results or len(results) < 1 :
            return None
        return [
                RetrieveDocs(**{
                        "score":i.score,
                        "text":i.payload["text"]
                })
            for i in results
        ]
>>>>>>> 03fc06c (Initial commit)
