from abc import ABC, abstractmethod


class ILogger(ABC):
    @abstractmethod
    def info(self, message: str):
        pass

    @abstractmethod
    def error(self, message: str):
        pass

    @abstractmethod
    def fatal(self, message: str):
        pass
