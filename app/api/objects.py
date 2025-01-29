from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud
from app.schemas.object import Object, ObjectCreate
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/objects/", response_model=Object)
def create_object(object: ObjectCreate, db: Session = Depends(get_db)):
    return crud.create_object(db=db, object=object)

@router.get("/objects/", response_model=list[Object])
def read_objects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    objects = crud.get_objects(db, skip=skip, limit=limit)
    return objects

@router.get("/objects/{object_id}", response_model=Object)
def read_object(object_id: int, db: Session = Depends(get_db)):
    db_object = crud.get_object(db, object_id=object_id)
    if db_object is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return db_object

@router.put("/objects/{object_id}", response_model=Object)
def update_object(object_id: int, object: ObjectCreate, db: Session = Depends(get_db)):
    updated_object = crud.update_object(db=db, object_id=object_id, object_data=object)
    if updated_object is None:
        raise HTTPException(status_code=404, detail="Object not found")
    return updated_object

@router.delete("/objects/{object_id}")
def delete_object(object_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_object(db=db, object_id=object_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Object not found")
    return {"message": "Object successfully deleted"}