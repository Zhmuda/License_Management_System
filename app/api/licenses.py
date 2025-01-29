from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/licenses/", response_model=schemas.License)
def create_license(license: schemas.LicenseCreate, db: Session = Depends(get_db)):
    return crud.create_license(db=db, license=license)

@router.get("/licenses/", response_model=list[schemas.License])
def read_licenses(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    licenses = crud.get_licenses(db, skip=skip, limit=limit)
    return licenses

@router.get("/licenses/{license_id}", response_model=schemas.License)
def read_license(license_id: int, db: Session = Depends(get_db)):
    db_license = crud.get_license(db, license_id=license_id)
    if db_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return db_license

@router.put("/licenses/{license_id}", response_model=schemas.License)
def update_license(license_id: int, license: schemas.LicenseCreate, db: Session = Depends(get_db)):
    updated_license = crud.update_license(db=db, license_id=license_id, license_data=license)
    if updated_license is None:
        raise HTTPException(status_code=404, detail="License not found")
    return updated_license

@router.delete("/licenses/{license_id}")
def delete_license(license_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_license(db=db, license_id=license_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="License not found")
    return {"message": "License successfully deleted"}