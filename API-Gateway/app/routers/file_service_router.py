import json

from fastapi import APIRouter

from app.config import exchanges_routing
from app.schemas.file_service_schema import GetPresignedURLRequest, GetPresignedURLResponse
from app.utils.pika_helper_gateway import pika_handler

router = APIRouter()


@router.post(path="/get-presigned-url",
             name="Get presigned url",
             description="Get presigned url for uploading file",
             response_model=GetPresignedURLResponse
             )
async def route_get_presigned(request: GetPresignedURLRequest):
    payload = request.json()
    payload = payload.encode('utf-8')

    corr_id = await pika_handler.send_message(
        exchange_name=exchanges_routing.file_exchange,
        routing_key=exchanges_routing.file_get_presigned_url_routing_key,
        message=payload
    )

    response = await pika_handler.get_response(corr_id)

    response = json.loads(response)

    return GetPresignedURLResponse(**response)

