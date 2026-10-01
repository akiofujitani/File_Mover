from tkinter import Toplevel, Frame, Label, Button
from PIL.Image import open
from PIL.ImageTk import PhotoImage


class About(Toplevel):
    '''
    About Window
    ------------

    Meant to store development information
    '''    
    def __init__(self, label_values: str, image_file: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.minsize(450, 400)
        self.gui_name = 'about'
        self.title('About')
        self.resizable(width=False, height=False)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.about_frame = Frame(self)
        self.about_frame.grid(column=0, row=0, sticky='nesw')

        image = open(image_file)
        image_tk = PhotoImage(image=image)
        image_label = Label(self.about_frame, image=image_tk, justify='center')
        image_label.image = image_tk
        image_label.grid(column=0, row=0, columnspan=3, padx=(10), pady=(5, 0), sticky='nesw')

        text_label = Label(self.about_frame, text=label_values, justify='left')
        text_label.grid(column=0, row=1, columnspan=2, sticky='sw', padx=(5), pady=(5, 0))

        self.ok_button = Button(self.about_frame, text='Ok', width=15)
        self.ok_button.grid(column=2, row=1, sticky='se', padx=(10), pady=(0, 10))

        self.about_frame.grid_columnconfigure(1, weight=1)
        self.about_frame.grid_rowconfigure(0, weight=1)
