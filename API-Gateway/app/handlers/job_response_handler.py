from app.utils.response_utils import response_utils
from app.schemas.job_schemas import JobResponse


async def handle_job_response(decoded_message_body):
    response = JobResponse.model_validate(decoded_message_body)
    await response_utils.update_response(response.job_id, response.return_content)
