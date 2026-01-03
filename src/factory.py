from src.chunking import character, recursive, semantic
from src.embedding import huggingface
from src.vector_store import chroma



_CHUNKERS = {
    "character": character.Character,
    "recursive": recursive.Recursive,
    "semantic" : semantic.Semantic
}


_EMBEDDINGS = {
    "huggingface": huggingface.HuggingFace,
}


_VECTOR_STORES = {"chroma": chroma.Chroma_Store}




def get_chunker(name="character", **kwargs):
    if name not in _CHUNKERS:
        raise ValueError(f"Chunker '{name}' não existe")
    return _CHUNKERS[name](**kwargs)


def get_embedding(name="huggingface", **kwargs):
    if name not in _EMBEDDINGS:
        raise ValueError(f"Embedding '{name}' não existe")
    return _EMBEDDINGS[name](**kwargs)


def get_vector_store(name="chroma", **kwargs):
    if name not in _VECTOR_STORES:
        raise ValueError(f"Vector store '{name}' não existe")
    return _VECTOR_STORES[name](**kwargs)
