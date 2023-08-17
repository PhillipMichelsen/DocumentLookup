from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class File(Base):
    __tablename__ = 'files'

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String)
    original_file_name = Column(String)
    user_id = Column(String)
    total_entries = Column(Integer)
    entries_processed = Column(Integer)


class FileSchema(BaseModel):
    document_id: str
    original_file_name: str
    user_id: str
    total_entries: int
    entries_processed: int
