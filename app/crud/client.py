from sqlalchemy.orm import Session
from sqlalchemy.sql import func
from app.schemas.client import ClientCreate
from app.crud.activity import log_activity
from datetime import datetime, timedelta
from app.models import Client, License
from app.utils import send_email

def get_client(db: Session, client_id: int):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        return None

    # Подсчёт активных лицензий
    active_licenses_count = (
        db.query(func.count(License.id))
        .filter(License.client_id == client_id, License.is_active == True)
        .scalar()
    )

    return {
        **client.__dict__,
        "active_licenses_count": active_licenses_count,
        "is_active": active_licenses_count > 0,
    }

def get_clients(db: Session, skip: int = 0, limit: int = 100):
    clients = db.query(Client).offset(skip).limit(limit).all()

    clients_with_licenses = []
    for client in clients:
        active_licenses_count = (
            db.query(func.count(License.id))
            .filter(License.client_id == client.id, License.is_active == True)
            .scalar()
        )
        clients_with_licenses.append(
            {
                **client.__dict__,
                "active_licenses_count": active_licenses_count,
                "is_active": active_licenses_count > 0,
            }
        )

    return clients_with_licenses

def create_client(db: Session, client: ClientCreate):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    log_activity(db, action="client_created", details=f"Client ID: {db_client.id}")

    return db_client

def update_clients(db: Session, client_id: int, client: ClientCreate):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return None

    for key, value in client.dict(exclude_unset=True).items():
        if getattr(db_client, key) != value:
            setattr(db_client, key, value)

    db.commit()
    db.refresh(db_client)

    log_activity(db, action="client_updated", details=f"Client ID: {db_client.id} updated")

    return db_client

def delete_clients(db: Session, client_id: int):
    db_client = db.query(Client).filter(Client.id == client_id).first()
    if not db_client:
        return False

    db.delete(db_client)
    db.commit()

    log_activity(db, action="client_deleted", details=f"Client ID: {client_id} deleted")

    return True


def notify_clients_about_expiring_licenses(db: Session):
    today = datetime.today()

    clients = db.query(Client).filter(Client.is_active == True).all()

    for client in clients:
        expiration_date = today + timedelta(days=client.notify_before_days)

        expiring_licenses = db.query(License).filter(
            License.client_id == client.id,
            License.end_date == expiration_date,
            License.is_active == True
        ).all()

        for license in expiring_licenses:
            subject = "Ваша лицензия скоро истечет"
            body = f"Здравствуйте, {client.company_name}!\n\nВаша лицензия на сервис '{license.service.name}' истекает через {client.notify_before_days} дня(ей). Пожалуйста, обновите ее вовремя."
            send_email(client.email, subject, body)
