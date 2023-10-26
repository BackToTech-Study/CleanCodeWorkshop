from samples.CommandPattern.Commands.ICommand import ICommand
from samples.CommandPattern.Receiver.Calculator import Calculator


class DivideCommand(ICommand):
    def __init__(self, calculator: Calculator):
        self.__calculator = calculator

    def execute(self, value: float) -> float:
        self.__calculator.divide(value)
        return self.__calculator.currentValue

    def undo(self, value: float) -> float:
        self.__calculator.multiply(value)
        return self.__calculator.currentValue
