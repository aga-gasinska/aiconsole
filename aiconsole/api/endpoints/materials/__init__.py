
from fastapi import APIRouter

from . import material, index

router = APIRouter()

router.include_router(material.router)
router.include_router(index.router)