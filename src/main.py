from fastapi import FastAPI
from routes  import base,data
from helpers.config import getSettings
from motor.motor_asyncio import AsyncIOMotorClient
app = FastAPI(title="Mini Rag ", version="0.1")

@app.on_event("startup")
async def startupDbClient():
    
    settings = getSettings()
    
    app.mongo_conn = AsyncIOMotorClient(settings.MONGODB_URL)
    
    app.db_client = app.mongo_conn[settings.MONGODB_DATABASE]

@app.on_event("shutdown")
async def shutDown():
    app.mongo_conn.close()

app.include_router(base.baseRouter)
app.include_router(data.dataRouter)

