from src.document_loaders import txt_loader, pdf_loader
from src.chunking import character, recursive
from src.embedding import huggingface
from src.vector_store import chroma


_LOADER_DOCUMENTS = {"txt": txt_loader.TXT_Loader, "pdf": pdf_loader.PDF_Loader}

_CHUNKERS = {
    "character": character.Character,
    "recursive": recursive.Recursive,
}


_EMBEDDINGS = {
    "huggingface": huggingface.HuggingFace,
}


_VECTOR_STORES = {"chroma": chroma.Chroma_Store}


def get_document_loader(name="txt", **kwargs):
    if name not in _LOADER_DOCUMENTS:
        raise ValueError(f"Document Loader '{name}' não existe")
    return _LOADER_DOCUMENTS[name](**kwargs)


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
