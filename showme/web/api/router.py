from fastapi.routing import APIRouter

from showme.web.api import monitoring
from showme.web.api import country
from showme.web.api import kafka

api_router = APIRouter()
api_router.include_router(monitoring.router)
api_router.include_router(country.router)
api_router.include_router(kafka.router)
