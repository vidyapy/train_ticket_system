from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TrainNameResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True