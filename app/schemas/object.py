from pydantic import BaseModel

class ObjectBase(BaseModel):
    name: str
    client_id: int

class ObjectCreate(ObjectBase):
    pass

class Object(ObjectBase):
    id: int

    class Config:
        from_attributes = True