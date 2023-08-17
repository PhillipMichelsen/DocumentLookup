import json

from fastapi import APIRouter

from app.schemas.core_tasks import embed_store_schemas, retrieve_query_context_schemas, get_files_schemas
from app.utils.service_utils import job_request_response

router = APIRouter()


@router.post(path="/embed-store-text",
             name="Embed Store Text",
             description="Embeds and stores text given",
             response_model=embed_store_schemas.EmbedStoreResponse
             )
async def route_embed_store_text(request: embed_store_schemas.EmbedStoreRequest):
    response = await job_request_response(request, "embed_store_text")
    return embed_store_schemas.EmbedStoreResponse.model_validate(json.loads(response))


@router.post(path="/retrieve-query-context",
             name="Retrieve Query Context",
             description="Searches for the closest entries to the given query",
             response_model=retrieve_query_context_schemas.RetrieveQueryContextResponse
             )
async def route_retrieve_query_context(request: retrieve_query_context_schemas.RetrieveQueryContextRequest):
    response = await job_request_response(request, "retrieve_query_context")
    return retrieve_query_context_schemas.RetrieveQueryContextResponse.model_validate(json.loads(response))


@router.post(path='/get-files',
             name='Get Files',
             description='Get all files stored in the database',
             response_model=get_files_schemas.GetFilesResponse)
async def route_get_files(request: get_files_schemas.GetFilesRequest):
    response = await job_request_response(request, "get_files")
    return get_files_schemas.GetFilesResponse.model_validate(json.loads(response))
