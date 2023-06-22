from pydantic import ValidationError

from app.modules.cross_encode_module import rerank
from app.schemas.cross_encode_schema import CrossEncodeRequest, CrossEncodeResponse


def handle_cross_encode(raw_payload: dict):
    try:
        request = CrossEncodeRequest(**raw_payload)
        sentences, scores = rerank(request.query, request.sentences)
        response = CrossEncodeResponse(sentences=sentences, scores=scores)

    except ValidationError as e:
        response = CrossEncodeResponse(error=str(e))

    return response
