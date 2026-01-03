from src.factory import (
    get_chunker,
    get_embedding,
    get_vector_store,
)


# CREATE DOCUMENT LOADER
from src.document_loaders.data_preparation import DataPreparation

# Inicializa o DataPreparation
data_prep = DataPreparation(
    repo_id="HuggingFaceTB/SmolVLM-256M-Instruct",
    prompt="Describe the image in three sentences. Be consise and accurate.",
    provider_vlm=None  # Opções: None (default), "local", "remote"
)

docs, errors = data_prep.process_files(
    folder_or_file="data/huggingface_images",  
    format_output="txt"  
)
if errors:
    print(f"Erros encontrados: {errors}")



# CREATE CHUNKING
Chunking = get_chunker(name="character", chunk_size=1024, chunk_overlap=200)
chunks = Chunking.split_document(docs)

# CREATE EMBEDDINGS
Embedding = get_embedding(
    name="huggingface", model_name="BAAI/bge-large-en"
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
