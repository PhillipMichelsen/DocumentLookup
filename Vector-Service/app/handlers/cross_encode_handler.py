import json

from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.job_schemas import JobRequest, JobResponse
from app.schemas.jobs.cross_encode_schemas import CrossEncodeRequest, CrossEncodeResponse
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis_utils


def handle_cross_encode(decoded_message_body):
    request = JobRequest(**decoded_message_body)
    job = job_redis_utils.get_job(request.job_id)
    cross_encode_request = CrossEncodeRequest.model_validate(json.loads(job.content))

    sentence_score_pairs = generate_cross_encoding(cross_encode_request.query, cross_encode_request.sentences)
    sentences_ranked, scores_ranked = rerank(sentence_score_pairs)

    cross_encode_response = CrossEncodeResponse(sentences=sentences_ranked, scores=scores_ranked)

    job_redis_utils.update_job_attribute(job.job_id, "content", json.dumps(cross_encode_response.model_dump()))
    job_redis_utils.update_job_attribute(job.job_id, "status", "COMPLETED")

    job_response = JobResponse(job_id=request.job_id)
    job_response = json.dumps(job_response.model_dump())

    pika_utils.publish_response(
        message=job_response.encode()
    )
