from src.factory import get_embedding, get_vector_store
from src.llm.configure_provider import LLM
from dotenv import load_dotenv
import os
import pandas as pd

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


# RETRIEVER
instance_vector_store = Vector_Store.get_instance_vector_store()
retriever = instance_vector_store.as_retriever(
    search_type="similarity", search_kwargs={"k": 5}
)

# LLM
llm = LLM(base_url=os.getenv("GROQ_BASE_URL"), api_key=os.getenv("GROQ_API_KEY"))

# Ler o arquivo metadata.csv
df = pd.read_csv("./data/metadata.csv")

# Criar coluna para armazenar as respostas da LLM
df["answer_llm"] = ""

# Processar cada query
for idx, row in df.iterrows():
    question = row["query"]
    print(f"\n{'='*80}")
    print(f"Processando query {idx + 1}/{len(df)}")
    print(f"Pergunta: {question}")
    print(f"{'='*80}")

    # Recuperar documentos
    docs = retriever.invoke(question)

    # Gerar resposta com LLM
    response = llm.generate_response(user_input=question, docs_retriever=docs)

    # Salvar resposta no DataFrame
    df.at[idx, "answer_llm"] = response

    print(f"Resposta LLM: {response}")

# Salvar o DataFrame atualizado
df.to_csv("./data/metadata.csv", index=False)
print(f"\n{'='*80}")
print("Processamento concluído! Respostas salvas em ./data/metadata.csv")
print(f"{'='*80}")
