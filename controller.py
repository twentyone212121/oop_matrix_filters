from model import Model
from view import View

class Controller:
    def __init__(self, model: Model, view: View) -> None:
        self.model = model
        self.view = view

        default_filter_buttons = [(name, lambda f=flt: self.apply_filter(f)) for (name, flt) in self.model.get_default_filters()]
        self.view.set_default_filters(default_filter_buttons)

    def apply_filter(self, filter):
        new_image = self.model.apply_filter(filter)
        self.view.update_image(new_image)
    
    def undo(self, event):
        new_image = self.model.undo()
        self.view.update_image(new_image)
    
    def redo(self, event):
        new_image = self.model.redo()
        self.view.update_image(new_image)
    
    def save_image(self, event):
        filetypes = (('jpg', '*.jpg'), ('jpeg', '*.jpeg'), ('png', '*.png'))
        filename = self.view.get_save_file_name(filetypes)
        if filename == '':
            return
        
        self.model.save_image(filename)
    
    def load_image(self, event):
        filetypes = (('jpg', '*.jpg'), ('jpeg', '*.jpeg'), ('png', '*.png'))
        filename = self.view.get_load_file_name(filetypes)
        if filename == '':
            return
        
        image = self.model.load_image(filename)
        self.view.update_image(image)
    
    def clear(self, event):
        self.view.clear_image()
        self.model.clear()
    
    def create_matrix_filter(self, matrix):
        filter = self.model.create_matrix_filter(matrix)
        return lambda f=filter: self.apply_filter(f)