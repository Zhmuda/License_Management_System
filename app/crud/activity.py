from sqlalchemy.orm import Session
from app.models.activity_log import ActivityLog

def log_activity(db: Session, action: str, details: str):
    db_activity = ActivityLog(action=action, details=details)
    db.add(db_activity)
    db.commit()
    db.refresh(db_activity)
    return db_activity

def get_recent_activitiess(db: Session, limit: int = 10):
    return db.query(ActivityLog).order_by(ActivityLog.timestamp.desc()).limit(limit).all()