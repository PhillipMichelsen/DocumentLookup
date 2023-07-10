from fastapi import APIRouter
import json
import logging

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
    logging.info(f"[!] Received new request...")
    headers, return_future = await task_helper.create_task("test-embed", json.dumps(request.dict()))
    message = json.dumps({"task_id": headers["task_id"]})

    await pika_helper.publish_message(
        exchange_name="gateway_exchange",
        routing_key=".job",
        headers=headers,
        message=message.encode('utf-8')
    )

    response = await return_future
    response = json.loads(response)
    logging.info(f"[*] Returning response to user...")

    return test_embedding.TaskTestEmbedResponse(**response)
