import logging
from time import sleep
from threading import Event
from os.path import normpath, abspath
from os.path import split as path_split
from datetime import datetime, timedelta
from .classes.config import Configuration
from .scripts.file_handler import listFilesInDirSubDir, fileCreationDate, file_move_copy


logger = logging.getLogger('file_mover')


def wait_time(event: Event, wait_time: int) -> None:
    logger.info(f'Wait time ... {wait_time}')
    while wait_time > 0:
        if event.is_set():
            logger.info(f'Wait time interrupted at {wait_time}')
            return        
        if int(wait_time / 3600) > 0 and wait_time % 3600 == 0:
            logger.info('More than a hour')
        if int(wait_time / 1800) > 0 and wait_time < 3600 and wait_time % 1800 == 0:
            logger.info('More than 30 minutes')
        if int(wait_time / 900) > 0 and wait_time < 1800 and wait_time % 900 == 0:
            logger.info('More than 15 minutes')
        if int(wait_time / 60) > 0 and wait_time < 900:
            if wait_time % 600 == 0 or wait_time % 300 == 0:
                logger.info(f'{int(wait_time / 60)} minutes')
            if wait_time < 360 and wait_time % 60 == 0:
                logger.info(f'{int(wait_time / 60)} minutes')
        if wait_time < 60:
            if wait_time % 15 == 0:
                logger.info(f'Time to next cicle {wait_time} seconds')
            if wait_time < 10:
                logger.info(f'Time to next cicle {wait_time} seconds')
        wait_time -= 1
        sleep(1)
    return


def file_mover(config: Configuration, event: Event) -> None:
    path_type = {'Yearly' : 1, 'Monthly' : 2, 'Daily' : 3}

    while True:
        if len(config.directory_list) > 0:
            for move_settings in config.directory_list:
                try:
                    if event.is_set():
                        logger.info('Event is set')
                        return
                    logger.info(f'Listing files from {move_settings.source}')
                    path_organization = path_type[move_settings.path_organization]
                    file_list = listFilesInDirSubDir(move_settings.source, move_settings.extention)
                    if len(file_list) > 0:
                        logger.info(f'Starting moving files')
                        counter = 0
                        for file in file_list:
                            file_last_modification = fileCreationDate(file)
                            if datetime.today().date() - timedelta(days=move_settings.days_from_today) >= file_last_modification:
                                file_date_tuple = (file_last_modification.year, config.month_name_list[int(file_last_modification.month) - 1], "{:02d}".format(file_last_modification.day))     
                                path_date = ''
                                for i in range(path_organization):
                                    path_date = f'{path_date}/{file_date_tuple[i]}'
                                file_destination = f'{move_settings.destination}{path_date}'
                                file_destination_path = normpath(file_destination)
                                source_path, file_name = path_split(abspath(file))
                                try:
                                    file_move_copy(source_path, file_destination_path, file_name, move_settings.copy, True)
                                except Exception as error:
                                    logger.warning(f'Could not move file {file_name} due {error}')
                                counter += 1
                                if counter >= config.file_per_cicle:
                                    logger.info(f'Number {config.file_per_cicle} of files per cicle reached.')
                                    break
                            if event.is_set():
                                logger.info(f'Counter at {counter}')
                                logger.info('Event is set')
                                return
                except Exception as error:
                    event.set()
                    logger.warning(f'Error processing files {error}')
                    return
        wait_time(event, config.min_to_seconds())
