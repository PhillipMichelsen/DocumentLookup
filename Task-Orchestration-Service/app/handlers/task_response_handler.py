import json

from app.schemas.task_schemas import TaskResponse, TaskRouteRequest
from app.utils.job_utils import job_utils
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


def handle_task_response(decoded_message_body):
    task_response = TaskResponse.model_validate(decoded_message_body)

    completed_task = task_redis.get_stored_task(task_response.task_id)

    job_utils.step_up_task_index(completed_task.job_id)
    job = job_redis.get_stored_job(completed_task.job_id)

    new_task = task_redis.get_stored_task(job.task_chain.split(',')[job.current_task_index])
    new_task_attributes = task_utils.tasks[new_task.task_name]

    # TODO: Cleanup this mess, move to task_utils
    if new_task_attributes.task_type == "process":
        route_request = TaskRouteRequest(
            task_id=completed_task.task_id,
            next_task_id=new_task.task_id,
            job_id=job.job_id,
            exchange=new_task_attributes.exchange,
            routing_key=new_task_attributes.routing_key
        )

        message = json.dumps(route_request.model_dump())
        pika_utils.publish_message(
            exchange_name='task_routing_exchange',
            routing_key=task_response.service_id,
            message=message.encode('utf-8')
        )
    elif new_task_attributes.task_type == "return":
        route_request = TaskRouteRequest(
            task_id=completed_task.task_id,
            next_task_id=new_task.task_id,
            job_id=job.job_id,
            exchange='gateway_exchange',
            routing_key=job.requesting_service_id
        )

        message = json.dumps(route_request.model_dump())
        pika_utils.publish_message(
            exchange_name='task_routing_exchange',
            routing_key=task_response.service_id,
            message=message.encode('utf-8')
        )
