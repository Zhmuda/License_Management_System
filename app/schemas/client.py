from pydantic import BaseModel, EmailStr, Field
from typing import List, Optional
from app.schemas.license import License

class ClientBase(BaseModel):
    company_name: str = Field(..., max_length=250)
    inn: str = Field(..., min_length=10, max_length=12)
    contact_person: str = Field(..., max_length=250)
    email: EmailStr
    phone: str = Field(..., pattern=r"^\+?\d{10,15}$")
    notify_before_days: int = Field(3, ge=1)

class ClientCreate(ClientBase):
    pass

class Client(ClientBase):
    id: int
    is_active: bool
    active_licenses_count: Optional[int] = None

    class Config:
        from_attributes = True
