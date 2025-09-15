from fastapi import FastAPI
from routes  import base,data
from helpers.config import getSettings
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.llmProviderFactory import LLMProviderFactory
app = FastAPI(title="Mini Rag ", version="0.1")

async def startupDbClient():
    
    settings = getSettings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    llmProviderFactory = LLMProviderFactory(settings)
    app.generationClient = llmProviderFactory.create(provider=settings.GENERATION_BACKEND)
    app.generationClient.setGenerationModel(modelId=settings.GENERATION_MODEL_ID)
    app.embeddingClient = llmProviderFactory.create(provider=settings.EMBEDDING_BACKEND)
    app.embeddingClient.setEmbeddingModel(modelId=settings.EMBEDDING_MODEL_ID)
    app.embeddingClient.setEmbeddingModel(modelId=settings.EMBEDDING_MODEL_SIZE)

async def shutDown():
    app.mongo_conn.close()

app.router.lifespan.on_startup.append(startupDbClient)
app.router.lifespan.on_shutdown.append(shutDown)

app.include_router(base.baseRouter)
app.include_router(data.dataRouter)

