from abc import abstractmethod, ABC


class ILightState(ABC):
    @abstractmethod
    def processMotionDetected(self) -> None:
        pass
