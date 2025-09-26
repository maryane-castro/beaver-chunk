from abc import ABC, abstractmethod


class ABC_DocumentLoaders(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def get_documents(self):
        pass
