#
from fastapi import FastAPI
from app.api.routes.health import router as health_router
from app.api.routes.db_test import router as db_test_router
from app.core.config import settings
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix="/health", tags=["health"])
app.include_router(db_test_router, prefix="/db", tags=["db"])
