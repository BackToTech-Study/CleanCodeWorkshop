from abc import ABC, abstractmethod


class IConfigurationFactory(ABC):
    @abstractmethod
    def get(self, configData):
        pass
