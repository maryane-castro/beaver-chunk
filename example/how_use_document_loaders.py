from src.factory import get_document_loader


document_loader = get_document_loader(
    name="txt", path_document="data/mock/description.txt"
)
docs = document_loader.get_documents()
print("TXT: ", docs)

document_loader = get_document_loader(
    name="pdf", path_document="data/mock/description.pdf"
)
docs = document_loader.get_documents()
print("PDF: ", docs)
