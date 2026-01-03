from src.factory import (
    get_document_loader,
    get_chunker,
    get_embedding,
    get_vector_store,
)


# CREATE DOCUMENT LOADER
Document_Loader = get_document_loader(
    name="txt", path_document="data/mock/description.txt"
)
docs = Document_Loader.get_documents()

# CREATE CHUNKING
Chunking = get_chunker(name="character", chunk_size=500, chunk_overlap=0)
chunks = Chunking.split_document(docs)

# CREATE EMBEDDINGS
Embedding = get_embedding(
    name="huggingface", model_name="sentence-transformers/all-MiniLM-L6-v2"
)
embedding_instance = Embedding.get_instance_for_vector_store()


# CREATE VECTOR STORE
Vector_Store = get_vector_store(
    name="chroma",
    collection_name="my_collection",
    embeddings=embedding_instance,
    persist_directory="./data/chroma_langchain_db",
)

# indexing
Vector_Store.add(chunks)
