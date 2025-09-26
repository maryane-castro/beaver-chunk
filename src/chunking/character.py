from src.chunking.abstract_chunking import ABC_Chunking
from langchain_text_splitters import CharacterTextSplitter


class Character(ABC_Chunking):
    def __init__(self, **kwargs):
        self.splitter = CharacterTextSplitter(**kwargs)

    def split_document(self, documents):
        chunks = self.splitter.split_documents(documents)
        return chunks
