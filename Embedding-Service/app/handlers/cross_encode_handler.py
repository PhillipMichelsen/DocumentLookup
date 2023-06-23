from pydantic import ValidationError

from app.modules.cross_encode_module import rerank, generate_cross_encoding
from app.schemas.cross_encode_schema import CrossEncodeRequest, CrossEncodeResponse


def handle_cross_encode(raw_payload: dict) -> CrossEncodeResponse:
    """Handle cross-encoding request from `on_message_rerank` in `cross_encode_listener`.

    Passes decoded payload through schema and sends to `generate_cross_encoding` in `cross_encode_module`.

    :param raw_payload: Decoded payload from the request
    :return: Cross-encoding response
    """
    try:
        request = CrossEncodeRequest(**raw_payload)
        sentence_score_pairs = generate_cross_encoding(request.query, request.sentences)
        sentences_ranked, scores_ranked = rerank(sentence_score_pairs)
        response = CrossEncodeResponse(sentences=sentences_ranked, scores=scores_ranked)

    except ValidationError as e:
        response = CrossEncodeResponse(error=str(e))

    return response
