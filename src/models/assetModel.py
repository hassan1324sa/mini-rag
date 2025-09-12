from .baseDataModel import BaseDataModel
from .dbSchemes import Asset
from .enums.dataBaseEunm import DataBaseEnum
from bson import ObjectId

class AssetModel(BaseDataModel):
    
    def __init__(self, dbClient:object):
        super().__init__(dbClient)
        self.collection = dbClient[DataBaseEnum.collectionAssetName.value]
    
    @classmethod
    async def createInstance(cls,dbClient:object):
        instance = cls(dbClient)
        await instance.initCollection()
        return instance
    

    async def initCollection(self):
        allCollections = await self.dbClient.list_collection_names()
        if DataBaseEnum.collectionAssetName.value not in allCollections:
            self.collection = self.dbClient[DataBaseEnum.collectionAssetName.value]
            indexes = Asset.getIndexes()
            for index in indexes:
                await self.collection.create_index(
                    index["key"],
                    name=index["name"],
                    unique=index["unique"]
                )
    
    async def createAsset(self,asset:Asset):
        
        result = await self.collection.insert_one(asset.dict(by_alias=True,exclude_unset=True))

        asset.id = result.inserted_id
        return asset

    async def getAllProjectAssets(self,assetProjectId):
        return await self.collection.find(
                {"assetProjectId":ObjectId(assetProjectId) if isinstance(assetProjectId,str)else assetProjectId}
            ).to_list(length=None)
