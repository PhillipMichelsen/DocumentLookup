import json

from fastapi import APIRouter

from app.config import exchanges_routing
from app.schemas.file_service_schema import UploadFileRequest, UploadFileResponse
from app.utils.pika_utils import pika_handler
from app.utils.task_utils import task_utils

router = APIRouter()


@router.post(path="/upload-file",
             name="Upload file",
             description="Upload and process file",
             response_model=UploadFileResponse
             )
async def route_upload_file(request: UploadFileRequest):
    task_utils.start_new_task('upload_file', request.dict())




    #return UploadFileResponse(**response)
