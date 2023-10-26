from consolemenu import ConsoleMenu, Screen
from consolemenu.items import FunctionItem

from samples.CommandPattern.Commands.ICommand import ICommand
from samples.CommandPattern.Helpers.ExecutedCommand import ExecutedCommand


class UserInterface:
    def __init__(self, addCommand: ICommand, subtractCommand: ICommand, multiplyCommand: ICommand, divideCommand: ICommand):
        self.__addCommand = addCommand
        self.__subtractCommand = subtractCommand
        self.__multiplyCommand = multiplyCommand
        self.__divideCommand = divideCommand
        self.__executedCommands = []
        self.__undoneCommands = []

        self.__menu = ConsoleMenu("Calculator", "", exit_option_text='Exit', exit_menu_char='q')
        self.__updateCurrentValue(0)
        add = FunctionItem("Add", function=self.__runWithInput, args=[self.__add], menu_char="+")
        subtract = FunctionItem("Subtract", function=self.__runWithInput, args=[self.__subtract], menu_char="-")
        multiply = FunctionItem("Multiply", function=self.__runWithInput, args=[self.__multiply], menu_char="*")
        divide = FunctionItem("Divide", function=self.__runWithInput, args=[self.__divide], menu_char="/")
        undo = FunctionItem("Undo", function=self.__replay, args=[self.__undo], menu_char="u")
        redo = FunctionItem("Redo", function=self.__replay, args=[self.__redo], menu_char="r")

        self.__menu.append_item(add)
        self.__menu.append_item(subtract)
        self.__menu.append_item(multiply)
        self.__menu.append_item(divide)
        self.__menu.append_item(undo)
        self.__menu.append_item(redo)

    def listenForCommands(self):
        self.__menu.show()

    def __updateCurrentValue(self, newValue: float):
        self.__menu.subtitle = f"Current value {newValue}"

    def __getValue(self) -> float or None:
        try:
            return float(self.__menu.screen.input(prompt='Enter value: '))
        except ValueError:
            self.__menu.screen.println("Invalid value")
            return None

    def __runWithInput(self, operation):
        value = self.__getValue()
        if value is None:
            return
        result = operation(value)
        self.__updateCurrentValue(result)

    def __replay(self, operation):
        result = operation()
        if result is not None:
            self.__updateCurrentValue(result)

    def __add(self, value) -> float:
        result = self.__addCommand.execute(value)
        self.__executedCommands.append(ExecutedCommand(self.__addCommand, value))
        return result

    def __subtract(self, value) -> float:
        result = self.__subtractCommand.execute(value)
        self.__executedCommands.append(ExecutedCommand(self.__subtractCommand, value))
        return result

    def __multiply(self, value) -> float:
        result = self.__multiplyCommand.execute(value)
        self.__executedCommands.append(ExecutedCommand(self.__multiplyCommand, value))
        return result

    def __divide(self, value) -> float:
        result = self.__divideCommand.execute(value)
        self.__executedCommands.append(ExecutedCommand(self.__divideCommand, value))
        return result

    def __undo(self) -> float or None:
        if len(self.__executedCommands) <= 0:
            return None

        stored = self.__executedCommands.pop()
        result = stored.command.undo(stored.value)
        self.__undoneCommands.append(stored)
        return result

    def __redo(self) -> float or None:
        if len(self.__undoneCommands) <= 0:
            return None

        stored = self.__undoneCommands.pop()
        result = stored.command.execute(stored.value)
        self.__executedCommands.append(stored)
        return result
