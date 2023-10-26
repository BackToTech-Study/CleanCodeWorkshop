import logging
from logging.handlers import RotatingFileHandler

from .ILogger import ILogger
from ..configurations.LoggerConfiguration import LoggerConfiguration


def getFormatter() -> logging.Formatter:
    return logging.Formatter('%(levelname)s - %(message)s')


def getStdOutLogHandler():
    handler = logging.StreamHandler()
    handler.setFormatter(getFormatter())
    return handler


def getRollingFileLogHandler(fileName, maxBytes, backupCount):
    handler = RotatingFileHandler(fileName, maxBytes=maxBytes, backupCount=backupCount)
    handler.setFormatter(getFormatter())
    return handler


class Logger(ILogger):
    def __init__(self, loggerName: str, level: int, handlerCollection: []):
        self.__logger = logging.getLogger(loggerName)

        for handler in handlerCollection:
            self.addHandler(handler)

        self.setLevel(level)

    def addHandler(self, handler):
        self.__logger.addHandler(handler)

    def setLevel(self, level):
        self.__logger.setLevel(level)

    def info(self, message):
        self.__logger.info(message)

    def error(self, message):
        self.__logger.error(message)

    def fatal(self, message):
        self.__logger.fatal(message)
