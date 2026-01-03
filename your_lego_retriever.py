from src.factory import get_embedding, get_vector_store


# CREATE EMBEDDINGS
Embedding = get_embedding(
    name="huggingface", model_name="BAAI/bge-small-en"
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
retriever = instance_vector_store.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)

question = "What was the non-GAAP operating efficiency ratio for SVB Financial in 2016?"
docs = retriever.invoke(question)
print("Pergunta:", question)
n = 1
for i in docs:
    print(f"{n} - DOC")
    print(i)
    n += 1



