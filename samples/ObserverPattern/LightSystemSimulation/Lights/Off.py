from datetime import datetime

from samples.ObserverPattern.LightSystemSimulation.Lights.ILightState import ILightState
from samples.ObserverPattern.LightSystemSimulation.Logger.ILogger import ILogger


class Off(ILightState):
    def __init__(self, light, log: ILogger):
        log.info("Turn off lights.")
        self.__light = light

    def processMotionDetected(self) -> None:
        self.__light.turnOn()