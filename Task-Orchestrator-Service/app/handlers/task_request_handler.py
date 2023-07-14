from app.schemas.task_schemas import TaskRequest
from app.utils.task_utils import task_utils
from app.utils.job_utils import job_utils


def handle_task(decoded_message_body, message_headers):
    task_request = TaskRequest(**decoded_message_body)

    task = task_utils.create_task(
        task_name=task_request.task_name,
        task_id=task_request.task_id,
        api_gateway_id=message_headers['api_gateway_id'],
        initial_request=task_request.initial_request
    )

    job_utils.execute_job(task.job_chain.split(',')[task.current_job_index])


