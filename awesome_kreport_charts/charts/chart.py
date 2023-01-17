from abc import ABC, abstractmethod

class Chart(ABC):
    """Abstract chart."""

    def __init__(self):
        super().__init__()

    @abstractmethod
    def plot(self, labels, sources, targets, values):
        pass
