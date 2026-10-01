import logging
from threading import Event, Thread
from .file_mover import file_mover
from .database import Database
from .gui_config import GuiConfiguration
from .scripts.json_config import load_json_config
from .templates import data_object_list, gui_configuration


logger = logging.getLogger('main_model')

class Model():
    '''
    Model main class
    '''
    def __init__(self) -> None:
        try:
            self.database = Database.init_dict(load_json_config('./data/data_object_list.json', data_object_list))  
            self.gui_configuration = GuiConfiguration.init_dict(load_json_config('./data/gui_configuration.json', gui_configuration))
        except Exception as error:
            logger.error(f'Could not load data_object_list.json due {error}')
            raise error
        self.routine_name = 'File mover backup'
        self.event = Event()
        self.thread = None
        self.__start_on_initialize()        

    def __start_on_initialize(self):
        '''
        Start routine if condition is met
        '''
        configuration = self.database.get('config')
        if configuration.start_delay:
            self.event.clear()
            self.thread = Thread(target=file_mover, args=(self.database, self.event, configuration.start_delay), name=self.routine_name)
            self.thread.start()            

    def start_routine(self):
        '''
        Start routine
        '''
        logger.info(f'starting {self.routine_name}')
        if not self.routine_active():
            self.event.clear()
            self.thread = Thread(target=file_mover, args=(self.database, self.event, ), name=self.routine_name)
            self.thread.start()

    def pause_temp_routine(self):
        '''
        Temporary pause
        '''
        self.stop_routine()
        configuration = self.database.get('config')
        self.event.clear()
        self.thread = Thread(target=file_mover, args=(self.database, self.event, configuration.pause_time), name=self.routine_name)
        self.thread.start()         

    def stop_routine(self):  
        '''
        Stop routine
        '''             
        if self.routine_active():
            logger.info(f'stopping {self.routine_name}')
            self.event.set()
            self.thread.join()
        return

    def restart_routine(self):
        '''
        Restart routine
        '''
        self.stop_routine()
        self.start_routine()

    def routine_active(self):
        '''
        Check if current routine is running
        '''
        if not self.thread:
            logger.info('No thread created')
            return False
        if not self.thread.is_alive():
            logger.info('Thread is already stopped')
            return False
        return True  

    def on_close(self):
        '''
        Ends the routine on application close
        '''
        if not self.thread:
            return
        if not self.thread.is_alive():
            return
        self.stop_routine()
        self.thread.join()
        logger.info('Thread termination complete')