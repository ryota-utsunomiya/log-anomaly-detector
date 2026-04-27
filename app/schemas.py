from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LogCreate(BaseModel):
    message:str
    source:str
     
    class Config:
        orm_mode=True
        