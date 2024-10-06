from abc import ABC, abstractmethod


class BaseWindow(ABC):  # each window has custom initialization to stay flexible
    @abstractmethod
    def draw(self) -> None:
        pass
