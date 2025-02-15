from uuid import UUID, uuid4
from pydantic import BaseModel, Field
from datetime import datetime, timezone


class User(BaseModel):
    id: UUID = Field(default_factory=uuid4) 
    name: str 
    email: str
    password: str 
    fl_active: bool = True 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc)) 
