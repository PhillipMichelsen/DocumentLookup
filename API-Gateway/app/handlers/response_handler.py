import json

from app.utils.pika_async_utils import pika_helper
from app.utils.task_utils import task_helper, task_redis


async def handle_response(message, headers):
    task_id = headers["task_id"]
    await task_redis.update_job_data(task_id, message)

    await task_helper.step_next_job(task_id)
    new_job = await task_redis.get_single_task_detail(task_id, "current_job")

    # if this next job is a return job, we need to set the routing key to the "original_gateway_id" + .job
    # this is because the gateway will be listening for this routing key

    job_message = json.dumps({"task_id": task_id})

    if task_helper.jobs[new_job].type == "return":
        routing_key = f"{headers['original_gateway_id']}.job"
    else:
        routing_key = ".job"

    await pika_helper.publish_message(
        exchange_name="gateway_exchange",
        routing_key=routing_key,
        headers=headers,
        message=job_message.encode('utf-8')
    )
