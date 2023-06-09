from PIL import Image
from commands import HistoryCommand, ApplyFilterCommand
from filters import *

class Model:
    def __init__(self) -> None:
        self.original_image = None
        self.current_image = None
        self.history = HistoryCommand()
    
    def undo(self) -> Image.Image:
        self.history.undo()
        self.current_image = self.original_image.copy()
        self.current_image = self.history.execute(self.current_image)
        return self.current_image
    
    def redo(self) -> Image.Image:
        self.history.redo()
        self.current_image = self.original_image.copy()
        self.current_image = self.history.execute(self.current_image)
        return self.current_image
    
    def save_image(self, path: str) -> None:
        self.current_image.save(path, subsampling=0, quality=100)
    
    def load_image(self, path: str) -> Image.Image:
        self.original_image = Image.open(path)
        self.current_image = self.original_image.copy()
        return self.current_image
    
    def clear(self) -> None:
        self.history.clear()
    
    def apply_filter(self, filter: Filter) -> Image.Image:
        if self.current_image is None:
            return self.current_image
        apply_filter_command = ApplyFilterCommand(filter)
        self.history.add(apply_filter_command)
        self.current_image = apply_filter_command.execute(self.current_image)
        return self.current_image
    
    def create_matrix_filter(self, matrix):
        return CustomFilter(matrix)
    
    def get_default_filters(self) -> list[tuple[str, Filter]]:
        default_filters = \
        [('Black & white', BlackWhiteFilter()), 
        ('Only red', OnlyRedFilter()), 
        ('Only green', OnlyGreenFilter()), 
        ('Only blue', OnlyBlueFilter()), 
        ('Sepia', SepiaFilter()), 
        ('Max hue', HueFilter()), 
        ('Max saturation', MaxSaturationFilter()), 
        ('Max contrast', MaxContrastFilter())]
        return default_filters