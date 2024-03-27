from pydantic import BaseModel

class TimestampBaseModel(BaseModel):
    created_at: str
