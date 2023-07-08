import json

from app.utils.pika_async_utils import pika_helper
from app.utils.task_utils import task_helper, task_redis


async def handle_response(message, headers):
    print(f"Received response for task {headers['task_id']}... Message {message}", flush=True)
    task_id = headers["task_id"]
    await task_redis.update_job_data(task_id, message)

    await task_helper.step_next_job(task_id)
    job_message = json.dumps({"task_id": task_id})

    await pika_helper.publish_message(
        exchange_name="gateway_exchange",
        routing_key=".job",
        headers=headers,
        message=job_message.encode('utf-8')
    )
