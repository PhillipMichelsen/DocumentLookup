import json

from app.config import settings
from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.task_schemas import TaskRequest, TaskRouteRequest
from app.schemas.tasks.cross_encode_schemas import CrossEncodeRequest, CrossEncodeResponse
from app.utils.pika_utils import pika_utils
from app.utils.response_hold_utils import response_hold


def handle_cross_encode(decoded_message_body):
    request = TaskRequest.model_validate(decoded_message_body)
    cross_encode_request = CrossEncodeRequest.model_validate(json.loads(request.content))

    sentence_score_pairs = generate_cross_encoding(cross_encode_request.query, cross_encode_request.sentences)
    sentences_ranked, scores_ranked = rerank(sentence_score_pairs)

    cross_encode_response = CrossEncodeResponse(sentences=sentences_ranked, scores=scores_ranked)

    response_hold.stash_response(request.task_id, cross_encode_response)

    route_request = TaskRouteRequest(
        task_id=request.task_id,
        service_id=pika_utils.service_id,
        status='COMPLETED'
    )

    message = json.dumps(route_request.model_dump())

    pika_utils.publish_message(
        exchange_name=settings.task_orchestrator_exchange,
        routing_key=settings.task_orchestrator_task_response_routing_key,
        message=message.encode()
    )
