import json

from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.service_tasks.cross_encode_schemas import CrossEncodeRequest, CrossEncodeResponse
from app.schemas.task_schemas import TaskRequest
from app.utils.service_utils import send_handler_messages


def handle_cross_encode(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    cross_encode_request = CrossEncodeRequest.model_validate(job_data)

    entries_score_pairs = generate_cross_encoding(cross_encode_request.query, cross_encode_request.entries)
    entries_ranked, scores_ranked = rerank(entries_score_pairs)

    cross_encode_response = CrossEncodeResponse(ranked_entries=entries_ranked, ranked_scores=scores_ranked)

    send_handler_messages(task_request.task_id, job_data, cross_encode_response)
