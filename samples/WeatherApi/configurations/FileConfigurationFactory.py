from .Configuration import Configuration
from .Dynamic import Dynamic
from .IConfigurationFactory import IConfigurationFactory


class FileConfigurationFactory(IConfigurationFactory):
    def get(self, fileName: str) -> Configuration:
        configuration = Dynamic.fromFile(fileName)
        return configuration
