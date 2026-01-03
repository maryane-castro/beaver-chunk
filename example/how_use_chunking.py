from src.factory import get_document_loader, get_chunker


document_loader = get_document_loader(
    name="txt", path_document="data/mock/description.txt"
)
docs = document_loader.get_documents()

chunking = get_chunker("character", chunk_size=500, chunk_overlap=0)
chunks = chunking.split_document(docs)  # passe os seus documentos

chunking.get_kwargs()  # verificar argumentos que estao disponiveis


### outra forma

chunking = get_chunker("recursive", language="markdown")
chunks = chunking.split_document(docs)
chunking.get_kwargs()
