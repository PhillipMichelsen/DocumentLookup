from app.schemas.job_schemas import JobResponse
from app.utils.redis_utils import job_redis, task_redis
from app.utils.job_utils import job_utils
from app.utils.task_utils import task_utils


def handle_job(decoded_message_body):
    job_response = JobResponse(**decoded_message_body)

    job = job_redis.get_job(job_response.job_id)
    next_job = task_utils.step_job_chain(job_response.job_id)

    job_utils.execute_job(next_job)




