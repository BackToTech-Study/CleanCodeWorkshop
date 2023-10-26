from samples.ObserverPattern.LightSystemSimulation.Lights.IObserver import IObserver
from samples.ObserverPattern.LightSystemSimulation.Lights.Off import Off
from samples.ObserverPattern.LightSystemSimulation.Lights.On import On
from samples.ObserverPattern.LightSystemSimulation.Logger.ILogger import ILogger


class LightSystem(IObserver):
    def __init__(self, log: ILogger, timeout: int or None = None):
        self.__log = log
        self.turnOff()
        self.__timeout = timeout

    @property
    def timeout(self) -> int:
        return self.__timeout

    def update(self) -> None:
        self.__log.info("Motion detected.")
        self.__currentState.processMotionDetected()

    def turnOn(self) -> None:
        self.__currentState = On(self, self.__log)

    def turnOff(self) -> None:
        self.__currentState = Off(self, self.__log)
