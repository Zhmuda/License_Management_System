from app.models.client import Client
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.object import Object
from app.schemas.object import ObjectCreate

def get_object(db: Session, object_id: int):
    return db.query(Object).filter(Object.id == object_id).first()

def get_objects(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Object).offset(skip).limit(limit).all()

def create_object(db: Session, object: ObjectCreate):
    db_client = db.query(Client).filter(Client.id == object.client_id).first()
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")

    db_object = Object(**object.model_dump())
    db.add(db_object)
    db.commit()
    db.refresh(db_object)
    return db_object

def update_object(db: Session, object_id: int, object_data: ObjectCreate):
    db_object = db.query(Object).filter(Object.id == object_id).first()

    if not db_object:
        return None

    for key, value in object_data.dict(exclude_unset=True).items():
        setattr(db_object, key, value)

    db.commit()
    db.refresh(db_object)

    return db_object

def delete_object(db: Session, object_id: int):
    db_object = db.query(Object).filter(Object.id == object_id).first()

    if not db_object:
        return False

    db.delete(db_object)
    db.commit()

    return True
