import weaviate


class WeaviateUtils:
    def __init__(self):
        self.class_name = None
        self.client = None

    def init_connection(self, host: str, port: int) -> None:
        """Initialize connection to Weaviate

        :param host: The host of the Weaviate server
        :param port: The port of the Weaviate server
        :return: None
        """
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
                    "dataType": ["string"]
                },
                {
                    "name": "documentID",
                    "description": "The ID of the document the text belongs to",
                    "dataType": ["string"]
                }
            ],
            "vectorizer": "none"
        }

        self.client.schema.create_class(class_object)

    def add_entry(self, text: str, text_type: str, document_id: str, vector=None):
        """
        Add an entry to Weaviate.

        :param text: Text content.
        :param text_type: Type of the text (paragraph, sentence).
        :param document_id: UUID of the document in Minio.
        :param vector: Vector representation of the text (optional).
        """
        obj = {
            "text": text,
            "type": text_type,
            "documentId": document_id,
        }
        return self.client.data_object.create(obj, self.class_name, vector=vector)

    def update_entry(self, uuid, vector):
        """
        Update an entry in Weaviate by adding or updating a vector.

        :param uuid: UUID of the object.
        :param vector: Vector to add or update.
        """
        return self.client.data_object.update_vector(self.class_name, uuid, vector)

    def delete_entry(self, uuid):
        """
        Delete an entry from Weaviate by UUID.

        :param uuid: UUID of the object.
        """
        return self.client.data_object.delete(self.class_name, uuid)


weaviate_utils = WeaviateUtils()
