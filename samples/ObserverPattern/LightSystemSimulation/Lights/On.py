from threading import Timer

from samples.ObserverPattern.LightSystemSimulation.Lights.ILightState import ILightState
from samples.ObserverPattern.LightSystemSimulation.Logger.ILogger import ILogger


class On(ILightState):
    def __init__(self, light, log: ILogger):
        self.__log = log

        self.__log.info("Turn on lights.")
        self.__light = light

        self.__timeoutTask = self.__getTimeoutTask()
        self.__timeoutTask.start()

    def __getTimeoutTask(self) -> Timer:
        return Timer(self.__light.timeout, self.__turnOffAfterTimeout, [])

    def __turnOffAfterTimeout(self):
        self.__log.info("Inactivity timeout reached.")
        self.__light.turnOff()

    def processMotionDetected(self) -> None:
        self.__timeoutTask.cancel()
        self.__timeoutTask = self.__getTimeoutTask()
        self.__timeoutTask.start()
