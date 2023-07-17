import json

from app.modules.embed_module import generate_embeddings
from app.schemas.job_schemas import JobRequest, JobResponse
from app.schemas.jobs.embed_schemas import EmbedRequest, EmbedResponse
from app.utils.pika_utils import pika_utils
from app.utils.redis_utils import job_redis_utils


def handle_embed(decoded_message_body):
    request = JobRequest(**decoded_message_body)
    job = job_redis_utils.get_job(request.job_id)
    embed_request = EmbedRequest.model_validate(json.loads(job.content))

    embeddings = generate_embeddings(embed_request.sentences)

    embed_response = EmbedResponse(embedding=embeddings)

    job_redis_utils.update_job_attribute(job.job_id, "content", json.dumps(embed_response.model_dump()))
    job_redis_utils.update_job_attribute(job.job_id, "status", "COMPLETED")

    job_response = JobResponse(job_id=request.job_id)
    job_response = json.dumps(job_response.model_dump())

    pika_utils.publish_response(
        message=job_response.encode()
    )
