import logging
from queue import Queue
from view.main import View
from model.scripts.log_builder import logger_setup
from model.main import Model
from controller.main import Controller


logger = logging.getLogger('main')


def main():
    '''
    Main
    '''
    log_queue = Queue()
    logger = logging.getLogger()
    logger_setup(logger, log_queue)
    
    view = View()
    model = Model()
    controller = Controller(view, model, log_queue)
    controller.start()
    

if __name__ == '__main__':
    main()