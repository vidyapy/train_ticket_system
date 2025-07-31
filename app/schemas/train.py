from pydantic import BaseModel


class TrainNameResponse(BaseModel):
    id: int
    name: str
    
    class Config:
        from_attributes = True