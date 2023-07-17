from app.utils.response_utils import response_utils
from app.schemas.task_request import TaskResponse


async def handle_response(decoded_message_body):
    response = TaskResponse(**decoded_message_body)
    await response_utils.update_response(response.task_id, response.content)
