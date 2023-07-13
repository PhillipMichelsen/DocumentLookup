from typing import Optional

from pydantic import BaseModel


class JobsSchema(BaseModel):
    name: str
    type: str
    exchange: Optional[str]
    routing_key: Optional[str]