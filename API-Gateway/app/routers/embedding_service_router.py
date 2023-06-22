import json

from fastapi import APIRouter

from app.config import exchanges_routing
from app.schemas.embedding_service_schema import EmbedRequest, EmbedResponse, CrossEncodeRequest, CrossEncodeResponse
from app.utils.pika_helper_gateway import pika_handler

router = APIRouter()


@router.post(path="/embed",
             name="Sentence Embedding",
             description="Generate embeddings for sentences",
             response_model=EmbedResponse
             )
async def route_embedding(request: EmbedRequest):
    payload = request.json()
    payload = payload.encode('utf-8')

    corr_id = await pika_handler.send_message(
        exchange_name=exchanges_routing.embedding_exchange,
        routing_key=exchanges_routing.embedding_embed_routing_key,
        message=payload
    )

    response = await pika_handler.get_response(corr_id)

    response = json.loads(response)

    return EmbedResponse(**response)


@router.post(path="/rerank",
             name="Rerank embeddings",
             description="Reranking embeddings based on query",
             response_model=CrossEncodeResponse
             )
async def route_rerank(request: CrossEncodeRequest):
    payload = request.json()
    payload = payload.encode('utf-8')

    corr_id = await pika_handler.send_message(
        exchange_name=exchanges_routing.embedding_exchange,
        routing_key=exchanges_routing.embedding_rerank_routing_key,
        message=payload
    )

    response = await pika_handler.get_response(corr_id)

    response = json.loads(response)

    return CrossEncodeResponse(**response)
