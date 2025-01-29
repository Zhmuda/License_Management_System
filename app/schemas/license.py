from datetime import date
from pydantic import BaseModel, Field

class LicenseBase(BaseModel):
    start_date: date = Field(default_factory=date.today)
    end_date: date
    service_id: int
    client_id: int
    is_active: bool

class LicenseCreate(LicenseBase):
    pass
class License(LicenseBase):
    id: int

    class Config:
        from_attributes = True