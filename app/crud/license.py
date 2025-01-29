from app.models.service import Service
from fastapi import HTTPException
from sqlalchemy import func, and_, or_
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.license import License
from app.schemas.license import LicenseCreate
from app.crud.activity import log_activity

def get_license(db: Session, license_id: int):
    return db.query(License).filter(License.id == license_id).first()

def get_licenses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(License).offset(skip).limit(limit).all()

def create_license(db: Session, license: LicenseCreate):
    db_service = db.query(Service).filter(Service.id == license.service_id).first()
    if not db_service:
        raise HTTPException(status_code=404, detail="Service not found")

    db_license = License(**license.model_dump())
    db.add(db_license)
    db.commit()
    db.refresh(db_license)

    log_activity(db, action="license_created", details=f"License ID: {db_license.id} for Service ID: {license.service_id}")

    return db_license

def get_active_licenses_count(db: Session):
    return db.query(License).filter(License.is_active == True).count()

def get_inactive_licenses_count(db: Session):
    return db.query(License).filter(License.is_active == False).count()

def get_expiring_this_month_licenses_count(db: Session):
    today = datetime.today()
    end_of_month = today.replace(day=28) + timedelta(days=4)  # Конец текущего месяца
    return db.query(License).filter(
        and_(
            License.end_date >= today,
            License.end_date <= end_of_month
        )
    ).count()


def get_expired_licenses_count(db: Session):
    yesterday = datetime.today() - timedelta(days=1)
    res = db.query(License).filter(License.end_date < yesterday).count()
    print(res)
    return res

def get_active_licenses_trends(db: Session, period: str):
    today = datetime.today()
    if period == "day":
        start_date = today - timedelta(days=1)
    elif period == "week":
        start_date = today - timedelta(weeks=1)
    elif period == "month":
        start_date = today - timedelta(days=30)
    elif period == "year":
        start_date = today - timedelta(days=365)
    else:
        start_date = today - timedelta(days=1)

    return db.query(License).filter(
        and_(
            License.is_active == True,
            License.start_date >= start_date
        )
    ).count()


def get_licenses_expiring_soons(db: Session, days: int):
    today = datetime.today()
    end_date = today + timedelta(days=days)
    return db.query(License).filter(
        and_(
            License.end_date >= today,
            License.end_date <= end_date
        )
    ).all()

def update_license(db: Session, license_id: int, license_data: LicenseCreate):
    db_license = db.query(License).filter(License.id == license_id).first()

    if not db_license:
        return None

    for key, value in license_data.dict(exclude_unset=True).items():
        setattr(db_license, key, value)

    db.commit()
    db.refresh(db_license)

    log_activity(
        db,
        action="license_updated",
        details=f"License ID: {db_license.id} updated"
    )

    return db_license


def delete_license(db: Session, license_id: int):
    db_license = db.query(License).filter(License.id == license_id).first()

    if not db_license:
        return False

    db.delete(db_license)
    db.commit()

    log_activity(
        db,
        action="license_deleted",
        details=f"License ID: {license_id} deleted"
    )

    return True
