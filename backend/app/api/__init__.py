"""API module exports"""
from app.api.auth import router as auth_router
from app.api.examens import router as examens_router
from app.api.dashboard import router as dashboard_router

__all__ = [
    "auth_router",
    "examens_router", 
    "dashboard_router"
]
