from fastapi import FastAPI
from routes  import base,data , nlp
from helpers.config import getSettings
from motor.motor_asyncio import AsyncIOMotorClient
from stores.llm.llmProviderFactory import LLMProviderFactory
from stores.vectordb.vectorDBProviderFactory import VectorDBProviderFactory
from stores.llm.templates.templateParser import TemplateParser
app = FastAPI(title="Mini Rag ", version="0.1")
@app.on_event("startup")
async def startupSpan():
    
    settings = getSettings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]
    
    llmProviderFactory = LLMProviderFactory(settings)
    vectorDBProviderFactory = VectorDBProviderFactory(settings) 


    app.generationClient = llmProviderFactory.create(provider=settings.EMBEDDING_BACKEND)
    app.generationClient.setGenerationModel(modelId=settings.GENERATION_MODEL_ID)
    app.embeddingClient = llmProviderFactory.create(provider=settings.EMBEDDING_BACKEND)
    app.embeddingClient.setEmbeddingModel(modelId=settings.EMBEDDING_MODEL_ID,embeddingSize=settings.EMBEDDING_MODEL_SIZE)

    app.vectorDBClient = vectorDBProviderFactory.create(provider=settings.VECTOR_DB_BACKEND)
    app.vectorDBClient.connect()
    app.templateParser = TemplateParser(
        lang=settings.PRIMARY_LANG,
        defaultLang=settings.DEFAULT_LANG
    )

@app.on_event("shutdown")
async def shutDownSpan():
    app.mongo_conn.close()
    app.vectorDBClient.disconnect()

# app.router.lifespan.on_startup.append(startupSpan)
# app.router.lifespan.on_shutdown.append(shutDownSpan)

app.include_router(base.baseRouter)
app.include_router(data.dataRouter)
app.include_router(nlp.nlpRouter)

