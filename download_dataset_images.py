"""
Script simples para baixar apenas as imagens do dataset VDR_ibm-research_REAL-MM-RAG
do Hugging Face.

As imagens serão salvas em ./data/huggingface_images/ e você pode processá-las
depois com o your_lego_indexing.py
"""

from datasets import load_dataset
from PIL import Image
import io
import csv
from pathlib import Path


def download_images_from_dataset(num_samples=10, save_path="./data/huggingface_images"):
    """
    Baixa apenas as imagens do dataset e salva localmente.

    Args:
        num_samples: Número de exemplos para baixar (padrão: 10 para teste)
        save_path: Diretório onde as imagens serão salvas

    Returns:
        tuple: (saved_paths, metadata) - Caminhos das imagens e metadados
    """
    print(f"[INFO] Carregando dataset do Hugging Face com streaming...")
    print(
        f"[INFO] Baixando primeiros {num_samples} exemplos (sem baixar dataset completo)"
    )

    # Carrega o dataset com streaming (não baixa tudo)
    dataset_stream = load_dataset(
        "racineai/VDR_ibm-research_REAL-MM-RAG", split="train", streaming=True
    )

    # Pega apenas os primeiros N exemplos
    dataset = list(dataset_stream.take(num_samples))

    print(f"[INFO] {len(dataset)} exemplos carregados com sucesso")

    # Cria diretório para salvar as imagens
    Path(save_path).mkdir(parents=True, exist_ok=True)

    saved_paths = []
    metadata_list = []

    for idx, sample in enumerate(dataset):
        try:
            # Extrai informações do sample
            sample_id = sample["id"]
            query = sample["query"]
            answer = sample["answer"]
            image_data = sample["image"]

            # Define o nome do arquivo da imagem
            image_filename = f"{save_path}/image_{idx:03d}_{sample_id[:8]}.png"

            # Salva a imagem
            if isinstance(image_data, Image.Image):
                image_data.save(image_filename)
            elif isinstance(image_data, bytes):
                img = Image.open(io.BytesIO(image_data))
                img.save(image_filename)
            else:
                print(
                    f"[WARN] Tipo de imagem desconhecido no sample {idx}: {type(image_data)}"
                )
                continue

            saved_paths.append(image_filename)

            # Salva metadados
            metadata = {
                "index": idx,
                "sample_id": sample_id,
                "image_path": image_filename,
                "query": query,
                "answer": answer,
            }
            metadata_list.append(metadata)

            print(f"[OK] {idx+1}/{num_samples} - Salvo: {image_filename}")

        except Exception as e:
            print(f"[ERRO] Falha ao processar sample {idx}: {e}")

    print(f"\n{'='*80}")
    print(f"[SUCESSO] Download completo!")
    print(f"{'='*80}")
    print(f"  📁 Diretório: {save_path}")
    print(f"  🖼️  Imagens salvas: {len(saved_paths)}")
    print(f"\n[PRÓXIMOS PASSOS]")
    print(f"  1. Use o your_lego_indexing.py para processar as imagens")
    print(f'  2. Altere o caminho para: folder_or_file="{save_path}"')

    # Salva metadados em arquivo CSV
    csv_file = f"{save_path}/metadata.csv"
    with open(csv_file, "w", encoding="utf-8", newline="") as f:
        fieldnames = ["id", "query", "answer", "image_path"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)

        writer.writeheader()
        for meta in metadata_list:
            writer.writerow({
                "id": meta["sample_id"],
                "query": meta["query"],
                "answer": meta["answer"],
                "image_path": meta["image_path"]
            })

    print(f"  📄 Metadados salvos em CSV: {csv_file}")

    # Salva metadados em arquivo texto para referência
    metadata_file = f"{save_path}/metadata.txt"
    with open(metadata_file, "w", encoding="utf-8") as f:
        f.write("METADADOS DO DATASET VDR_ibm-research_REAL-MM-RAG\n")
        f.write("=" * 80 + "\n\n")
        for meta in metadata_list:
            f.write(f"Imagem {meta['index']+1}:\n")
            f.write(f"  ID: {meta['sample_id']}\n")
            f.write(f"  Arquivo: {meta['image_path']}\n")
            f.write(f"  Query: {meta['query']}\n")
            f.write(f"  Answer: {meta['answer']}\n")
            f.write("-" * 80 + "\n\n")

    print(f"  📄 Metadados salvos em TXT: {metadata_file}\n")

    return saved_paths, metadata_list


if __name__ == "__main__":
    # CONFIGURAÇÃO: Altere aqui o número de exemplos para baixar
    NUM_SAMPLES = 10  # Mude para 100, 1000, etc conforme necessário

    # Baixa as imagens
    image_paths, metadata = download_images_from_dataset(
        num_samples=NUM_SAMPLES, save_path="./data/huggingface_images"
    )
