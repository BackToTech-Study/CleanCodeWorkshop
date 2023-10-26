from datetime import datetime
from .ILogger import ILogger


class Logger(ILogger):
    def info(self, message):
        self.__show(message)

    def error(self, message):
        self.__show(message)

    def fatal(self, message):
        self.__show(message)

    def __show(self, message):
        print(f"{datetime.now()} - {message}")
