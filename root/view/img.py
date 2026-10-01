import logging
from tkinter import Tk, Frame
from os.path import normpath
from model.scripts.file_handler import resource_path
from model.constants import IMG_PATH
from PIL import Image, ImageTk

logger = logging.getLogger('img')


class Images(Frame):
    '''
    Images
    ------

    Load image files to class

    https://www.flaticon.com/free-icons/send

    https://www.flaticon.com/free-icons/settings
    
    https://www.flaticon.com/free-icons/black-cat
    '''    
    def __init__(self, *args, **kwargs) -> None:
        try:
            # Load and format all images
            image_dimension = 45
            self.icon_path = resource_path(IMG_PATH + '/shih-tzu_02.png')
            start_image = Image.open(resource_path(IMG_PATH + '/play.png'))
            start_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.start = ImageTk.PhotoImage(start_image)
            pause_image = Image.open(resource_path(IMG_PATH + '/pause.png'))
            pause_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.pause = ImageTk.PhotoImage(pause_image)            
            stop_image = Image.open(resource_path(IMG_PATH + '/stop.png'))
            stop_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.stop = ImageTk.PhotoImage(stop_image)
            settings_image = Image.open(resource_path(IMG_PATH + '/settings.png'))
            settings_image.thumbnail((image_dimension, image_dimension), Image.Resampling.LANCZOS)
            self.settings = ImageTk.PhotoImage(settings_image)
            self.icon = Image.open(self.icon_path)
            self.icon.thumbnail((96, 96), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(self.icon)
            self.master.wm_iconphoto(True, photo)
        except Exception as error:
            logger.error(f'Could not load icon {error}')

