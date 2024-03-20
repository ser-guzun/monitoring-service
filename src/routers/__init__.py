from fastapi import APIRouter

from src.routers import links

router = APIRouter()

router.include_router(links.router)
