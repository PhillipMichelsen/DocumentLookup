import json
import time

from app.schemas.service_tasks.chat_completion_schemas import ChatCompletionRequest, ChatCompletionResponse
from app.schemas.task_schemas import TaskRequest
from app.schemas.job_schemas import AddTasksToJobRequest
from app.utils.openai_utils import openai_utils
from app.utils.service_utils import send_handler_messages, send_add_task_to_job_message


def handle_chat_completion(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    chat_completion_request = ChatCompletionRequest.model_validate(job_data)

    if chat_completion_request.messages is None:
        chat_completion_message = openai_utils.form_messages(chat_completion_request.user_query)
    else:
        chat_completion_message = openai_utils.add_messages(chat_completion_request.messages, chat_completion_request.context)

    output, is_query_request = openai_utils.chat_completion(chat_completion_message)

    chat_completion_response = ChatCompletionResponse(messages=chat_completion_message)

    if is_query_request:
        print(f"GPT Requested context, Query: {output}", flush=True)
        send_add_task_to_job_message(task_request.job_id, task_request.task_id, ['retrieve_context', 'chat_completion'])
        chat_completion_response.context_query = output
    else:
        print(f"GPT Generated Response", flush=True)
        chat_completion_response.chat_completion = output

    send_handler_messages(task_request.task_id, job_data, chat_completion_response)
