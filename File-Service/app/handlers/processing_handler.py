from pydantic import ValidationError
import httpx

from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.schemas.processing_schemas import ProcessFileRequest
from app.config import service_endpoints


def handle_process_file(raw_payload: dict):
    request = ProcessFileRequest(**raw_payload)

    processed_document = grobid_fulltext_pdf(presigned_url_download=request.presigned_url)

    paragraphs, sentences = parse_grobid_output(processed_document)

    paragraphs_vectors = httpx.post(url=service_endpoints.embed_embedding, json={'sentences': paragraphs}).json()
    sentence_vectors = httpx.post(url=service_endpoints.embed_embedding, json={'sentences': sentences}).json()


