import json
import logging

from fastapi import APIRouter

from app.schemas.core_tasks import embed_text
from app.utils.pika_async_utils import pika_helper
from app.utils.task_utils import task_helper

router = APIRouter()


@router.post(path="/embed-text",
             name="Embed Text",
             description="Embeds text given",
             response_model=embed_text.TaskEmbedTextResponse
             )
async def route_upload_file(request: embed_text.TaskEmbedTextRequest):
    logging.info(f"[!] Received new request...")
    headers, return_future = await task_helper.create_task("embed_text", json.dumps(request.dict()))
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

    return embed_text.TaskEmbedTextResponse(**response)
