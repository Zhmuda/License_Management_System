from fastapi import FastAPI
from app.api import clients, objects, services, licenses, dashboard
from app.database import engine, Base
from app.api.api_user import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(clients.router, prefix="/api", tags=["Clients"])
app.include_router(objects.router, prefix="/api", tags=["Objects"])
app.include_router(services.router, prefix="/api", tags=["Services"])
app.include_router(licenses.router, prefix="/api", tags=["Licenses"])
app.include_router(dashboard.router, prefix="/api", tags=["Dashboard"])
app.include_router(user_router, prefix="/settings", tags=["Users"])