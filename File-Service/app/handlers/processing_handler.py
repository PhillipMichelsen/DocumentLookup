from pydantic import ValidationError
import httpx

from app.modules.processing_module import grobid_fulltext_pdf, parse_grobid_output
from app.schemas.processing_schemas import ProcessFileRequest
from app.utils.pika_helper import pika_helper


def handle_process_file(raw_payload: dict):
    request = ProcessFileRequest(**raw_payload)

    processed_document = grobid_fulltext_pdf(presigned_url_download=request.presigned_url)

    paragraphs, sentences = parse_grobid_output(processed_document)

    paragraph_vectors = pika_helper.send_message('file_queue_embed_embedding', 'embed_embedding', {'sentences': paragraphs})
    sentences_vectors = pika_helper.send_message('file_queue_embed_embedding', 'embed_embedding', {'sentences': sentences})

    paragraphs_vectors = httpx.post(url=service_endpoints.embed_embedding, json={'sentences': paragraphs}).json()
    sentence_vectors = httpx.post(url=service_endpoints.embed_embedding, json={'sentences': sentences}).json()


