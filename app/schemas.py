from pydantic import BaseModel
from datetime import datetime

class LogBase(BaseModel):
    created: datetime
    int_id: str
    str: str
    address: str

class MessageBase(BaseModel):
    created: datetime
    id: str
    int_id: str
    str: str