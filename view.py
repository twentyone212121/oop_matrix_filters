import tkinter as tk
from tkinter import filedialog as fd
from show_image_target import ShowImageTarget

class View(tk.Frame):
    def __init__(self, parent) -> None:
        super().__init__(parent)
        self['bd'] = 0
        self['bg'] = '#ffffff'
        self['highlightcolor'] = '#ffffff'
        self['highlightbackground'] = '#ffffff'

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Left Frame and its contents
        leftFrame = tk.Frame(self, width=240, height = 480)
        leftFrame.grid(row=0, column=0, padx=8, pady=4, sticky="nsew")
        leftFrame.grid_rowconfigure(0, weight=1)
        leftFrame.grid_columnconfigure(0, weight=1)
        leftFrame['bg'] = '#dfe4ea'

        self.filtersList = FiltersList(leftFrame)
        self.filtersList.grid(row=0, column=0, padx=10, pady=(10, 6), sticky='nsew')

        matrixEntry = MatrixEntry(leftFrame)
        matrixEntry.grid(row=1, column=0, padx=10, pady=(0, 6), sticky='nsew')
        matrixEntry.on_enter_callback = self.add_matrix_filter

        # Right Frame and its contents
        self.showImageTarget = ShowImageTarget(self)
        self.showImageTarget.grid(row=0, column=1, padx=8, pady=2, sticky="nsew")

    def set_controller(self, controller):
        self.controller = controller

        # Key binds
        self.bind_all('<Command-z>', self.controller.undo)
        self.bind_all('<Command-y>', self.controller.redo)
        self.bind_all('<Command-s>', self.controller.save_image)
        self.bind_all('<Command-o>', self.controller.load_image)
        self.bind_all('<Command-d>', self.controller.clear)
    
    def set_default_filters(self, default_filters):
        for (name, callback) in default_filters:
            self.filtersList.add_filter(name, callback)
    
    def get_save_file_name(self, filetypes):
        return fd.asksaveasfilename(title='Select where to save a file', initialdir='/', filetypes=filetypes)
    
    def get_load_file_name(self, filetypes):
        return fd.askopenfilename(title='Select a picture to open', initialdir='/', filetypes=filetypes)
    
    def update_image(self, image):
        self.showImageTarget.update_image(image)
    
    def clear_image(self):
        self.showImageTarget.clear()

    def add_matrix_filter(self, matrix, name):
        callback = self.controller.create_matrix_filter(matrix)
        self.filtersList.add_filter(name, callback)
    
class FiltersList(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self['bg'] = '#ced6e0'
        self['highlightbackground'] = '#ced6e0'

        # Create a header
        self.header = tk.Label(self, text='Filters list:')
        self.header.pack(side=tk.TOP)
        self.header['bg'] = '#ced6e0'
        self.header['highlightbackground'] = '#ced6e0'
        self.header['fg'] = '#2f3542'

        # Create a scrollable canvas
        self.canvas = tk.Canvas(self)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.canvas['bg'] = '#ced6e0'
        self.canvas['highlightcolor'] = '#ced6e0'
        self.canvas['highlightbackground'] = '#ced6e0'

        # Add a scrollbar to the canvas
        self.scrollbar = tk.Scrollbar(self, orient=tk.VERTICAL, command=self.canvas.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Create a frame inside the canvas for the buttons
        self.button_frame = tk.Frame(self.canvas, width=self.canvas.size()[0])
        self.button_frame['bg'] = '#ced6e0'
        self.canvas.create_window((200, 200), window=self.button_frame, anchor=tk.CENTER)

        # Create buttons list
        self.buttons = []

        # Update the canvas scrollable region
        self.button_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        # Bind mouse scroll events to the canvas
        self.canvas.bind_all("<MouseWheel>", self.on_mouse_scroll)

    def add_filter(self, text: str, callback):
        button = tk.Button(self.button_frame, text=text, command=callback, width=self.button_frame.size()[0])
        button.pack(pady=(0, 3), fill='both', expand=True)
        button['bg'] = '#ced6e0'
        button['highlightbackground'] = '#ced6e0'
        button['fg'] = '#2f3542'
        self.buttons.append(button)

        # Update the canvas scrollable region
        self.button_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_button_click(self, button_text):
        print("Button clicked:", button_text)

    def on_mouse_scroll(self, event):
        self.canvas.yview_scroll(-event.delta, "units")


class MatrixEntry(tk.Frame):
    def __init__(self, parent: tk.Frame) -> None:
        super().__init__(parent)
        self['bg'] = '#ced6e0'
        
        self.__on_enter_callback = None

        # init matrix fields
        self.__entry_fields = []
        for i in range(3):
            row_entries = []
            for j in range(4):
                bgcolor = '#FFFFFF'
                if (j == 0):
                    bgcolor = '#ff4757'
                elif (j == 1):
                    bgcolor = '#2ed573'
                elif (j == 2):
                    bgcolor = '#3742fa'
                entry = tk.Entry(self, width=8)
                entry['bg'] = bgcolor
                entry['fg'] = '#2f3542'
                entry['highlightbackground'] = '#ced6e0'
                entry.grid(row=i, column=j, padx=2, pady=2)
                row_entries.append(entry)
            self.__entry_fields.append(row_entries)

        # init text
        self.name_hint = tk.Label(self, text='Name: ')
        self.name_hint.grid(row=4, column=0)
        self.name_hint['bg'] = '#ced6e0'
        self.name_hint['fg'] = '#2f3542'

        # init text entry
        self.name_var = tk.StringVar()
        self.name_entry = tk.Entry(self, textvariable=self.name_var)
        self.name_entry.grid(row=4, column=1, columnspan=2, pady=5)
        self.name_entry['bg'] = '#f1f2f6'
        self.name_entry['highlightbackground'] = '#ced6e0'
        self.name_entry['fg'] = '#2f3542'

        # init button
        self.submit_button = tk.Button(self, text="Add matrix filter", command=self.get_matrix_entries)
        self.submit_button.grid(row=4, column=3)
        self.submit_button['bg'] = '#ced6e0'
        self.submit_button['highlightbackground'] = '#ced6e0'
        self.name_hint['fg'] = '#2f3542'
    
    @property
    def on_enter_callback(self):
        return self.__on_enter_callback
    
    @on_enter_callback.setter
    def on_enter_callback(self, callback):
        self.__on_enter_callback = callback

    def get_matrix_entries(self):
        matrix = []
        for i in range(3):
            row = []
            for j in range(4):
                entry = self.__entry_fields[i][j].get()
                row.append(float(entry))
            matrix.append(row)
        
        try:
            self.__on_enter_callback(matrix, self.name_var.get())
        except:
            self.show_callback_error()
    
    def show_callback_error(self):
        self.submit_button['fg'] = 'red'
        self.submit_button.after(2000, self.hide_callback_error)
    
    def hide_callback_error(self):
        self.submit_button['fg'] = 'black'

