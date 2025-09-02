from fastapi import FastAPI

app = FastAPI(title="Mini Rag ", version="0.1")


@app.get("/")
def welcome():
    return{
        "message":"hello"
    }

@app.get("/welcome")
def welcome():
    return{
        "message":"hello"
    }