import json
import uuid

from fastapi import APIRouter

from app.config import settings
from app.schemas.utility_tasks import embed_schemas, cross_encode_schemas, presigned_url_schemas, retrieve_closest_entries_schemas
from app.schemas.job_schemas import JobRequest
from app.utils.pika_utils import pika_utils
from app.utils.response_utils import response_utils

router = APIRouter()


@router.post(path="/embed-text",
             name="Embed Text",
             description="Embeds text given",
             response_model=embed_schemas.EmbedResponse
             )
async def route_embed_text(request: embed_schemas.EmbedRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="embed_text",
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

    return embed_schemas.EmbedResponse.model_validate(json.loads(response))


@router.post(path="/rerank-text",
             name="Rerank Text",
             description="Re-ranks text given",
             response_model=cross_encode_schemas.CrossEncodeResponse
             )
async def route_cross_encode_text(request: cross_encode_schemas.CrossEncodeRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="rerank_text",
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

    return cross_encode_schemas.CrossEncodeResponse.model_validate(json.loads(response))


@router.post(path="/get-presigned-url-upload",
             name="Get Presigned URL Upload",
             description="Gets a presigned URL for uploading",
             response_model=presigned_url_schemas.PresignedURLUploadResponse
             )
async def route_get_presigned_url_upload(request: presigned_url_schemas.PresignedURLUploadRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="generate_presigned_url_upload",
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

    return presigned_url_schemas.PresignedURLUploadResponse.model_validate(json.loads(response))


@router.post(path="/retrieve-closest-entries",
             name="Retrieve Closest Entries",
             description="Retrieves closest entries",
             response_model=retrieve_closest_entries_schemas.RetrieveClosestEntriesResponse
             )
async def route_retrieve_closest_entries(request: retrieve_closest_entries_schemas.RetrieveClosestEntriesRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="retrieve_closest_entries",
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

    return retrieve_closest_entries_schemas.RetrieveClosestEntriesResponse.model_validate(json.loads(response))

