from pydantic import BaseModel
from datetime import datetime


class TimestampBaseModel(BaseModel):
    created_at: datetime = datetime.now()
