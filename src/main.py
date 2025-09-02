from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv("./.env")
from routes  import base


app = FastAPI(title="Mini Rag ", version="0.1")
app.include_router(base.baseRouter)