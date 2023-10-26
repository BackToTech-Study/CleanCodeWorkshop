from samples.CommandPattern.Commands.AddCommand import AddCommand
from samples.CommandPattern.Commands.DivideCommand import DivideCommand
from samples.CommandPattern.Commands.MultiplyCommand import MultiplyCommand
from samples.CommandPattern.Commands.SubtractCommand import SubtractCommand
from samples.CommandPattern.Receiver.Calculator import Calculator


class Client:
    def __init__(self):
        self.__calculator = Calculator()
        self.addCommand = AddCommand(self.__calculator)
        self.subtractCommand = SubtractCommand(self.__calculator)
        self.multiplyCommand = MultiplyCommand(self.__calculator)
        self.divideCommand = DivideCommand(self.__calculator)
