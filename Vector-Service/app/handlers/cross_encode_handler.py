import json

from app.config import settings
from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.task_schemas import TaskRequest, TaskResponse
from app.schemas.service_tasks.cross_encode_schemas import CrossEncodeRequest, CrossEncodeResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_cross_encode(decoded_message_body):
    task_request = TaskRequest.model_validate(decoded_message_body)
    job_data = json.loads(task_request.job_data)
    cross_encode_request = CrossEncodeRequest.model_validate(job_data)

    entries_score_pairs = generate_cross_encoding(cross_encode_request.query, cross_encode_request.entries)
    entries_ranked, scores_ranked = rerank(entries_score_pairs)

    cross_encode_response = CrossEncodeResponse(ranked_entries=entries_ranked, ranked_scores=scores_ranked)

    job_data.update(cross_encode_response.model_dump())
    response_hold.stash_job_data(task_request.task_id, job_data)

    task_response = TaskResponse(
        task_id=task_request.task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(task_response.model_dump())
    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_response_routing_key,
        message=message.encode('utf-8')
    )
