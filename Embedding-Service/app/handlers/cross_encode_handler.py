from pydantic import ValidationError
from typing import Any
from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.jobs.cross_encode_schemas import CrossEncodeRequest, CrossEncodeResponse


def handle_cross_encode(decoded_payload: Any) -> CrossEncodeResponse:
    """Handle cross-encoding request from `on_message_rerank` in `cross_encode_listener`.

    Passes decoded payload through schema and sends to `generate_cross_encoding` in `cross_encode_module`.

    :param decoded_payload: Decoded payload from the request
    :return: Cross-encoding response
    """
    try:
        request = CrossEncodeRequest.parse_obj(decoded_payload)

        sentence_score_pairs = generate_cross_encoding(request.query, request.sentences)
        sentences_ranked, scores_ranked = rerank(sentence_score_pairs)

        response = CrossEncodeResponse(sentences=sentences_ranked, scores=scores_ranked)

    except ValidationError as e:
        response = CrossEncodeResponse(error=str(e))

    return response
