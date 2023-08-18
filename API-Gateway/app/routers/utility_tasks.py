import json

from fastapi import APIRouter
from app.schemas.utility_tasks import retrieve_context_schemas
from app.utils.service_utils import job_request_response

router = APIRouter()


@router.post(path='/retrieve-context',
             name='Retrieve Context',
             description='Retrieve context based on the given query',
             response_model=retrieve_context_schemas.RetrieveContextResponse)
async def route_answer_question(request: retrieve_context_schemas.RetrieveContextRequest):
    response = await job_request_response(request, "retrieve_context")
    return retrieve_context_schemas.RetrieveContextResponse.model_validate(json.loads(response))
