import logging
from os.path import normpath, exists
from os import mkdir
from tkinter.filedialog import askdirectory
from tkinter.messagebox import askquestion, showerror
from model.database import Database
from model.classes.config import Configuration
from model.gui_config import GuiConfiguration
from view.settings import Setting
from controller.validation_controller import int_validate

logger = logging.getLogger('settings_controller')


class SetttingsController:
    def __init__(self, settings_view: Setting, current_configuration: object, database: Database, gui_configuration: GuiConfiguration) -> None:
        self.frame = settings_view
        self.database = database
        self.current_configuration = current_configuration
        self.gui_configuration = gui_configuration
        self.configuration = self.database.get('configuration')
        self.last_grab = self.frame.grab_current()
        self.frame.grab_set()   
        win_pos = self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'settings')
        if win_pos:
            self.frame.geometry(win_pos)
        self.frame.protocol('WM_DELETE_WINDOW', self.__on_window_close)  

        # Widgets Entries
        self.entry_file_path = self.frame.entry_file_path
        self.entry_file_name = self.frame.entry_file_name
        self.entry_file_extension = self.frame.entry_file_extension
        self.entry_job_minimum_lenght = self.frame.entry_job_minimum_lenght
        self.entry_store_time = self.frame.entry_store_time

        # Widgets Buttons
        self.button_file_path = self.frame.button_file_path
        self.button_cancel = self.frame.button_cancel
        self.button_ok = self.frame.button_ok

        # Commands
        self.button_file_path.config(command=self.file_path_command)
        self.button_cancel.config(command=self.cancel_command)
        self.button_ok.config(command=self.ok_command)
        self.entry_list = (self.entry_file_path, self.entry_file_name, self.entry_file_extension, self.entry_job_minimum_lenght, self.entry_store_time)
        self.fill_entries()

        # Validation
        self.int_vcmd = (self.frame.register(int_validate), 
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_job_minimum_lenght.config(validate='key', validatecommand=self.int_vcmd)
        self.entry_store_time.config(validate='key', validatecommand=self.int_vcmd)


    def file_path_command(self, event=None) -> None:
        file_path = askdirectory(initialdir='/', title='Select the file path')
        old_path = self.entry_file_path.get()
        if file_path:
            try:
                file_path = normpath(file_path)
                self.entry_file_path.delete(0, 'end')
                self.entry_file_path.insert('end', str(file_path))
                self.entry_file_path.lift()
                logger.debug(f'File path {file_path}')
            except Exception as error:
                logger.warning(f'Could not get file path due {error}')
                if old_path:
                    self.entry_file_path.delete(0, 'end')
                    self.entry_file_path.insert('end', str(old_path))

    def cancel_command(self, event=None) -> None:
        self.save_close()

    def ok_command(self, event=None) -> None:
        self.save_close()

    def save_close(self) -> None:
        new_config = self.get_entries()
        if not new_config.__eq__(self.configuration):
            answer = askquestion('Configuration save', 'Changes were made in configuration. \nDo you want to save it?')
            if answer == 'yes':
                self.save(new_config)
        self.destroy()

    def save(self, new_config: Configuration) -> None:
        try:
            self.database.save_update('configuration', new_config)
            self.current_configuration(new_config)
        except Exception as error:
            logger.error(f'Could not save due {error}')
            showerror(f'Could not save configuration due {error}')
        return

    def fill_entries(self) -> None:
        self.clear()
        self.entry_file_path.insert(0, normpath(self.configuration.file_path))
        self.entry_file_name.insert(0, self.configuration.file_name)
        self.entry_file_extension.insert(0, self.configuration.file_extension)
        self.entry_job_minimum_lenght.insert(0, str(self.configuration.job_minimum_length))
        self.entry_store_time.insert(0, str(self.configuration.days_to_keep))

    def get_entries(self) -> Configuration:
        try:
            new_file_path = self.entry_file_path.get()
            if not exists(new_file_path):
                mkdir(new_file_path)
            file_name = self.entry_file_name.get().lower().replace(' ', '_')
            file_extension = self.entry_file_extension.get().lower()
            job_minimum_length = int(self.entry_job_minimum_lenght.get())
            store_time = int(self.entry_store_time.get())
            return Configuration(new_file_path, file_name, file_extension, job_minimum_length, store_time)
        except Exception as error:
            showerror('Configuration error', 'Could not get configuration values.')
            logger.warning(f'Could not get entries due {error}')
            self.fill_entries()

    def clear(self) -> None:
        for entry in self.entry_list:
            entry.delete(0, 'end')
    
    def __on_window_close(self):
        self.destroy()

    def destroy(self) -> None:
        if self.last_grab:
            self.last_grab.grab_set()
        self.gui_configuration.check_update_win_pos(self.frame.geometry(), 'settings')
        self.frame.destroy()