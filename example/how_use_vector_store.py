from src.factory import (
    get_document_loader,
    get_chunker,
    get_embedding,
    get_vector_store,
)


# carrega os documentos
document_loader = get_document_loader(
    name="txt", path_document="data/mock/description.txt"
)
docs = document_loader.get_documents()

# divide em chunks
chunking = get_chunker(name="character", chunk_size=500, chunk_overlap=0)
chunks = chunking.split_document(docs)


# carrega os embeddings
embedding = get_embedding(
    name="huggingface", model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# embeda os chunks diretamente
embeddings = embedding.get_embeddings_for_documents(chunks)

# pega apenas a instancia para passar no banco
embedding_instance = embedding.get_instance_for_vector_store()


# pode passar o embedding no vector store
vector_store = get_vector_store(
    name="chroma",
    collection_name="my_collection",
    embeddings=embedding_instance,
    persist_directory="./chroma_langchain_db",
)

vector_store.add(chunks)  # indexa no banco
