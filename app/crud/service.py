from app.models.object import Object
from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.service import Service
from app.schemas.service import ServiceCreate

def get_service(db: Session, service_id: int):
    return db.query(Service).filter(Service.id == service_id).first()

def get_services(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Service).offset(skip).limit(limit).all()

def create_service(db: Session, service: ServiceCreate):
    db_object = db.query(Object).filter(Object.id == service.object_id).first()
    if not db_object:
        raise HTTPException(status_code=404, detail="Object not found")

    db_service = Service(**service.model_dump())
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service

def update_service(db: Session, service_id: int, service_data: ServiceCreate):
    db_service = db.query(Service).filter(Service.id == service_id).first()

    if not db_service:
        return None

    for key, value in service_data.dict(exclude_unset=True).items():
        setattr(db_service, key, value)

    db.commit()
    db.refresh(db_service)

    return db_service

def delete_service(db: Session, service_id: int):
    db_service = db.query(Service).filter(Service.id == service_id).first()

    if not db_service:
        return False

    db.delete(db_service)
    db.commit()

    return True
