import json

from fastapi import APIRouter

from app.schemas.core_tasks import answer_question_schemas, get_files_schemas, generate_presigned_url_upload_schemas
from app.utils.service_utils import job_request_response

router = APIRouter()


@router.post(path='/answer-question',
             name='Answer Question',
             description='Answer a question based on the given context',
             response_model=answer_question_schemas.AnswerQuestionResponse)
async def route_answer_question(request: answer_question_schemas.AnswerQuestionRequest):
    response = await job_request_response(request, "answer_question")
    return answer_question_schemas.AnswerQuestionResponse.model_validate(json.loads(response))


@router.post(path='/generate-presigned-url-upload',
             name='Generate Presigned URL Upload',
             description='Generates a presigned url for uploading a file to Minio',
             response_model=generate_presigned_url_upload_schemas.GeneratePresignedURLUploadResponse)
async def route_answer_question(request: generate_presigned_url_upload_schemas.GeneratePresignedURLUploadRequest):
    response = await job_request_response(request, "generate_presigned_url_upload")
    return generate_presigned_url_upload_schemas.GeneratePresignedURLUploadResponse.model_validate(json.loads(response))


@router.post(path='/get-files',
             name='Get Files',
             description='Get information about files',
             response_model=get_files_schemas.GetFilesResponse)
async def route_answer_question(request: get_files_schemas.GetFilesRequest):
    response = await job_request_response(request, "get_files")
    return get_files_schemas.GetFilesResponse.model_validate(json.loads(response))


