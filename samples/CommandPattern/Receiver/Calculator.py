class Calculator:
    def __init__(self):
        self.__currentValue: float = 0

    @property
    def currentValue(self) -> float:
        return self.__currentValue

    def add(self, value: float):
        self.__currentValue += value

    def subtract(self, value: float):
        self.__currentValue -= value

    def multiply(self, value: float):
        self.__currentValue *= value

    def divide(self, value: float):
        if value == 0:
            raise ValueError("Cannot divide by zero")
        self.__currentValue /= value
