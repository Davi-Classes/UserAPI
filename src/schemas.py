from uuid import UUID
from datetime import datetime
from pydantic import BaseModel, EmailStr


class MessageOut(BaseModel):
    message: str


class UserIn(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    name: str
    email: str
    fl_active: bool
    created_at: datetime
