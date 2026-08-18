from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, SessionLocal, engine
from app.routers import admin, auth, summarize
from app.seed_admin import seed_admin

app = FastAPI(title="Summarize-AI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        seed_admin(db)
    finally:
        db.close()


app.include_router(auth.router)
app.include_router(summarize.router)
app.include_router(admin.router)


@app.get("/health")
def health():
    return {"status": "ok"}
