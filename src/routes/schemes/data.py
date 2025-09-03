from pydantic import BaseModel
from typing import Optional

class ProcessRequest(BaseModel):
    fileId:str
    chunkSize:Optional[int] = 100
    overlap:Optional[int]=20
    doReset: Optional[int]=0
    