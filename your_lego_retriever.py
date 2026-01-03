from src.factory import get_embedding, get_vector_store


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


# retriver
instance_vector_store = Vector_Store.get_instance_vector_store()
retriever = instance_vector_store.as_retriever()
docs = retriever.invoke("what did the president say about ketanji brown jackson?")
print(docs)
