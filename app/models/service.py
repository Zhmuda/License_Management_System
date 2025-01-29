from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    object_id = Column(Integer, ForeignKey("objects.id"))

    object = relationship("Object", back_populates="services")
    licenses = relationship("License", back_populates="service")