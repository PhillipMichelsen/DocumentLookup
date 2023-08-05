import json
import uuid

from fastapi import APIRouter

from app.config import settings
from app.schemas.core_tasks import embed_text_schemas, rerank_text_schemas
from app.schemas.job_schemas import JobRequest
from app.utils.pika_utils import pika_utils
from app.utils.response_utils import response_utils

router = APIRouter()


@router.post(path="/embed-text",
             name="Embed Text",
             description="Embeds text given",
             response_model=embed_text_schemas.TaskEmbedTextResponse
             )
async def route_upload_file(request: embed_text_schemas.TaskEmbedTextRequest):
    job_id = str(uuid.uuid4())

    job = JobRequest(
        job_name="embed_text",
        requesting_service_id=pika_utils.service_id,
        job_id=job_id,
        initial_request_content=json.dumps(request.model_dump())
    )

    response_future = await response_utils.create_response(job_id)

    message = json.dumps(job.model_dump())

    await pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_job_request_routing_key,
        message=message.encode('utf-8')
    )

    response = await response_future

    return embed_text_schemas.TaskEmbedTextResponse.model_validate(json.loads(response))


@router.post(path="/rerank-text",
             name="Rerank Text",
             description="Re-ranks text given",
             response_model=rerank_text_schemas.TaskRerankTextResponse
             )
async def route_upload_file(request: rerank_text_schemas.TaskRerankTextRequest):
    # TODO: Need to fix this bullshit
    task_id = str(uuid.uuid4())

    task = TaskRequest(
        task_name="rerank_text",
        api_gateway_id=pika_helper.service_id,
        task_id=task_id,
        initial_request=json.dumps(request.model_dump())
    )

    response_future = await response_utils.create_response(task_id)

    task = json.dumps(task.model_dump())

    await pika_helper.publish_task(message=task.encode('utf-8'))

    response = await response_future

    return rerank_text_schemas.TaskRerankTextResponse.model_validate(json.loads(response))
