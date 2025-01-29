from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.crud.license import (
    get_active_licenses_count,
    get_inactive_licenses_count,
    get_expiring_this_month_licenses_count,
    get_expired_licenses_count,
    get_active_licenses_trends,
    get_licenses_expiring_soons,
)
from app.crud.activity import (
    get_recent_activitiess
)
from app.database import SessionLocal


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/dashboard/license_stats")
def get_license_stats(db: Session = Depends(get_db)):
    return {
        "active_licenses": get_active_licenses_count(db),
        "inactive_licenses": get_inactive_licenses_count(db),
        "expiring_this_month": get_expiring_this_month_licenses_count(db),
        "expired_licenses": get_expired_licenses_count(db)
    }

@router.get("/dashboard/active_licenses_trend")
def get_active_licenses_trend(period: str = "day", db: Session = Depends(get_db)):
    return {
        "active_licenses_trend": get_active_licenses_trends(db, period)
    }

@router.get("/dashboard/licenses_expiring_soon")
def get_licenses_expiring_soon(days: int = 7, db: Session = Depends(get_db)):
    licenses = get_licenses_expiring_soons(db, days)
    return {
        "licenses_expiring_soon": [
            {
                "id": license.id,
                "client_id": license.service.object.client.id,
                "client_name": license.service.object.client.company_name,
                "end_date": license.end_date
            }
            for license in licenses
        ]
    }

@router.get("/dashboard/recent_activities")
def get_recent_activities(limit: int = 10, db: Session = Depends(get_db)):
    activities = get_recent_activitiess(db, limit)
    return {
        "recent_activities": [
            {
                "id": activity.id,
                "action": activity.action,
                "details": activity.details,
                "timestamp": activity.timestamp
            }
            for activity in activities
        ]
    }