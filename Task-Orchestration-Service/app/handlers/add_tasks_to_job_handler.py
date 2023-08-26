from app.schemas.job_schemas import AddTasksToJobRequest, AddTasksToJobResponse
from app.utils.job_utils import job_utils
from app.utils.redis_utils import job_redis, task_redis
from app.utils.task_utils import task_utils


def handle_add_tasks_to_job(decoded_message_body):
    add_tasks_to_job_request = AddTasksToJobRequest.model_validate(decoded_message_body)
    job = job_redis.get_stored_job(add_tasks_to_job_request.job_id)
    requesting_task_index = job.task_chain.split(',').index(add_tasks_to_job_request.requesting_task_id)
    print("Before adding tasks", flush=True)
    print(job.task_chain, flush=True)

    for task_name in add_tasks_to_job_request.task_names:
        task_id = task_utils.create_task(task_name, job.job_id)
        job_utils.insert_task_into_task_chain(job, task_id, requesting_task_index + 1)
        print(f"Added task_id {task_id}", flush=True)
        requesting_task_index += 1

    print("Added tasks to job", flush=True)
    print(job.task_chain, flush=True)
