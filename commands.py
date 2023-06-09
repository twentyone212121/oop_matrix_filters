from abc import * 
from filters import Filter
from PIL import Image

class Command(object, metaclass=ABCMeta):
    '''
    Abstract class that defines Command interface on Image: execute method
    '''
    @abstractmethod
    def execute(self, image: Image.Image):
        pass


class HistoryCommand(Command):
    '''
    Holder of the past commands for this Image
    '''
    def __init__(self):
        self.__past_commands = []
        self.__future_commands = []

    def execute(self, image: Image.Image) -> Image.Image:
        '''
        Execute all past commands
        '''
        last_image = image
        for past_command in self.__past_commands:
            last_image = past_command.execute(last_image)
        return last_image

    def add(self, cmd):
        if (len(self.__future_commands) > 0):
            self.__future_commands.clear()
        self.__past_commands.append(cmd)

    def undo(self):
        '''
        Delete the last command
        '''
        if len(self.__past_commands) != 0:
            self.__future_commands.append(self.__past_commands.pop())
    
    def redo(self):
        '''
        Redo the last undoed command
        '''
        if len(self.__future_commands) != 0:
            self.__past_commands.append(self.__future_commands.pop())

    def clear(self):
        '''
        Delete all history of commands
        '''
        self.__past_commands.clear()
        self.__future_commands.clear()

class ApplyFilterCommand(Command):
    '''
    Command to apply a filter
    '''
    def __init__(self, filter: Filter):
        self.__filter = filter

    def execute(self, image: Image.Image) -> Image.Image:
        return self.__filter.apply(image)
