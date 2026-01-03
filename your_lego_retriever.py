from src.factory import get_embedding, get_vector_store
from src.llm.configure_provider import LLM
from dotenv import load_dotenv
import os

load_dotenv()

# CREATE EMBEDDINGS
Embedding = get_embedding(name="huggingface", model_name="BAAI/bge-large-en")
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
    search_type="similarity", search_kwargs={"k": 5}
)

question = "What was the non-GAAP operating efficiency ratio for SVB Financial in 2016?"
docs = retriever.invoke(question)
print("Pergunta:", question)
n = 1
for i in docs:
    print(f"{n} - DOC")
    print(i)
    n += 1


llm = LLM(base_url=os.getenv("GROQ_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))


response = llm.generate_response(user_input=question, docs_retriever=docs)
print("\n\n\n", response)
