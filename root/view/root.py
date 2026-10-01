from tkinter import Tk

class Root(Tk):
    '''
    Root Class
    ----------
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)  
        min_width = 450
        min_height = 350
        self.minsize(min_width, min_height)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def destroy(self) -> None:
        return super().destroy()