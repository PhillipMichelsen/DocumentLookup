import json

from app.modules.embed_module import generate_embeddings
from app.schemas.service_tasks.embed_schemas import EmbedRequest, EmbedResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.service_utils import send_handler_messages


def handle_embed(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    embed_request = EmbedRequest.model_validate(job_data)

    embeddings = generate_embeddings(embed_request.text)

    embed_response = EmbedResponse(embedding=embeddings)

    send_handler_messages(task_request.task_id, job_data, embed_response)
