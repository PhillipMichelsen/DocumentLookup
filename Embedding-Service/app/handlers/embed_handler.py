from pydantic import ValidationError
from typing import Any
from app.modules.embed_module import generate_embedding
from app.schemas.embed_schema import EmbedRequest, EmbedResponse


def handle_embed(decoded_payload: Any) -> EmbedResponse:
    """Handles embedding request from `on_message_embed` in `embed_listener`.

    Passes decoded payload through schema and sends to `generate_embedding` in `embed_module`.

    :param decoded_payload: Decoded payload from the request
    :return: Embedding response

    :raises ValidationError: If the payload is invalid
    """
    try:
        request = EmbedRequest.parse_obj(decoded_payload)
        embedding = generate_embedding(request.sentences)
        response = EmbedResponse(embedding=embedding)

    except ValidationError as e:
        response = EmbedResponse(error=str(e))

    return response
