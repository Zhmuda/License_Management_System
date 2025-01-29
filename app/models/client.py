from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship
from app.database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    company_name = Column(String, index=True)
    inn = Column(String, unique=True, index=True)
    contact_person = Column(String)
    email = Column(String, unique=True, index=True)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    notify_before_days = Column(Integer, default=3)

    # Обратная связь с лицензиями
    licenses = relationship("License", back_populates="client", cascade="all, delete-orphan")
    objects = relationship("Object", back_populates="client")
