from threading import Timer

from samples.ObserverPattern.LightSystemSimulation.Lights.IObserver import IObserver
from samples.ObserverPattern.LightSystemSimulation.MotionSensor.IMotionSensor import IMotionSensor


class MockMotionSensor(IMotionSensor):
    def __init__(self, detectionCycle: int = 5):
        self.__detectionCycle = detectionCycle
        self.__observerCollection = []
        self.__detectionTask = self.__getDetectionTask()
        self.__detectionTask.start()

    def __getDetectionTask(self) -> Timer:
        return Timer(self.__detectionCycle, self.__notifyObservers, [])

    def subscribe(self, observer: IObserver) -> None:
        if observer is not None:
            self.__observerCollection.append(observer)

    def unsubscribe(self, observer: IObserver) -> None:
        if observer is not None:
            self.__observerCollection.remove(observer)

    def __notifyObservers(self) -> None:
        self.__detectionTask.cancel()
        for observer in self.__observerCollection:
            observer.update()
        self.__detectionTask = self.__getDetectionTask()
        self.__detectionTask.start()
