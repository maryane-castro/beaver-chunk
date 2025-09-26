from src.embedding.abstract_embedding import ABC_Embedding
from langchain_huggingface import HuggingFaceEmbeddings


class HuggingFace(ABC_Embedding):
    def __init__(self, model_name):
        self.model_name = model_name
        self.embedding = HuggingFaceEmbeddings(model_name=self.model_name)

    def get_embeddings_for_documents(self, documents):
        if documents and hasattr(documents[0], "page_content"):
            texts = [doc.page_content for doc in documents]
        else:
            texts = documents

        return self.embedding.embed_documents(texts)

    def get_embeddings_for_query(self, query):
        return self.embedding.embed_query(query)

    def get_instance_for_vector_store(self):
        return self.embedding
