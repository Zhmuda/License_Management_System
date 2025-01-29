from sqlalchemy import Column, Integer, String, DateTime, Enum
from app.database import Base
from datetime import datetime

class ActivityLog(Base):
    __tablename__ = "activity_log"

    id = Column(Integer, primary_key=True, index=True)
    action = Column(String)
    details = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)