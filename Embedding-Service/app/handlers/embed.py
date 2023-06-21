from app.schemas.embed import EmbedRequest, EmbedResponse
from app.modules.embedding import generate_embedding
from pydantic import ValidationError


def handle_embed(raw_payload: dict):
    try:
        request = EmbedRequest(**raw_payload)
        embedding = generate_embedding(request.sentences)
        response = EmbedResponse(embedding=embedding)

    except ValidationError as e:
        response = EmbedResponse(error=str(e))

    return response
