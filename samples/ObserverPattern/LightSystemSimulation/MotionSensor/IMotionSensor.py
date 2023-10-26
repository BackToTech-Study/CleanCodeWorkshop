from abc import abstractmethod, ABC

from samples.ObserverPattern.LightSystemSimulation.Lights.IObserver import IObserver


class IMotionSensor(ABC):
    @abstractmethod
    def subscribe(self, observer: IObserver) -> None:
        pass

    @abstractmethod
    def unsubscribe(self, observer: IObserver) -> None:
        pass
