from langchain_community.document_loaders.text import TextLoader
from src.document_loaders.abstract_document_loaders import ABC_DocumentLoaders


class TXT_Loader(ABC_DocumentLoaders):
    def __init__(self, path_document):
        self.txt_loader = TextLoader(path_document)

    def get_documents(self):
        document = self.txt_loader.load()
        return document
