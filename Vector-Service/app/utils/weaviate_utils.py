import weaviate


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
                    "description": "The type of the text, either paragraph or sentence",
                    "dataType": ["text"]
                },
                {
                    "name": "documentID",
                    "description": "The ID of the document the text belongs to",
                    "dataType": ["text"]
                }
            ],
            "vectorizer": "none"
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

    def add_vector_to_entry(self, entry_uuid, vector):
        """
        Update an entry in Weaviate by adding or updating a vector.

        :param entry_uuid: UUID of the entry.
        :param vector: Vector to add or update.
        """
        return self.client.data_object.update(data_object={}, class_name=self.class_name, uuid=entry_uuid,
                                              vector=vector)

    def retrieve_closest_entries(self, vector, top_n, type_filter, document_id):
        query = (
            self.client.query
            .get("Text", ["text"])
            .with_near_vector({
                "vector": vector
            })
            .with_limit(top_n)
            .with_where({
                "path": ["type"],
                "operator": "Equal",
                "valueText": type_filter
            })
        )

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

        response = query.do()

        return response

    def delete_entry(self, entry_uuid):
        """
        Delete an entry from Weaviate by UUID.

        :param entry_uuid: UUID of the entry.
        """
        return self.client.data_object.delete(uuid=entry_uuid, class_name=self.class_name)


weaviate_utils = WeaviateUtils()
