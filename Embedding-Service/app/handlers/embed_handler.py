from pydantic import ValidationError

from app.modules.embed_module import generate_embedding
from app.schemas.embed_schema import EmbedRequest, EmbedResponse


def handle_embed(raw_payload: dict):
    try:
        request = EmbedRequest(**raw_payload)
        embedding = generate_embedding(request.sentences)
        response = EmbedResponse(embedding=embedding)

    except ValidationError as e:
        response = EmbedResponse(error=str(e))

    return response
