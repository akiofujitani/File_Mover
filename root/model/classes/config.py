import logging
from dataclasses import dataclass
from os.path import normpath, abspath


logger = logging.getLogger('config')


@dataclass
class Move_Settings:
    source: str
    destination: str
    extention: str
    days_from_today: int
    copy: bool
    path_organization: str


    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True

    @classmethod
    def init_dict(cls, dict_values: dict[str, any]) -> object:
        try:
            source = normpath(abspath(dict_values.get('source')))
            destination = normpath(abspath(dict_values.get('destination')))
            extension = str(dict_values.get('extension'))
            days_from_today = int(dict_values.get('days_from_today'))
            copy = eval(dict_values.get('copy'))
            path_organization = dict_values.get('path_organization')
            return cls(source, destination, extension, days_from_today, copy, path_organization)
        except Exception as error:
            logger.error(f'Could not load move settings due {error}')
            return


@dataclass
class Configuration:
    wait_time: int
    file_per_cicle: int
    month_name_list: list
    directory_list: list

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return NotImplemented
        else:
            self_values = self.__dict__
            for key in self_values.keys():
                if not getattr(self, key) == getattr(other, key):
                    return False
            return True
    
    def directory_list_add(self, move_settings: Move_Settings) -> None:
        self.directory_list.append(move_settings)

    def min_to_seconds(self) -> int:
        return self.wait_time * 60

    @classmethod
    def init_dict(cls, dict_values: dict[str, any]) -> object:
        try:
            wait_time = dict_values.get('wait_time')
            file_per_cicle = dict_values.get('file_per_cicle')
            month_name_list = [str(month) for month in dict_values.get('month_name_list')]
            directory_list = list(Move_Settings.init_dict(move_setting) for move_setting in dict_values.get('directory_list'))
            return cls(wait_time, file_per_cicle, month_name_list, directory_list)
        except Exception as error:
            logger.error(f'Configuration load erro due {error}')
            return