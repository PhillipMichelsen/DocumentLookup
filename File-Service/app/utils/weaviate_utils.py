import weaviate
from typing import List

class WeaviateUtils:
    def __init__(self):
        self.class_name = "Text"
        self.client: weaviate.Client = None

    def init_connection(self, host: str, port: int) -> None:
        self.client = weaviate.Client(f'http://{host}:{port}')

        class_object = {
            "class": self.class_name,
            "description": "Text class, stores paragraphs or sentences and their embeddings",
            "properties": [
                {
                    "name": "text",
                    "description": "The text itself",
                    "dataType": ["text"]
                },
                {
                    "name": "type",
                    "description": "The type of the text, either div or paragraph",
                    "dataType": ["text"]
                },
                {
                    "name": "documentID",
                    "description": "The ID of the document the text belongs to",
                    "dataType": ["text"]
                }
            ]
        }

        if not self.client.schema.contains():
            self.client.schema.create_class(class_object)

    def add_entry(self, text: str, text_type: str, document_id: str):
        """
        Add an entry to Weaviate.

        :param text: Text content.
        :param text_type: Type of the text (paragraph, sentence).
        :param document_id: UUID of the document in Minio.
        """
        obj = {
            "text": text,
            "type": text_type,
            "documentID": document_id,
        }
        return self.client.data_object.create(data_object=obj, class_name=self.class_name)

    def batch_add_entries(self, text: List[str], text_type: str, document_id: str) -> List[str]:
        """
        Add an entry to Weaviate.

        :param text: Text content.
        :param text_type: Type of the text (paragraph, sentence).
        :param document_id: UUID of the document in Minio.
        """
        data_objects = []
        uuids = []
        for t in text:
            data_objects.append({
                "text": t,
                "type": text_type,
                "documentID": document_id,
            })

        with self.client.batch(
            batch_size=15
        ) as batch:
            for data_object in data_objects:
                uuids.append(batch.add_data_object(data_object=data_object, class_name=self.class_name))

        return uuids

    def retrieve_count_by_document_id(self, document_id: str):
        query = (
            self.client.query
            .aggregate("Text")
            .with_where({
                "path": ["documentID"],
                "operator": "Equal",
                "valueString": document_id
            })
            .with_meta_count()
        )

        response = query.do()

        return response['data']['Aggregate']['Text'][0]['meta']['count']

    def retrieve_closest_entries(self, query: str, top_n: int, type_filter: str, document_id: str):
        query = (
            self.client.query
            .get("Text", ["text"])
            .with_near_text({
                "concepts": [query],
            })
            .with_limit(top_n)
            .with_where({
                "path": ["type"],
                "operator": "Equal",
                "valueText": type_filter
            })
        )

        """
        if document_id:
            query = query.with_where([
                {
                    "path": ["documentID"],
                    "operator": "Equal",
                    "valueString": document_id
                },
                {
                    "path": ["type"],
                    "operator": "Equal",
                    "valueText": type_filter
                }
            ])
        """

        response = query.do()

        return response

    def delete_entry(self, entry_uuid):
        """
        Delete an entry from Weaviate by UUID.

        :param entry_uuid: UUID of the entry.
        """
        return self.client.data_object.delete(uuid=entry_uuid, class_name=self.class_name)


weaviate_utils = WeaviateUtils()
