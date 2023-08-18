from pydantic import BaseModel
from typing import List
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String)
    original_file_name = Column(String)
    user_id = Column(String)
    total_entries = Column(Integer)
    weaviate_uuids = Column(ARRAY(String))


class FileSchema(BaseModel):
    document_id: str
    original_file_name: str
    user_id: str
    total_entries: int
    weaviate_uuids: List[str]
