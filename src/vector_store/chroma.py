from src.vector_store.abstract_vector_store import Vector_Store
from langchain_chroma import Chroma
from uuid import uuid4


class Chroma_Store(Vector_Store):
    def __init__(
        self, collection_name, embeddings, persist_directory="./chroma_langchain_db"
    ):
        self.collection_name = collection_name
        self.embeddings = embeddings
        self.persist_directory = persist_directory

        self.vector_store = Chroma(
            collection_name=self.collection_name,
            embedding_function=self.embeddings,
            persist_directory=self.persist_directory,
        )

    def add(self, documents):
        uuids = [str(uuid4()) for _ in range(len(documents))]
        self.vector_store.add_documents(documents=documents, ids=uuids)

    def update(self):
        pass

    def get_instance_vector_store(self):
        return self.vector_store
