from src.chunking.abstract_chunking import ABC_Chunking

from langchain_experimental.text_splitter import SemanticChunker
from langchain_huggingface import HuggingFaceEmbeddings


class Semantic(ABC_Chunking):
    def __init__(self, embeddings):
        self.splitter = SemanticChunker(
            embeddings = HuggingFaceEmbeddings(model_name=embeddings)
        )

    def split_document(self, documents):
        chunks = self.splitter.split_documents(documents)
        for chunk in chunks:
            chunk.page_content = self.remove_irrelevant_characters(chunk.page_content)
            
        return chunks