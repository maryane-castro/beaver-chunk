from abc import ABC, abstractmethod


class ABC_Embedding(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_embeddings_for_documents():
        pass

    @abstractmethod
    def get_embeddings_for_query():
        pass
