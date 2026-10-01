import logging
from tkinter import Menu
from tkinter.messagebox import askokcancel, showerror, askquestion
from queue import Queue
from datetime import datetime, timedelta
from copy import deepcopy
from model.main import Model
from model.classes.config import Configuration
from model.scripts.file_handler import resource_path, file_writer
from view.about import About
from view.settings import Setting
from view.main_view import MainView
from controller.about_controller import AboutController
from controller.settings_controller import SetttingsController
from controller.validation_controller import int_validate


logger = logging.getLogger('main_view_controller')


class MainViewController:
    '''
    MainViewController
    ------------------

    Controller Class For MainView


    '''
    def __init__(self, main_view: MainView, model: Model, log_queue: Queue) -> None:
        self.frame = main_view
        self.master = self.frame.master
        self.model = model
        self.gui_configuration = self.model.gui_configuration
        self.database = self.model.database
        self.configuration = self.database.get('configuration')
        self.job_block_list = self.database.get('job_list')
        self.log_queue = log_queue
        self.entry_job = self.frame.entry_job
        self.button_send = self.frame.button_send
        self.button_settings = self.frame.button_setting

        self.treeview = self.frame.treeview
        for column in self.frame.columns:
            self.treeview.heading(column, command=lambda column_value=column: self.__sort_tree_view(column_value, False))  
        self.treeview.bind('<3>', self.do_popup)
        self.entry_job.bind('<Return>', self.__send)

        menu_bar = Menu(self.frame)
        file_menu = Menu(menu_bar, tearoff=0)
        file_menu.add_command(label='Send   ', command=self.__send)
        file_menu.add_command(label='Update   ', command=self.__update)
        file_menu.add_separator()
        file_menu.add_command(label='Exit   ', command=self.__quit)

        edit_menu = Menu(menu_bar, tearoff=0)
        edit_menu.add_command(label='Setting   ', command=self.__setting)

        help_menu = Menu(menu_bar, tearoff=0)
        help_menu.add_command(label='About  ', command=self.__about)

        menu_bar.add_cascade(label='File   ', menu=file_menu)
        menu_bar.add_cascade(label='Edit   ', menu=edit_menu)
        menu_bar.add_cascade(label='Help   ', menu=help_menu)

        self.master.config(menu=menu_bar)
        self.master.protocol('WM_DELETE_WINDOW', self.__quit)

        self.button_send.config(command=self.__send)
        self.button_settings.config(command=self.__setting)

        self.int_vcmd = (self.master.register(int_validate), 
                        '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_job.config(validate='key', validatecommand=self.int_vcmd)

        self.__update_job_list_by_date()

        self.popup = Menu(self.frame, tearoff=0)
        self.popup.add_command(label='Delete  ', command=self.__delete)
        self.popup.add_separator()


    def __update_job_list_by_date(self) -> None:
        '''
        Remove values older than set data from job_list class, saves it and updates the Automatic Calculation job_list_block
        '''
        self.job_block_list.remove_older_than(self.__set_removal_date())
        self.database.save_update('job_list', self.job_block_list)
        self.__update_job_list()            
        if len(self.job_block_list.job_list) > 0:
            self.set_treeview()

    def __sort_tree_view(self, colum_value, descending):
        '''
        Sort treeview by its columns

        https://www.w3resource.com/python-exercises/tkinter/python-tkinter-widgets-exercise-18.php
        '''
        tree_view_data = [(self.treeview.set(item, colum_value), item) for item in self.treeview.get_children('')]
        if colum_value == 'insertion_date':
            tree_view_data = [(datetime.strptime(treeview_date[0], "%d/%m/%Y %H:%M:%S"), treeview_date[1]) for treeview_date in tree_view_data]
        tree_view_data.sort(reverse=descending)
        even_odd = {0 : 'evenrow', 1 : 'oddrow'}
        for index, (_, item) in enumerate(tree_view_data):
            self.treeview.move(item, '', index)
            self.treeview.item(item, tags=(even_odd.get(index % 2)))
        self.treeview.heading(colum_value, command=lambda: self.__sort_tree_view(colum_value, not descending))

    def do_popup(self, event=None) -> None:
        row_id =self.treeview.identify('item', event.x, event.y)
        if row_id:
            self.treeview.selection_set(row_id)
            self.treeview.focus_set()
            self.treeview.focus(row_id)            
            self.popup.post(event.x_root, event.y_root)

    def __set_removal_date(self) -> datetime:
        date_to_remove = datetime.today().date() - timedelta(self.configuration.days_to_keep)
        return datetime(date_to_remove.year, date_to_remove.month, date_to_remove.day)

    def set_treeview(self) -> None:
        even_odd = {0: 'evenrow', 1: 'oddrow'}
        self.treeview.delete(*self.treeview.get_children())
        if len(self.job_block_list.job_list) > 0:
            for i, job_value in enumerate(self.job_block_list.job_list):
                self.treeview.insert('', 'end', values=(job_value.job_number, f'{datetime.strftime(job_value.insertion_date, "%d/%m/%Y %H:%M:%S")}'), tags=(even_odd.get(i % 2)))

    def __insert_job(self, job_number: int) -> None:
        result = self.job_block_list.add_job(job_number)
        if result:
            self.__update_job_list_by_date()
        else:
            showerror('Send error', f'Could not add {job_number} to job block list')

    def __delete(self) -> None:
        logger.debug('Delete')
        row_id = self.treeview.selection()
        if row_id:
            treeview_item = self.treeview.item(row_id)
            selected_job = treeview_item.get('values')[0]
            answer = askquestion('Delete', f'Do you really want to delete the entry {selected_job}')
            if answer == 'yes':
                if self.job_block_list.remove_job(selected_job):
                    self.__update_job_list_by_date()
                    
    def __update_job_list(self) -> None:
        self.configuration = self.database.get('configuration')
        try:
            file_name = f'{self.configuration.file_name}.{self.configuration.file_extension}'
            file_writer(self.configuration.file_path, file_name, '\n'.join([str(job_num) for job_num in self.job_block_list.get_job_list()]))
            self.set_treeview()
        except Exception as error:
            logger.error(f'Could not update job list due {error}')
            showerror('Update Error', f'Could not update job list due {error}.')

    def __send(self, event=None) -> None:
        logger.debug('Send')
        job_number = self.entry_job.get()
        if len(str(job_number)) >= self.configuration.job_minimum_length:
            self.entry_job.delete(0, 'end')
            self.__insert_job(job_number)
        else:
            self.entry_job.focus_force()
            self.entry_job.select_range(0, 'end')

    def update_configuration(self, new_config: Configuration) -> None:
        if new_config:
            self.configuration = new_config

    def __update(self):
        self.job_block_list.remove_older_than(self.__set_removal_date())
        self.database.save_update('job_list', self.job_block_list)
        self.__update_job_list()

    def __quit(self, event=None) -> None:
        if askokcancel('Quit', 'Do you want to quit?'):
            self.gui_configuration.check_update_win_pos(self.master.geometry(), 'main')
            logger.info('Forcing kill thread if it is open')                
            self.master.after(0, self.master.deiconify)      
            self.master.destroy()

    def __setting(self, event=None) -> None:
        logger.debug('Setting')        
        setting_view = Setting(self.master)
        self.setting_controller = SetttingsController(setting_view, self.update_configuration, self.database, self.gui_configuration)

    def __about(self, event=None) -> None:
        logger.info('About clicked')
        about = About('''
            Application name: Automatic Calculation Blocker
            Version: 1.10.00
            Developed by: Akio Fujitani
            e-mail: akiofujitani@gmail.com
        ''', resource_path('./Img/bedo_mora_siris.png'))
        self.about_controller = AboutController(self.master, about, self.gui_configuration)