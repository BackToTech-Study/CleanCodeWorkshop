from abc import abstractmethod, ABC


class ICommand(ABC):
    @abstractmethod
    def execute(self, value: float) -> float:
        pass

    @abstractmethod
    def undo(self, value: float) -> float:
        pass
