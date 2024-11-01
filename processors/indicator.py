from abc import ABC, abstractmethod

class Indicator(ABC):
    @abstractmethod
    def compute(self, *args, **kwargs):
        raise NotImplementedError("This method should be implemented by subclasses")
