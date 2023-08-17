import json

from fastapi import APIRouter

from app.schemas.utility_tasks import embed_schemas, cross_encode_schemas, presigned_url_schemas, \
    retrieve_closest_entries_schemas
from app.utils.service_utils import job_request_response

router = APIRouter()


@router.post(path="/embed-text",
             name="Embed Text",
             description="Embeds text given",
             response_model=embed_schemas.EmbedResponse
             )
async def route_embed_text(request: embed_schemas.EmbedRequest):
    response = await job_request_response(request, "embed_text")
    return embed_schemas.EmbedResponse.model_validate(json.loads(response))


@router.post(path="/rerank-text",
             name="Rerank Text",
             description="Re-ranks text given",
             response_model=cross_encode_schemas.CrossEncodeResponse
             )
async def route_cross_encode_text(request: cross_encode_schemas.CrossEncodeRequest):
    response = await job_request_response(request, "rerank_text")
    return cross_encode_schemas.CrossEncodeResponse.model_validate(json.loads(response))


@router.post(path="/generate-presigned-url-upload",
             name="Generate Presigned URL Upload",
             description="Generates a presigned URL for uploading",
             response_model=presigned_url_schemas.PresignedURLUploadResponse
             )
async def route_generate_presigned_url_upload(request: presigned_url_schemas.PresignedURLUploadRequest):
    response = await job_request_response(request, "generate_presigned_url_upload")
    return presigned_url_schemas.PresignedURLUploadResponse.model_validate(json.loads(response))


@router.post(path="/retrieve-closest-entries",
             name="Retrieve Closest Entries",
             description="Retrieves closest entries",
             response_model=retrieve_closest_entries_schemas.RetrieveClosestEntriesResponse
             )
async def route_retrieve_closest_entries(request: retrieve_closest_entries_schemas.RetrieveClosestEntriesRequest):
    response = await job_request_response(request, "retrieve_closest_entries")
    return retrieve_closest_entries_schemas.RetrieveClosestEntriesResponse.model_validate(json.loads(response))
