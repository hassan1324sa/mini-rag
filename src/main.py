from fastapi import FastAPI
from routes  import base
from routes  import data


app = FastAPI(title="Mini Rag ", version="0.1")
app.include_router(base.baseRouter)
app.include_router(data.dataRouter)