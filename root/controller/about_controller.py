import logging
from model.gui_config import GuiConfiguration
from tkinter import Toplevel, Tk

logger = logging.getLogger('about_contoller')


class AboutController:
    '''
    AboutController
    ---------------

    Controller Class For About

    Has little to none controls.
    '''
    def __init__(self, master_win: Tk, about: Toplevel, gui_configuration: GuiConfiguration) -> None:
        self.gui_configuration = gui_configuration
        self.about = about
        self.master_win = master_win
        if self.gui_configuration.always_on_top == True:
            self.about.master_win.attributes('-topmost', False)
        self.last_grab = self.about.grab_current()
        self.about.grab_set()        
        win_pos = self.gui_configuration.check_update_win_pos(self.about.geometry(), self.about.gui_name)
        if win_pos:
            self.about.geometry(win_pos)
        self.about.ok_button.config(command=self.__pressed_ok_button)
        self.about.protocol('WM_DELETE_WINDOW', self.__on_window_close)    
    
    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        self.gui_configuration.check_update_win_pos(self.about.geometry(), 'about')
        self.master_win.attributes('-topmost', self.gui_configuration.always_on_top)
        return self.about.destroy()

    def __pressed_ok_button(self):
        self.__on_window_close()

    def __on_window_close(self):
        self.destroy()