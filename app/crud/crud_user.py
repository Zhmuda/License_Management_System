from sqlalchemy.orm import Session
from app.models.user import User
from app.schemas.user import UserCreate
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(db: Session, user: UserCreate):
    if user.role not in ["admin", "manager"]:
        raise ValueError("Invalid role. Allowed roles are: admin, manager.")

    hashed_password = pwd_context.hash(user.password)

    db_user = User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user


def update_user_role(db: Session, user_id: int, role: str):
    if role not in ["admin", "manager"]:
        raise ValueError("Invalid role. Allowed roles are: admin, manager.")

    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user:
        db_user.role = role
        db.commit()
        db.refresh(db_user)
        return db_user
    return None


def delete_user(db: Session, user_id: int):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return False
    db.delete(user)
    db.commit()
    return True


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
