from pydantic import BaseModel

class ServiceBase(BaseModel):
    name: str
    object_id: int

class ServiceCreate(ServiceBase):
    pass

class Service(ServiceBase):
    id: int

    class Config:
        from_attributes = True