from langchain_community.document_loaders.pdf import PyPDFLoader
from src.document_loaders.abstract_document_loaders import ABC_DocumentLoaders

from src.utils.pos_processor.for_document_loader import process_PDF


class PDF_Loader(ABC_DocumentLoaders):
    def __init__(self, path_document):
        self.txt_loader = PyPDFLoader(file_path=path_document)

    def get_documents(self):
        document = self.txt_loader.load()
        pos_process_document = process_PDF(document)
        return pos_process_document
