from fastapi import APIRouter

router = APIRouter()

# Import and include route modules here
from . import bill_parsing, public_routes

router.include_router(bill_parsing.router, prefix="/ai", tags=["AI"])
router.include_router(public_routes.router, prefix="/public", tags=["Public"])
