from abc import ABC, abstractmethod


class ABC_Chunking(ABC):
    def __init__(self):
        pass

    @abstractmethod
    def split_document(self):
        pass

    def get_kwargs(self):
        print(vars(self.splitter))

        # print(dir(self.splitter))
        # print(self.splitter.__dict__)
