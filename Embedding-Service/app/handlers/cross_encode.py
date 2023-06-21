from app.schemas.cross_encode import CrossEncodeRequest, CrossEncodeResponse
from app.modules.cross_encoding import rerank
from pydantic import ValidationError


def handle_cross_encode(raw_payload: dict):
    try:
        request = CrossEncodeRequest(**raw_payload)
        sentences, scores = rerank(request.query, request.sentences)
        response = CrossEncodeResponse(sentences=sentences, scores=scores)

    except ValidationError as e:
        response = CrossEncodeResponse(error=str(e))

    return response
