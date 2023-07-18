import json
import uuid

from fastapi import APIRouter

from app.utils.pika_utils import pika_helper

from app.config import settings

router = APIRouter()


@router.get(path="/health-check",
            name="Health Check",
            description="Provides a health check for a service",
            # response_model=
            )
async def route_health_check():
    raise NotImplementedError
