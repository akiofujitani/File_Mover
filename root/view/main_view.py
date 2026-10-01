import logging
from tkinter import scrolledtext, Button, WORD
from tkinter import Frame, Tk
from PIL import Image, ImageTk
from model.scripts.file_handler import resource_path
from idlelib.tooltip import Hovertip

logger = logging.getLogger('nome')


class MainView(Frame):
    def __init__(self, master: Tk, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.master = master      

        try:
            # Load and format all images
            image_dimension = 45
            self.icon_path = resource_path('./Img/shih-tzu_02.png')
            start_image = Image.open(resource_path('./Img/play.png'))
            start_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.start = ImageTk.PhotoImage(start_image)
            pause_image = Image.open(resource_path('./Img/pause.png'))
            pause_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.pause = ImageTk.PhotoImage(pause_image)            
            stop_image = Image.open(resource_path('./Img/stop.png'))
            stop_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.stop = ImageTk.PhotoImage(stop_image)
            settings_image = Image.open(resource_path('./Img/settings.png'))
            settings_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.settings = ImageTk.PhotoImage(settings_image)
            self.icon = Image.open(self.icon_path)
            self.icon.thumbnail((96, 96), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(self.icon)
            self.master.wm_iconphoto(True, photo)
        except Exception as error:
            logger.error(f'Could not load icon {error}')

        button_frame = Frame(self)
        button_frame.grid(column=0, row=0, columnspan=5, sticky='nesw')
        button_frame.grid_columnconfigure(3, weight=1)

        button_dimension = 60
        self.start_button = Button(button_frame, text='Start', image=self.start, compound='top', width=button_dimension, height=button_dimension)
        self.start_button.grid(column=0, row=0, padx=(3, 0), pady=(3), sticky='nesw')
        Hovertip(self.start_button, 'Monitoring cicle start.')    
        self.stop_button = Button(button_frame, text='Stop', image=self.stop, compound='top', width=button_dimension, height=button_dimension)
        self.stop_button.grid(column=2, row=0, padx=(0, 3), pady=(3), sticky='nesw')
        Hovertip(self.stop_button, 'Monitoring cicle stop.')
        self.config_button = Button(button_frame, text='Settings', image=self.settings, compound='top', width=button_dimension, height=button_dimension)
        self.config_button.grid(column=4, row=0, padx=(3), pady=(3), sticky='nesw')  
        Hovertip(self.config_button, 'Enter configuration.')

        self.scrolled_text = scrolledtext.ScrolledText(self, state='disabled')
        self.scrolled_text.configure(wrap=WORD, font=('Arial', 9))
        self.scrolled_text.grid(column=0, row=1, columnspan=4, sticky='nesw', padx=(5), pady=(5))
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)


if __name__ == '__main__':
    root = Tk()
    main_frame = Frame(root)
    main_frame.grid(column=0, row=0, sticky='nesw')
    settings = MainView(main_frame)
    root.mainloop()
