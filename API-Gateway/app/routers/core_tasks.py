from fastapi import APIRouter
import json

from app.schemas.core_tasks import test_embedding
from app.utils.task_utils import task_helper
from app.utils.pika_async_utils import pika_helper

router = APIRouter()


@router.post(path="/test-embed",
             name="Test Embedding",
             description="Tests the embedding task",
             response_model=test_embedding.TaskTestEmbedResponse
             )
async def route_upload_file(request: test_embedding.TaskTestEmbedRequest):
    print("Received request", flush=True)
    headers, return_future = await task_helper.create_task("test-embed", request.dict())
    print("Created task", flush=True)
    await pika_helper.publish_message(
        exchange_name="gateway_exchange",
        routing_key=".job",
        headers=headers,
        message=json.dumps({"task_id": headers["task_id"]}).encode('utf-8')
    )
    print("Published message", flush=True)

    response = await return_future
    print(response, flush=True)
    print(response.done(), flush=True)

    return test_embedding.TaskTestEmbedResponse(**response)
