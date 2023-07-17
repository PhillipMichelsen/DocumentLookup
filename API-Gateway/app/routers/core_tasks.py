import json
import uuid

from fastapi import APIRouter

from app.schemas.core_tasks import embed_text, rerank_text
from app.schemas.task_request import TaskRequest
from app.utils.pika_utils import pika_helper
from app.utils.response_utils import response_utils

from app.config import settings

router = APIRouter()


@router.post(path="/embed-text",
             name="Embed Text",
             description="Embeds text given",
             response_model=embed_text.TaskEmbedTextResponse
             )
async def route_upload_file(request: embed_text.TaskEmbedTextRequest):
    task_id = str(uuid.uuid4())

    task = TaskRequest(
        task_name="embed_text",
        api_gateway_id=pika_helper.service_id,
        task_id=task_id,
        initial_request=json.dumps(request.model_dump())
    )

    response_future = await response_utils.create_response(task_id)

    task = json.dumps(task.model_dump())

    await pika_helper.publish_task(message=task.encode('utf-8'))

    response = await response_future

    return embed_text.TaskEmbedTextResponse.model_validate(json.loads(response))


@router.post(path="/rerank-text",
             name="Rerank Text",
             description="Re-ranks text given",
             response_model=rerank_text.TaskRerankTextResponse
             )
async def route_upload_file(request: rerank_text.TaskRerankTextRequest):
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

    return rerank_text.TaskRerankTextResponse.model_validate(json.loads(response))
