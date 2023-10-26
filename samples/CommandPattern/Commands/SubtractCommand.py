from samples.CommandPattern.Commands.ICommand import ICommand
from samples.CommandPattern.Receiver.Calculator import Calculator


class SubtractCommand(ICommand):
    def __init__(self, calculator: Calculator):
        self.__calculator = calculator

    def execute(self, value: float) -> float:
        self.__calculator.subtract(value)
        return self.__calculator.currentValue

    def undo(self, value: float) -> float:
        self.__calculator.add(value)
        return self.__calculator.currentValue
