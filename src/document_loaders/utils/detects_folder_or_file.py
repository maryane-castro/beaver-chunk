import os
from urllib.parse import urlparse


def is_url(value: str) -> bool:
    """
    Retorna True se a string for uma URL válida.
    """
    try:
        parsed = urlparse(value)
        return bool(parsed.scheme and parsed.netloc)
    except Exception:
        return False


def normalize_and_rename(path):
    """
    Remove extensões intermediárias e renomeia o arquivo fisicamente.
    Se a nova extensão final for .txt, converte para .md.
    """
    dirname, filename = os.path.split(path)
    parts = filename.split('.')

    # Sem extensão ou formato inesperado → deixa como está
    if len(parts) < 2:
        return path

    final_ext = parts[-1].lower()
    base_name = parts[0]

    # Regra extra: se extensão final for .txt → vira .md
    if final_ext == "txt":
        final_ext = "md"

    new_filename = f"{base_name}.{final_ext}"
    new_path = os.path.join(dirname, new_filename)

    # Se já está normalizado, não faz nada
    if new_path == path:
        return path

    # Segurança: se o novo nome já existir, não sobrescreve
    if os.path.exists(new_path):
        print(f"[AVISO] Não renomeado (já existe): {new_path}")
        return path

    # Renomeia fisicamente
    try:
        os.rename(path, new_path)
        print(f"[OK] Renomeado: {path} -> {new_path}")
        return new_path
    except Exception as e:
        print(f"[ERRO] Não foi possível renomear {path}: {e}")
        return path


def detects_folder_or_file(folder_or_file):
    """
    Detecta arquivos, pastas ou URLs e retorna uma lista normalizada.
    """
    # Garante lista
    if isinstance(folder_or_file, str):
        paths = [folder_or_file]
    else:
        paths = folder_or_file

    results = []

    for item in paths:

        # 1) Se for URL → adiciona na lista
        if isinstance(item, str) and is_url(item):
            results.append(item)
            continue

        # 2) Caminho para arquivo local
        if os.path.isfile(item):
            new_path = normalize_and_rename(os.path.abspath(item))
            results.append(new_path)
            continue

        # 3) Caminho para pasta local
        if os.path.isdir(item):
            for root, _, filenames in os.walk(item):
                for fname in filenames:
                    full_path = os.path.join(root, fname)
                    new_path = normalize_and_rename(full_path)
                    results.append(new_path)
            continue

        # 4) Caso nada seja válido
        raise ValueError(f"Caminho inválido ou não encontrado: {item}")

    return results
