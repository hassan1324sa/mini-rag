from pydantic import BaseModel
from typing import Optional

class PushReq(BaseModel):
    doReset:Optional[int]=0



class SearchReq(BaseModel):
    text:str
    limit:Optional[int]=10