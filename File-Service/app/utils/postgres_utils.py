from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.models.files import File, Base, FileSchema


class PostgresUtils:
    def __init__(self):
        self.engine = None
        self.Session = None

    def init_connection(self, db_url: str):
        self.engine = create_engine(db_url, echo=True)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        Base.metadata.create_all(self.engine)

    def add_file(self, file_data):
        with self.Session() as session:
            file_record = File(**file_data)
            session.add(file_record)
            session.commit()

    def increment_entries_processed(self, document_id, increment_by=1):
        with self.Session() as session:
            file_record = session.query(File).filter_by(document_id=document_id).first()
            if file_record:
                file_record.entries_processed += increment_by
                session.commit()

    def increment_total_entries(self, document_id, increment_by=1):
        with self.Session() as session:
            file_record = session.query(File).filter_by(document_id=document_id).first()
            if file_record:
                file_record.total_entries += increment_by
                session.commit()

    def get_file_by_document_id(self, document_id: str) -> FileSchema:
        with self.Session() as session:
            file_record = session.query(File).filter_by(document_id=document_id).first()
            return FileSchema(
                document_id=file_record.document_id,
                original_file_name=file_record.original_file_name,
                user_id=file_record.user_id,
                total_entries=file_record.total_entries,
                entries_processed=file_record.entries_processed,
            )

    def get_all_document_ids(self) -> List[str]:
        with self.Session() as session:
            document_ids = session.query(File.document_id).all()
            return [doc_id[0] for doc_id in document_ids]


class FileTableUtils:
    @staticmethod
    def determine_processing_status(total_entries: int, entries_processed: int) -> str:
        if total_entries == 0 and entries_processed == 0:
            return "Parsing..."
        elif total_entries == entries_processed:
            return "Processed!"
        elif total_entries > entries_processed:
            progress = (entries_processed / total_entries) * 100
            return f"Embedding: {progress:.2f}% done"
        else:
            return f"Unknown! Total entries: {total_entries}, Entries processed: {entries_processed}"


postgres_utils = PostgresUtils()
file_table_utils = FileTableUtils()
