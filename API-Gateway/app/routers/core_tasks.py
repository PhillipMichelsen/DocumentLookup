import json
import uuid

from fastapi import APIRouter

from app.config import settings
from app.schemas.core_tasks import embed_store_schemas, retrieve_query_context_schemas
from app.schemas.job_schemas import JobRequest
from app.utils.pika_utils import pika_utils
from app.utils.response_utils import response_utils

router = APIRouter()


@router.post(path="/embed-store-text",
             name="Embed Store Text",
             description="Embeds and stores text given",
             response_model=embed_store_schemas.EmbedStoreResponse
             )
async def route_embed_store_text(request: embed_store_schemas.EmbedStoreRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="embed_store_text",
        requesting_service_exchange=settings.service_exchange,
        requesting_service_return_queue_routing_key=settings.update_result_queue_routing_key,
        requesting_service_id=pika_utils.service_id,
        job_id=job_id,
        job_data=json.dumps(request.model_dump())
    )

    task_result_response_future = await response_utils.create_response(job_id)

    message = json.dumps(job.model_dump())
    await pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_job_request_routing_key,
        message=message.encode('utf-8')
    )

    return_task_id = await task_result_response_future

    job_response_future = await response_utils.create_response(return_task_id)

    response = await job_response_future

    return embed_store_schemas.EmbedStoreResponse.model_validate(json.loads(response))


@router.post(path="/retrieve-query-context",
             name="Retrieve Query Context",
             description="Searches for the closest entries to the given query",
             response_model=retrieve_query_context_schemas.RetrieveQueryContextResponse
             )
async def route_embed_store_text(request: retrieve_query_context_schemas.RetrieveQueryContextRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="retrieve_query_context",
        requesting_service_exchange=settings.service_exchange,
        requesting_service_return_queue_routing_key=settings.update_result_queue_routing_key,
        requesting_service_id=pika_utils.service_id,
        job_id=job_id,
        job_data=json.dumps(request.model_dump())
    )

    task_result_response_future = await response_utils.create_response(job_id)

    message = json.dumps(job.model_dump())
    await pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_job_request_routing_key,
        message=message.encode('utf-8')
    )

    return_task_id = await task_result_response_future

    job_response_future = await response_utils.create_response(return_task_id)

    response = await job_response_future

    return retrieve_query_context_schemas.RetrieveQueryContextResponse.model_validate(json.loads(response))
