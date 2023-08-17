from app.schemas.task_schemas import TaskClearDataRequest
from app.utils.response_hold_utils import response_hold


def handle_clear_job_data(decoded_message_body):
    task_clear_data_request = TaskClearDataRequest.model_validate(decoded_message_body)
    response_hold.clear_job_data(task_clear_data_request.task_id)
