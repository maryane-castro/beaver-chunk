from src.evaluator.deep_eval import DeepEval
import pandas as pd


deep_eval = DeepEval()

# Ler o arquivo metadata.csv
df = pd.read_csv("./data/metadata.csv")

# Lista para armazenar os resultados da avaliação
results = []

# Processar cada linha do CSV
for idx, row in df.iterrows():
    input_user = row["query"]
    actual_output = row["answer_llm"]
    expected_output = row["answer"]

    print(f"\n{'='*80}")
    print(f"Avaliando query {idx + 1}/{len(df)}")
    print(f"Query: {input_user}")
    print(f"{'='*80}")

    # Avaliar com DeepEval
    result = deep_eval.eval(
        input_user=input_user,
        actual_output=actual_output,
        expected_output=expected_output,
    )

    # Armazenar resultado
    results.append(result)

    print(f"Resultado: {result}")

# Adicionar resultados ao DataFrame
df["eval_result"] = results

# Salvar o DataFrame atualizado
df.to_csv("./data/metadata.csv", index=False)
print(f"\n{'='*80}")
print("Avaliação concluída! Resultados salvos em ./data/metadata.csv")
print(f"{'='*80}")